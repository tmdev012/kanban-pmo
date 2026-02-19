"""
governor.py — kanban-pmo File-Write Governor
Single authorised surface for cross-repo file writes.
Version: 1.0.0 | Created: 2026-02-19
"""

import os
import yaml
from pathlib import Path
from typing import Optional

REGISTRY_PATH = Path(__file__).parent.parent.parent / "config" / "repos.yml"


# ── Registry I/O ──────────────────────────────────────────────────────────────

def load_registry() -> dict:
    with open(REGISTRY_PATH) as f:
        return yaml.safe_load(f)


def _save_registry(data: dict) -> None:
    with open(REGISTRY_PATH, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


# ── Repo CRUD ─────────────────────────────────────────────────────────────────

def add_repo(
    name: str,
    local_path: str,
    remote_url: Optional[str] = None,
    branch: str = "main",
    env_template: Optional[str] = None,
    gitignore_profile: Optional[str] = None,
    status: str = "active",
    role: str = "domain-project",
    env_stage: str = "dev",
) -> None:
    reg = load_registry()
    reg["repos"][name] = {
        "local_path": local_path,
        "remote_url": remote_url,
        "branch": branch,
        "env_template": env_template,
        "gitignore_profile": gitignore_profile,
        "status": status,
        "role": role,
        "env_stage": env_stage,
        "write_authority": "kanban-pmo",
    }
    reg["meta"]["total_known"] = len(reg["repos"]) + len(reg.get("pending", []))
    reg["meta"]["discovered_local"] = len(reg["repos"])
    reg["meta"]["updated"] = _today()
    _save_registry(reg)


def get_repo(name: str) -> dict:
    reg = load_registry()
    repo = reg["repos"].get(name)
    if not repo:
        raise KeyError(f"Repo '{name}' not in registry. Run governor.add_repo() first.")
    return repo


def list_repos(status: Optional[str] = None) -> dict:
    reg = load_registry()
    repos = reg["repos"]
    if status:
        repos = {k: v for k, v in repos.items() if v.get("status") == status}
    return repos


def update_repo(name: str, **kwargs) -> None:
    reg = load_registry()
    if name not in reg["repos"]:
        raise KeyError(f"Repo '{name}' not found in registry.")
    reg["repos"][name].update(kwargs)
    reg["meta"]["updated"] = _today()
    _save_registry(reg)


def discover() -> list:
    """
    Discover local git repos under HOME and register any not already tracked.
    Returns list of newly added repo names.
    """
    import subprocess
    home = Path.home()
    result = subprocess.run(
        ["find", str(home), "-maxdepth", "2", "-name", ".git", "-type", "d"],
        capture_output=True, text=True
    )
    found = []
    reg = load_registry()
    for git_dir in result.stdout.strip().splitlines():
        local_path = str(Path(git_dir).parent)
        name = Path(local_path).name
        if name in reg["repos"] or name == ".oh-my-zsh":
            continue
        add_repo(name=name, local_path=local_path)
        found.append(name)
    return found


# ── File-Write Primitive ──────────────────────────────────────────────────────

def write_file(repo_name: str, relative_path: str, content: str, merge: bool = False) -> Path:
    """
    Write content to a file inside a registered repo.
    This is the ONLY authorised write path. All governor ops call this.

    Args:
        repo_name:     Key in repos.yml
        relative_path: Path relative to repo root (e.g. ".env", ".gitignore")
        content:       File content to write
        merge:         If True, append non-duplicate lines instead of overwrite

    Returns:
        Resolved Path of written file.
    """
    repo = get_repo(repo_name)
    target = Path(repo["local_path"]) / relative_path

    if merge and target.exists():
        existing = target.read_text().splitlines()
        new_lines = [ln for ln in content.splitlines() if ln not in existing]
        if not new_lines:
            return target  # nothing to add
        target.write_text("\n".join(existing + new_lines) + "\n")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)

    return target


# ── Helpers ───────────────────────────────────────────────────────────────────

def _today() -> str:
    from datetime import date
    return str(date.today())


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        for name, meta in list_repos().items():
            print(f"  {name:30s} [{meta['status']:8s}] {meta['role']:20s} {meta['local_path']}")
    elif cmd == "discover":
        added = discover()
        print(f"Discovered {len(added)} new repos: {added}")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
