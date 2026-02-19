# TASK-B09: persist-memory-probe Upgrade — Real Tracking Implementations

- **Status:** wip
- **Labels:** probe, infra, priority:high
- **Parent:** TASK-B06 (T3 of 5)
- **Assignee:** tmdev012
- **Sprint:** S01
- **Time:** 1h (estimated)
- **Milestone:** S01 — Governance Prerequisite
- **Created:** 2026-02-19

## Description

Replace stub implementations in persist-memory-probe with real functional code.
`repo_tracker.py` discovers and tracks repos, `fs_writer.py` writes files
under governor authority, and `db_sync.py` syncs probe state to SQLite.

## Deliverables

- [x] `lib/py/repo_tracker.py` — real repo discovery + status tracking
- [x] `lib/py/fs_writer.py` — authorised file write bridge (delegates to kanban-pmo governor)
- [x] `lib/py/db_sync.py` — sync probe metadata to SQLite history.db

## Acceptance Criteria

- [ ] `repo_tracker.scan()` returns ≥1 repo discovered under HOME
- [ ] `fs_writer.write("ollama-local", ".probe-touch", "ok\n")` creates file without error
- [ ] `db_sync.sync_repos(repos)` inserts/updates rows in probe SQLite table
- [ ] All three modules import without error from persist-memory-probe root

---

*Card created: 2026-02-19 | Sub-task: B06-T3*
