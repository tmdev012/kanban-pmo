"""
gitignore_manager.py — Profile-based .gitignore authority
All writes go through governor.write_file().
Version: 1.0.0 | Created: 2026-02-19
"""

from pathlib import Path
from typing import List
from governor import write_file, get_repo, load_registry

PROFILES_DIR = Path(__file__).parent.parent.parent / "config" / "gitignore_profiles"


def load_profile(profile_name: str) -> List[str]:
    path = PROFILES_DIR / f"{profile_name}.gitignore"
    if not path.exists():
        raise FileNotFoundError(f"No profile '{profile_name}' at {path}")
    return [ln for ln in path.read_text().splitlines() if ln and not ln.startswith("##")]


def apply_profile(repo_name: str, profile_name: Optional[str] = None) -> Path:
    """
    Apply a named profile to a repo's .gitignore.
    If profile_name is None, reads it from the repo's registry entry.
    Merges — never overwrites existing rules.
    """
    if profile_name is None:
        repo = get_repo(repo_name)
        profile_name = repo.get("gitignore_profile")
        if not profile_name:
            raise ValueError(f"No gitignore_profile set for '{repo_name}' in registry.")
    rules = load_profile(profile_name)
    return merge_rules(repo_name, rules)


def merge_rules(repo_name: str, rules: List[str]) -> Path:
    """Append rules to a repo's .gitignore, skipping duplicates."""
    content = "\n".join(rules)
    return write_file(repo_name, ".gitignore", content, merge=True)


def list_profiles() -> List[str]:
    return [p.stem for p in PROFILES_DIR.glob("*.gitignore")]


from typing import Optional  # noqa: E402 (needed after forward ref above)
