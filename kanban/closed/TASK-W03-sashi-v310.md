# TASK-W03: Sashi CLI v3.2.0 — Kanban, Write, Banner

- **Status:** closed
- **Labels:** sashi, priority:high
- **Assignee:** tmdev012
- **Sprint:** S00 (pre-season)
- **Time:** 45m
- **Milestone:** S01 — v3.2.0 Ship
- **Created:** 2026-02-17

## Description

Update sashi CLI: version bump to 3.2.0, source shared banner, add kanban subcommand (board/state/columns), add write subcommand, update help text.

## Acceptance Criteria

- [x] VERSION="3.1.0"
- [x] Sources banner.sh, calls sashi_banner in help/status/chat
- [x] `sashi kanban board` — column counts
- [x] `sashi kanban state` — full state (files + DB)
- [x] `sashi kanban backlog|open|wip|closed` — list cards
- [x] `sashi write <file> <prompt>` — runs llama, writes output
- [x] Help text updated with kanban + write

## Files

- `~/ollama-local/sashi` (UPDATE)

---

*Card created: 2026-02-17*
