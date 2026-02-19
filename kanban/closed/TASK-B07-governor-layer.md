# TASK-B07: kanban-pmo Governor Layer — File-Write Authority

- **Status:** closed
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

- [x] `config/repos.yml` — registry: name, path, remote, branch, env, gitignore, status, env_stage
- [x] `lib/py/governor.py` — load/save registry, write_file primitive, add/update/list repos
- [x] `lib/py/gitignore_manager.py` — load profiles, apply/merge rules per repo
- [x] `lib/py/env_manager.py` — load templates, set keys, apply to any registered repo

## Acceptance Criteria

- [x] `governor.write_file("ollama-local", ".env", content)` writes to ~/ollama-local/.env
- [x] `governor.list_repos(status="active")` returns all active repos
- [x] `gitignore_manager.merge_rules("ollama-local", ["*.pyc"])` appends without duplicates
- [x] `env_manager.set_key("ollama-local", "OFFLINE_MODE", "true")` sets key in .env

## Evidence

```
$ python3 -c "from lib.py.governor import write_file; ..."
AC1 write_file: /tmp/tmpzr46yytm/.env — PASS
AC2 list_repos(active): ['kanban-pmo', 'ollama-local', 'persist-memory-probe', 'ollama-telemetry', 'football-telemetry', 'portfolio-dashboard'] — PASS
AC3 merge_rules no-dup: PASS
AC4 set_key OFFLINE_MODE=true: PASS
Ran: 2026-02-19 | Exit: 0
```

---

*Card created: 2026-02-19 | Closed: 2026-02-19 | Sub-task: B06-T1*
