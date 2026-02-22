# TASK-W04: Integrate Shared Banner into Orchestrator + Aliases

- **Status:** closed
- **Labels:** banner, sashi, priority:high
- **Assignee:** tmdev012
- **Sprint:** S00 (pre-season)
- **Time:** 15m
- **Milestone:** S01 — v3.2.0 Ship
- **Created:** 2026-02-17

## Description

Update ai-orchestrator to source shared banner.sh and replace inline ASCII art. Update aliases.sh mcp-help() to source and call sashi_banner.

## Acceptance Criteria

- [x] ai-orchestrator sources banner.sh
- [x] ai-orchestrator inline banner replaced with sashi_banner call
- [x] aliases.sh mcp-help() sources banner.sh
- [x] aliases.sh mcp-help() calls sashi_banner

## Files

- `~/ollama-local/mcp/llama/tools/ai-orchestrator` (UPDATE)
- `~/ollama-local/lib/sh/aliases.sh` (UPDATE)

---

*Card created: 2026-02-17*
