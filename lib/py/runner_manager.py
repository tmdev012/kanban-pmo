"""
runner_manager.py — Runner taxonomy loader and stub dispatcher.
Reads config/runners.yml, maps labor skills to execution contexts.
Version: 1.0.0 | Created: 2026-02-22
"""

from pathlib import Path
import yaml

_RUNNERS_YML = Path(__file__).parent.parent.parent / "config" / "runners.yml"

# event_type → skill_id mapping (IssueEvent conventions)
_EVENT_TO_SKILL = {
    "created": "card.create",
    "wip":     "card.move",
    "closed":  "card.close",
    "tick":    "verify.run",
    "probe":   "probe.sync",
    "model":   "model.build",
    "doc":     "doc.sync",
    "audit":   "cred.audit",
    "plan":    "sprint.plan",
    "retro":   "sprint.retro",
    "ignore":  "git.ignore",
    "lock":    "git.lock",
    "revert":  "git.revert",
}


class RunnerManager:
    def __init__(self):
        self._runners: dict = {}
        self._skill_index: dict = {}   # skill_id → runner_name

    def load(self) -> dict:
        """Load runners from config/runners.yml. Returns runners dict."""
        data = yaml.safe_load(_RUNNERS_YML.read_text())
        self._runners = data.get("runners", {})
        self._skill_index = {}
        for runner_name, cfg in self._runners.items():
            for skill in cfg.get("skills", []):
                self._skill_index[skill] = runner_name
        return self._runners

    def get_runner_for_skill(self, skill_id: str) -> str:
        """Return runner name for a given skill_id, or 'unknown'."""
        return self._skill_index.get(skill_id, "unknown")

    def dispatch(self, event) -> dict:
        """
        Stub dispatcher — logs intent and returns queued confirmation.
        Actual subprocess/gRPC execution implemented in B11.

        Args:
            event: IssueEventRequest (has .task_id, .event_type, .repo_name, .payload)
        Returns:
            dict with keys: queued, runner, skill, task_id
        """
        event_type = getattr(event, "event_type", "") or ""
        task_id    = getattr(event, "task_id", "")    or ""
        repo_name  = getattr(event, "repo_name", "")  or ""

        skill_id   = _EVENT_TO_SKILL.get(event_type, event_type)
        runner     = self.get_runner_for_skill(skill_id)
        runner_cfg = self._runners.get(runner, {})

        print(
            f"[runner] queued runner={runner!r} skill={skill_id!r} "
            f"task={task_id!r} repo={repo_name!r} "
            f"executor={runner_cfg.get('executor', '?')!r}"
        )

        return {
            "queued":   True,
            "runner":   runner,
            "skill":    skill_id,
            "task_id":  task_id,
            "executor": runner_cfg.get("executor", "unknown"),
        }

    def list_runners(self) -> list:
        """Return sorted list of runner names."""
        return sorted(self._runners.keys())
