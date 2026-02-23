# TASK-B11: Runner Execution Layer — Subprocess & gRPC Dispatch

- **Status:** backlog
- **Labels:** infra, runners, grpc, priority:high
- **Assignee:** tmdev012
- **Sprint:** S02
- **Time:** 4h (estimated)
- **Milestone:** v3.3.0 — Runner Execution
- **Created:** 2026-02-22
- **Blocked by:** B06 (gRPC governance layer)
- **Blocks:** automated runner execution across repos

---

## Context

B10 (runner taxonomy) established the skill→executor mapping via `config/runners.yml`
and `lib/py/runner_manager.py`. `IssueEventServicer.Emit()` now routes events to
`RunnerManager.dispatch()` which stubs dispatch (logs intent, returns `{queued: True}`).
This card implements actual execution: subprocess for bash/python runners, gRPC channel
for probe runner, and output streaming back through `IssueEvent.Stream()`.

---

## Scope of Work

### 1. Subprocess Runners (executor: bash / python)

For each runner where `executor` is `bash` or `python`:

- Read `cmd` or `module` from runners.yml config
- Resolve full path relative to repo root (from `repos` list → `config/repos.yml`)
- Launch via `subprocess.Popen` with timeout, stdout/stderr capture
- Emit captured lines as `IssueEvent` payloads back through `Stream()`

### 2. gRPC Runner (executor: grpc)

For the `probe` runner (`target: persist-memory-probe:50052`):

- Construct `grpc.insecure_channel(target)`
- Invoke RPC defined by `rpc:` field (e.g. `ProbeSync.SyncRepo`)
- Capture `SyncRepoResponse` and relay as event payload

### 3. Output Capture → Event Stream

Runner stdout/stderr should be emitted back as `IssueEvent` payloads so callers
using `IssueEvent.Stream()` can observe execution results in near-realtime.

### 4. Error Handling

- Timeout: configurable per runner (default 60s). Emit timeout event on breach.
- Non-zero exit: set `ok=False`, include stderr in event payload
- Missing cmd/module: log warning + skip (do not crash the gRPC server)
- gRPC channel failure: retry once, then emit error event

---

## Deliverables

- [ ] `RunnerManager.dispatch()` executes actual subprocess for bash/python runners
- [ ] `RunnerManager.dispatch()` constructs gRPC channel for probe runner
- [ ] Execution stdout/stderr emitted as `IssueEvent` stream entries
- [ ] Timeout enforced (60s default, per-runner override in runners.yml)
- [ ] All 8 runners execute without crashing the gRPC server

---

## Acceptance Criteria

- [ ] `sashi grpc start && python -c "emit TEST-01 created kanban-pmo"` → `[runner] board queued`
- [ ] Board runner subprocess actually runs a stub script and returns exit 0
- [ ] Probe runner successfully calls persist-memory-probe :50052 SyncRepo
- [ ] Stream() yields runner output lines as events after dispatch

---

*Card created: 2026-02-22 | Author: tmdev012 | Priority: HIGH — runner execution prerequisite*
