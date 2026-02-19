# TASK-B07: kanban-pmo Governor Layer — File-Write Authority

- **Status:** backlog
- **Labels:** infra, kanban, priority:high
- **Parent:** TASK-B06 (T1 of 5)
- **Assignee:** tmdev012
- **Sprint:** S01
- **Time:** 1h (estimated)
- **Milestone:** S01 — Governance Prerequisite
- **Created:** 2026-02-19

## Description

kanban-pmo must hold highest file-write hierarchy across all sibling repos.
This requires a registry of all repos and a Python governor layer that is the
only authorised surface for writing `.env`, `.gitignore`, and repo metadata.

## Deliverables

- [ ] `config/repos.yml` — registry: name, path, remote, branch, env, gitignore, status, env_stage
- [ ] `lib/py/governor.py` — load/save registry, write_file primitive, add/update/list repos
- [ ] `lib/py/gitignore_manager.py` — load profiles, apply/merge rules per repo
- [ ] `lib/py/env_manager.py` — load templates, set keys, apply to any registered repo

## Acceptance Criteria

- [ ] `governor.write_file("ollama-local", ".env", content)` writes to ~/ollama-local/.env
- [ ] `governor.list_repos(status="active")` returns all active repos
- [ ] `gitignore_manager.merge_rules("ollama-local", ["*.pyc"])` appends without duplicates
- [ ] `env_manager.set_key("ollama-local", "OFFLINE_MODE", "true")` sets key in .env

---

*Card created: 2026-02-19 | Sub-task: B06-T1*
