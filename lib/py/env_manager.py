"""
env_manager.py — .env template authority across registered repos
All writes go through governor.write_file().
Version: 1.0.0 | Created: 2026-02-19
"""

import re
from pathlib import Path
from typing import Optional
from .governor import write_file, get_repo

TEMPLATES_DIR = Path(__file__).parent.parent.parent / "config" / "env_templates"


def load_template(template_name: str) -> str:
    path = TEMPLATES_DIR / f"{template_name}.env"
    if not path.exists():
        raise FileNotFoundError(f"No template '{template_name}' at {path}")
    return path.read_text()


def apply_template(repo_name: str, template_name: Optional[str] = None) -> Path:
    """
    Apply an .env template to a registered repo.
    If template_name is None, reads from repo's registry entry.
    Merges — preserves existing keys, only adds missing ones.
    """
    if template_name is None:
        repo = get_repo(repo_name)
        template_name = repo.get("env_template")
        if not template_name:
            raise ValueError(f"No env_template set for '{repo_name}' in registry.")
    content = load_template(template_name)
    return write_file(repo_name, ".env", content, merge=True)


def set_key(repo_name: str, key: str, value: str) -> Path:
    """
    Set or update a single KEY=VALUE in a repo's .env.
    Creates .env if it doesn't exist. Never clobbers other keys.
    """
    repo = get_repo(repo_name)
    env_path = Path(repo["local_path"]) / ".env"

    if env_path.exists():
        lines = env_path.read_text().splitlines()
    else:
        lines = []

    pattern = re.compile(rf"^{re.escape(key)}\s*=")
    new_line = f"{key}={value}"
    updated = False
    for i, line in enumerate(lines):
        if pattern.match(line):
            lines[i] = new_line
            updated = True
            break
    if not updated:
        lines.append(new_line)

    content = "\n".join(lines) + "\n"
    return write_file(repo_name, ".env", content, merge=False)


def get_key(repo_name: str, key: str) -> Optional[str]:
    """Read a single key from a repo's .env without loading the whole file."""
    repo = get_repo(repo_name)
    env_path = Path(repo["local_path"]) / ".env"
    if not env_path.exists():
        return None
    pattern = re.compile(rf"^{re.escape(key)}\s*=\s*(.+)")
    for line in env_path.read_text().splitlines():
        m = pattern.match(line)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    return None


def list_templates() -> list:
    return [p.stem for p in TEMPLATES_DIR.glob("*.env")]
