# TASK-B06: gRPC Governance Layer — kanban-pmo as CFO, Cross-Repo Authority

- **Status:** backlog
- **Labels:** infra, kanban, workflow, priority:high
- **Assignee:** tmdev012
- **Sprint:** S01 — fast-track (pulled from S20-S21)
- **Time:** 3h (estimated)
- **Milestone:** S01 — v3.2.0 Ship → Governance Prerequisite
- **Created:** 2026-02-19
- **Blocked by:** none
- **Blocks:** all future cross-repo ops

---

## Context

Pipelines removed across all 3 repos (2026-02-19). Reason: GitHub Actions runners are not
available locally. All shell scripts inside those workflows had no logic aligned to actual
workflow — they were dead weight pretending to be CI.

This issue replaces them with a clean, intentional architecture:
kanban-pmo as the single governor (CFO) over all repos.

---

## Problem Statement

- 14 pipeline YMLs archived: 10 in kanban-pmo, 2 in ollama-local, 2 in persist-memory-probe
- persist-memory-probe is lazy: its `lib/` exists but has no integration contract with kanban-pmo
- ollama-local gRPC proto exists (`pipeline/proto/pipeline.proto`) but is disconnected
- persist-memory-probe gRPC proto exists (`webhooks/grpc/probe.proto`) but is disconnected
- No single repo has authority to read/write across all repos in a controlled way
- ollama-local must move to offline-only workhorse mode (no CI, no runners, pure execution)

---

## Scope of Work

### 1. kanban-pmo: Establish File-Write Hierarchy (Governor Role)

kanban-pmo is the CFO. It is the only repo authorised to:

- Write to `.gitignore` across sibling repos
- Write/update `.env` across sibling repos (secrets handled via probe)
- Know about dev/staging environments per repo
- Hold the canonical repo registry (all 21+ repos, their remotes, env, status)

**Deliverables:**
- [ ] `config/repos.yml` — registry of all repos: name, local_path, remote_url, branch, env, status
- [ ] `lib/governor.py` — repo registry reader/writer with file-write primitives
- [ ] `lib/gitignore_manager.py` — apply/merge .gitignore rules to any registered repo
- [ ] `lib/env_manager.py` — read/apply .env templates to any registered repo
- [ ] All writes go through kanban-pmo's governor layer. No direct file writes from other repos.

### 2. gRPC Transport Layer (Sanitised, Not Ad-Hoc)

Replace pipeline shell glue with a proper gRPC contract.

**Deliverables:**
- [ ] `proto/kanban.proto` — kanban-pmo service definition
  - `RepoRegistry` RPC: list/get/update repo metadata
  - `FileWrite` RPC: write .env / .gitignore to a registered repo path
  - `IssueEvent` RPC: emit card status changes (open/wip/close)
  - `ProbeSync` RPC: trigger persist-memory snapshot
- [ ] Generated stubs committed to `generated/`
- [ ] `server/grpc_server.py` — gRPC server (listens on unix socket, port 50051 fallback)
- [ ] Existing `pipeline/proto/pipeline.proto` in ollama-local: evaluate for consolidation or
  retire it in favour of this canonical proto

### 3. persist-memory-probe: Upgrade (No More Lazy)

Current state: lib files exist but are stubs. `webhooks/grpc/probe.proto` is defined but
unused. `lib/sh/sync-all-repos.sh` syncs nothing real.

**Deliverables:**
- [ ] Implement `lib/py/repo_tracker.py` fully: detect all local git repos, emit to governor
- [ ] Implement `lib/py/fs_writer.py` fully: receive write instructions from kanban-pmo governor
- [ ] Implement `lib/py/db_sync.py` fully: sync kanban-pmo DB snapshots to probe storage
- [ ] Wire `webhooks/grpc/probe.proto` to kanban-pmo's `ProbeSync` RPC
- [ ] Remove `lib/sh/cron-runner.sh` (cron = ad-hoc = wrong). Replace with gRPC trigger.
- [ ] `hooks/pre/context-check.sh` and `hooks/post/dev-snapshot.sh` must call governor, not curl

### 4. ollama-local: Offline-Only Mode

ollama-local is the workhorse. It runs inference. That is its only job.

**Deliverables:**
- [ ] Remove any cloud-dependency assumptions from `.env`
- [ ] `pipeline/proto/pipeline.proto` — either retire (archive) or align to kanban-pmo proto
- [ ] `sashi` CLI: all network calls go through gRPC to kanban-pmo, not direct HTTP
- [ ] Add `OFFLINE_MODE=true` to `.env` as the canonical flag
- [ ] `mcp/llama/tools/ai-orchestrator` must use local-only paths, no external runners

### 5. Repo Registry — kanban-pmo knows about all 21 repos

- [ ] Enumerate all repos under `~/` and populate `config/repos.yml`
- [ ] Each repo entry: `name`, `local_path`, `remote_url`, `default_branch`,
  `env_template`, `gitignore_profile`, `status` (active|archived|offline-only)
- [ ] kanban-pmo governs dev/staging split:
  - `dev` — local working state
  - `staging` — reviewed, tested, push-ready
  - `prod` — pushed to remote, tagged

---

## Acceptance Criteria

- [ ] Zero `.github/workflows/` YMLs in any active repo (pipelines live in `old-archive/` only)
- [ ] `config/repos.yml` exists in kanban-pmo with all 21+ repos registered
- [ ] `proto/kanban.proto` defines at minimum: RepoRegistry, FileWrite, IssueEvent, ProbeSync
- [ ] gRPC server starts cleanly: `python -m kanban.server.grpc_server`
- [ ] persist-memory-probe `repo_tracker.py` emits at least one valid repo event
- [ ] ollama-local `.env` has `OFFLINE_MODE=true`
- [ ] All 3 repos have `old-archive/session-2026-02-19/pipelines/` with archived YMLs

---

## Archived Pipelines (reference)

| Repo | File | Archived To |
|------|------|-------------|
| kanban-pmo | card-close.yml | old-archive/session-2026-02-19/pipelines/ |
| kanban-pmo | card-create.yml | old-archive/session-2026-02-19/pipelines/ |
| kanban-pmo | card-move.yml | old-archive/session-2026-02-19/pipelines/ |
| kanban-pmo | ci.yml | old-archive/session-2026-02-19/pipelines/ |
| kanban-pmo | cred-audit.yml | old-archive/session-2026-02-19/pipelines/ |
| kanban-pmo | doc-sync.yml | old-archive/session-2026-02-19/pipelines/ |
| kanban-pmo | model-build.yml | old-archive/session-2026-02-19/pipelines/ |
| kanban-pmo | sprint-plan.yml | old-archive/session-2026-02-19/pipelines/ |
| kanban-pmo | sprint-retro.yml | old-archive/session-2026-02-19/pipelines/ |
| kanban-pmo | verify-run.yml | old-archive/session-2026-02-19/pipelines/ |
| ollama-local | ci.yml | old-archive/session-2026-02-19/pipelines/ |
| ollama-local | docker.yml | old-archive/session-2026-02-19/pipelines/ |
| persist-memory-probe | ci.yml | old-archive/session-2026-02-19/pipelines/ |
| persist-memory-probe | docker-build.yml | old-archive/session-2026-02-19/pipelines/ |

---

## Notes

- This is the **architectural gate** before any other cross-repo feature is built
- The 37 SLMs mentioned by user are not accepted until this governance layer is proven
- kanban-pmo must be able to onboard a new repo with a single `governor.add_repo()` call
- No cron. No curl. No bash pipelines pretending to be CI. gRPC or nothing.

---

*Card created: 2026-02-19 | Author: tmdev012 | Priority: HIGH — architectural prerequisite*
