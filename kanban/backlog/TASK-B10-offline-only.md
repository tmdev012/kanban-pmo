# TASK-B10: ollama-local Offline-Only Mode — OFFLINE_MODE=true

- **Status:** backlog
- **Labels:** ollama, infra, priority:high
- **Parent:** TASK-B06 (T4 of 5)
- **Assignee:** tmdev012
- **Sprint:** S01
- **Time:** 30m (estimated)
- **Milestone:** S01 — Governance Prerequisite
- **Created:** 2026-02-19

## Description

Set `OFFLINE_MODE=true` in ollama-local's `.env` via the governor's `env_manager.set_key()`.
Archive any pipeline.proto or cloud-routing stubs that conflict with offline-only stance.

## Deliverables

- [ ] `OFFLINE_MODE=true` set in `~/ollama-local/.env` via `env_manager.set_key()`
- [ ] Any `pipeline.proto` or cloud-routing stubs archived to `old-archive/`
- [ ] `config/repos.yml` entry for `ollama-local` has `env_stage: offline`

## Acceptance Criteria

- [ ] `grep OFFLINE_MODE ~/ollama-local/.env` returns `OFFLINE_MODE=true`
- [ ] `governor.get_repo("ollama-local")["env_stage"]` returns `"offline"`
- [ ] No unarchived cloud-routing files remain in `~/ollama-local/`

---

*Card created: 2026-02-19 | Sub-task: B06-T4*
