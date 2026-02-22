# TASK-W02: Probe gatekeeper_3_1_0 — Credential Gateway + Inference Delegation

- **Status:** closed
- **Labels:** probe, sashi, priority:high
- **Assignee:** tmdev012
- **Sprint:** S00 (pre-season)
- **Time:** 45m
- **Milestone:** S01 — v3.2.0 Ship
- **Created:** 2026-02-17

## Description

Rewrite `~/persist-memory-probe/lib/sh/gatekeeper_3_1_0.sh` (formerly ai-orchestrator.sh) to delegate inference to ollama-local's canonical orchestrator while keeping unique credential-routing functions (github/sign/remote).

## Architecture

```
gatekeeper_3_1_0.sh (credential layer)
  ├── github, sign, remote     → probe-specific (kept)
  ├── ollama, kanban, ask      → delegates to ollama-local/ai-orchestrator
  ├── train                    → calls probe's train_credentials.py
  └── log_credential_usage()   → writes to credential_audit table
```

## Acceptance Criteria

- [x] Renamed from ai-orchestrator.sh → gatekeeper_3_1_0.sh
- [x] VERSION="3.1.0"
- [x] Sources shared banner.sh
- [x] cmd_ollama() delegates to canonical ai-orchestrator (fast `ollama run`)
- [x] cmd_github(), cmd_sign(), cmd_remote() preserved
- [x] log_credential_usage() preserved
- [x] cmd_kanban() added — delegates with --kanban
- [x] cmd_train() added — calls train_credentials.py
- [x] --status shows credential status + system status

## Files

- `~/persist-memory-probe/lib/sh/gatekeeper_3_1_0.sh` (REWRITE)

---

*Card created: 2026-02-17*
