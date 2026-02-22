"""
grpc_server.py — kanban-pmo gRPC Servicer Implementations
Wraps governor, gitignore_manager, env_manager behind a gRPC interface.
Version: 1.0.0 | Created: 2026-02-19
"""

import sys
import os
from pathlib import Path

# Ensure kanban-pmo root is on path for lib.py imports
_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

# Import generated stubs (populated after protoc run)
try:
    sys.path.insert(0, str(_ROOT / "generated"))
    import kanban_pb2
    import kanban_pb2_grpc
    _STUBS_AVAILABLE = True
except ImportError:
    _STUBS_AVAILABLE = False

import grpc
from concurrent import futures

from lib.py.governor import list_repos, get_repo, add_repo, update_repo, write_file
from lib.py.gitignore_manager import merge_rules
from lib.py.env_manager import set_key


# ── RepoRegistry Servicer ────────────────────────────────────────────────────

class RepoRegistryServicer:
    """Implements RepoRegistry RPC surface."""

    def ListRepos(self, request, context):
        status_filter = request.status_filter or None
        repos = list_repos(status=status_filter)
        entries = [
            kanban_pb2.RepoEntry(
                name=name,
                local_path=meta.get("local_path", ""),
                remote_url=meta.get("remote_url") or "",
                branch=meta.get("branch", "main"),
                env_template=meta.get("env_template") or "",
                gitignore_profile=meta.get("gitignore_profile") or "",
                status=meta.get("status", ""),
                role=meta.get("role", ""),
                env_stage=meta.get("env_stage", ""),
                write_authority=meta.get("write_authority", ""),
            )
            for name, meta in repos.items()
        ]
        return kanban_pb2.ListReposResponse(repos=entries)

    def GetRepo(self, request, context):
        try:
            meta = get_repo(request.name)
        except KeyError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))
            return
        return kanban_pb2.RepoEntry(
            name=request.name,
            local_path=meta.get("local_path", ""),
            remote_url=meta.get("remote_url") or "",
            branch=meta.get("branch", "main"),
            status=meta.get("status", ""),
            role=meta.get("role", ""),
        )

    def AddRepo(self, request, context):
        r = request.repo
        add_repo(
            name=r.name,
            local_path=r.local_path,
            remote_url=r.remote_url or None,
            branch=r.branch or "main",
            env_template=r.env_template or None,
            gitignore_profile=r.gitignore_profile or None,
            status=r.status or "active",
            role=r.role or "domain-project",
            env_stage=r.env_stage or "dev",
        )
        return kanban_pb2.StatusResponse(ok=True, message=f"Added repo '{r.name}'")

    def UpdateRepo(self, request, context):
        try:
            update_repo(request.name, **dict(request.fields))
        except KeyError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))
            return
        return kanban_pb2.StatusResponse(ok=True, message=f"Updated '{request.name}'")


# ── FileWrite Servicer ───────────────────────────────────────────────────────

class FileWriteServicer:
    """Implements FileWrite RPC surface. Delegates to governor.write_file()."""

    def Write(self, request, context):
        try:
            written = write_file(
                request.repo_name,
                request.relative_path,
                request.content,
                merge=request.merge,
            )
            return kanban_pb2.WriteResponse(ok=True, written_path=str(written))
        except Exception as e:
            return kanban_pb2.WriteResponse(ok=False, error=str(e))

    def MergeLines(self, request, context):
        try:
            written = merge_rules(request.repo_name, list(request.lines))
            return kanban_pb2.WriteResponse(ok=True, written_path=str(written))
        except Exception as e:
            return kanban_pb2.WriteResponse(ok=False, error=str(e))

    def SetEnvKey(self, request, context):
        try:
            written = set_key(request.repo_name, request.key, request.value)
            return kanban_pb2.WriteResponse(ok=True, written_path=str(written))
        except Exception as e:
            return kanban_pb2.WriteResponse(ok=False, error=str(e))


# ── IssueEvent Servicer ──────────────────────────────────────────────────────

class IssueEventServicer:
    """Minimal event log — emits to stdout; Stream yields buffered events."""

    _event_log: list = []

    def Emit(self, request, context):
        entry = {
            "task_id": request.task_id,
            "repo_name": request.repo_name,
            "event_type": request.event_type,
            "field": request.field,
            "payload": request.payload,
            "timestamp": request.timestamp,
        }
        IssueEventServicer._event_log.append(entry)
        print(f"[event] {request.event_type} {request.task_id} {request.field}")
        return kanban_pb2.StatusResponse(ok=True)

    def Stream(self, request, context):
        for entry in IssueEventServicer._event_log:
            if not request.repo_filter or entry["repo_name"] == request.repo_filter:
                yield kanban_pb2.IssueEventRequest(**entry)


# ── ProbeSync Servicer ───────────────────────────────────────────────────────

class ProbeSyncServicer:
    """Bridge to persist-memory-probe — runs integrate.py, exposes FsWrite."""

    _PROBE_ROOT = Path.home() / "persist-memory-probe"
    _INTEGRATE  = _PROBE_ROOT / "lib" / "py" / "integrate.py"

    def SyncRepo(self, request, context):
        import subprocess, re
        try:
            cmd = ["python3", str(self._INTEGRATE)]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(self._PROBE_ROOT / "lib" / "py"),
            )
            # Parse "Synced N repos → ..." from integrate.py stdout
            m = re.search(r"Synced (\d+) repos", result.stdout)
            files_synced = int(m.group(1)) if m else 0
            ok = result.returncode == 0
            error = result.stderr.strip() if not ok else ""
            print(f"[probe] SyncRepo repo={request.repo_name!r} ok={ok} files={files_synced}")
            return kanban_pb2.SyncRepoResponse(ok=ok, files_synced=files_synced, error=error)
        except Exception as e:
            return kanban_pb2.SyncRepoResponse(ok=False, error=str(e))

    def FsWrite(self, request, context):
        try:
            path = Path(request.target_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(request.content)
            print(f"[probe] FsWrite path={path}")
            return kanban_pb2.WriteResponse(ok=True, written_path=str(path))
        except Exception as e:
            return kanban_pb2.WriteResponse(ok=False, error=str(e))


# ── Server bootstrap ─────────────────────────────────────────────────────────

def serve(port: int = 50051):
    if not _STUBS_AVAILABLE:
        raise RuntimeError(
            "gRPC stubs not found in generated/. "
            "Run: python -m grpc_tools.protoc -I proto --python_out=generated "
            "--grpc_python_out=generated proto/kanban.proto"
        )
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    kanban_pb2_grpc.add_RepoRegistryServicer_to_server(RepoRegistryServicer(), server)
    kanban_pb2_grpc.add_FileWriteServicer_to_server(FileWriteServicer(), server)
    kanban_pb2_grpc.add_IssueEventServicer_to_server(IssueEventServicer(), server)
    kanban_pb2_grpc.add_ProbeSyncServicer_to_server(ProbeSyncServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"[grpc] kanban-pmo server listening on :{port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
