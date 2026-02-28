# TASK-B18: Modelfile Training + Rebuild

**Column:** Backlog
**Sprint:** S02 (2026-03-01 → 2026-03-07)
**Priority:** P1

## Goal
Rebuild sashi-llama-fast (3B) and sashi-llama-8b (8B) models with updated system prompts
including USB/WiFi context and football-telemetry knowledge.

## Acceptance Criteria
- [ ] `ollama create sashi-llama-fast -f ~/ollama-local/Modelfile.fast`
- [ ] `ollama create sashi-llama-8b -f ~/ollama-local/Modelfile.8b`
- [ ] Modelfile.8b updated with football-telemetry context (FastAPI, React, API-Football v3)
- [ ] `sashi 8b "explain sashi wifi init"` returns correct answer
- [ ] `sashi ask "usb vendor 04e8"` returns "Samsung"
- [ ] 245+ training dialogs in probe.db (export via sashi probe export)

## Status: PENDING — waiting for ollama create to be run
Run: ollama create sashi-llama-fast -f ~/ollama-local/Modelfile.fast
