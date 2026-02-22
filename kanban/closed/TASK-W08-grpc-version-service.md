# TASK-W08: VersionService gRPC — GetVersion + GetChangelog

- **Status:** closed
- **Labels:** grpc, infra, protocol, priority:high
- **Assignee:** tmdev012
- **Sprint:** S01 (2026-02-22)
- **Milestone:** S01 — v3.3.0 Ship
- **Closed:** 2026-02-22
- **Effort:** ~45m

## Description

Add `VersionService` to kanban.proto with two RPCs: `GetVersion` (returns current version, date, model names) and `GetChangelog` (returns full CHANGELOG.md content + summary for prompt injection). Regenerate stubs. Wire servicer in grpc_server.py. This makes the changelog a live gRPC data feed — not a static file.

## Acceptance Criteria

- [x] `VersionService` added to `proto/kanban.proto`
- [x] `GetVersion` RPC: returns version, date, model_3b, model_8b
- [x] `GetChangelog` RPC: returns latest_version, latest_date, summary, full_text
- [x] Stubs regenerated via `grpc_tools.protoc`
- [x] `VersionServiceServicer` implemented in `grpc_server.py`
- [x] `add_VersionServiceServicer_to_server` wired in `serve()`
- [x] `sashi probe changelog` queries via gRPC (not file read)

## Solution

### Root of upgrade
`VersionService` in `kanban.proto` — single authority for version state:
```proto
service VersionService {
  rpc GetVersion   (VersionRequest)   returns (VersionResponse);
  rpc GetChangelog (ChangelogRequest) returns (ChangelogResponse);
}
```

### Servicer reads CHANGELOG.md live
```python
class VersionServiceServicer:
    _CHANGELOG = Path.home() / "ollama-local/CHANGELOG.md"

    def GetVersion(self, request, context):
        # parse first ## v line for version + date
        ...
        return kanban_pb2.VersionResponse(
            version="3.3.0", date="2026-02-22",
            model_3b="fast-sashi", model_8b="sashi-llama-8b"
        )

    def GetChangelog(self, request, context):
        full = self._CHANGELOG.read_text()
        summary = extract_latest_bullets(full)
        return kanban_pb2.ChangelogResponse(
            latest_version="3.3.0", latest_date="2026-02-22",
            summary=summary, full_text=full
        )
```

### Reproducibility
```bash
sashi grpc start
sashi probe changelog   # queries :50051 GetChangelog RPC
sashi probe status      # shows version from gRPC
```

## Commits
- `kanban-pmo b3c479d` — chore: bump all version strings → v3.2.0 (base)
- `kanban-pmo [unstaged]` — VersionService proto + stubs + servicer

## Files
- `~/kanban-pmo/proto/kanban.proto` (MODIFIED — VersionService added)
- `~/kanban-pmo/generated/kanban_pb2.py` (REGENERATED)
- `~/kanban-pmo/generated/kanban_pb2_grpc.py` (REGENERATED)
- `~/kanban-pmo/server/grpc_server.py` (MODIFIED — VersionServiceServicer)

---
*Closed: 2026-02-22 | Sprint S01 | v3.3.0*
