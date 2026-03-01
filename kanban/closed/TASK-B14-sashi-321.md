# TASK-B14: Sashi v3.2.1 Integration

**Column:** CLOSED
**Sprint:** S02 (2026-03-01 → 2026-03-07)
**Priority:** P1 — ships with B13
**Assigned:** claude-sonnet-4-6

## Goal
Version bump 3.2.0 → 3.2.1 with full USB/WiFi/HuggingFace integration.
Train Modelfile.fast with new context. Rebuild sashi-llama-fast model.

## Acceptance Criteria
- [x] sashi VERSION = 3.2.1
- [x] sashi hf <prompt> works (HuggingFace free tier)
- [x] online/cloud fallback: OpenRouter → HuggingFace
- [x] Modelfile.fast updated with v3.2.1 context + USB/WiFi/HF docs
- [x] `ollama create sashi-llama-fast -f Modelfile.fast` — model rebuilt (2026-03-01)
- [x] CHANGELOG.md v3.2.1 section added
- [x] Modelfile.8b version bumped to 3.2.1
- [x] lib/sh/aliases.sh has HF alias: shf='sashi hf'
- [x] .env has HF_TOKEN and HF_MODEL entries

## Deliverables
- `~/ollama-local/sashi` v3.2.1
- `~/ollama-local/Modelfile.fast` updated
- `~/ollama-local/Modelfile.8b` bumped
- `~/ollama-local/CHANGELOG.md` — v3.2.1 entry added
- `sashi-llama-fast` model rebuilt from Modelfile.fast v4.2

## Status: DONE — 2026-03-01
All criteria met. Commits: 18770e6 (feat) + c360f7b (docs/Modelfile.8b).
