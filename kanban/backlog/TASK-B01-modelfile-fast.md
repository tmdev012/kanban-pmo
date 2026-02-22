# TASK-B01: Modelfile.fast — Full System Prompt

- **Status:** backlog
- **Labels:** model, sashi, priority:high
- **Assignee:** tmdev012
- **Sprint:** S00 (pre-season)
- **Time:** 30m (completed)
- **Milestone:** S01 — v3.2.0 Ship
- **Created:** 2026-02-17

## Description

Built `Modelfile.fast` with 120+ line system prompt containing full 3-repo context (ollama-local, kanban-pmo, persist-memory-probe). Rebuilt `fast-sashi` model via `ollama create`.

## Acceptance Criteria

- [x] Modelfile.fast written with v3.2.0 system prompt
- [x] `ollama create fast-sashi -f Modelfile.fast` succeeds
- [ ] Documented in CHANGELOG.md
- [ ] Verified: `ollama run fast-sashi "what version?"` → v3.2.0

## Files

- `~/ollama-local/Modelfile.fast`

---

*Card created: 2026-02-17*
