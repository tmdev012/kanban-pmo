# TASK-W01: Signature ASCII Banner — 15-Line Shared Function

- **Status:** closed
- **Labels:** banner, sashi, priority:high
- **Assignee:** tmdev012
- **Sprint:** S00 (pre-season)
- **Time:** 30m
- **Milestone:** S01 — v3.2.0 Ship
- **Created:** 2026-02-17

## Description

Create shared 15-line ASCII art banner function in `~/ollama-local/lib/sh/banner.sh`. Unicode box-drawing + block chars. "SASHI v3.2.0" in large block letters. Sourced by ai-orchestrator, sashi, and aliases.sh.

## Acceptance Criteria

- [ ] `~/ollama-local/lib/sh/banner.sh` created
- [ ] `sashi_banner` function renders 15 lines, ~78 cols
- [ ] Colors: cyan art, green version, dim frame
- [ ] Sourced by ai-orchestrator
- [ ] Sourced by sashi CLI
- [ ] Sourced by aliases.sh mcp-help()

## Files

- `~/ollama-local/lib/sh/banner.sh` (CREATE)
- `~/ollama-local/mcp/llama/tools/ai-orchestrator` (UPDATE)
- `~/ollama-local/sashi` (UPDATE)
- `~/ollama-local/lib/sh/aliases.sh` (UPDATE)

---

*Card created: 2026-02-17*
