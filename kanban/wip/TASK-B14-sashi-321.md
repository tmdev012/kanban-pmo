# TASK-B14: Sashi v3.2.1 Integration

**Column:** WIP
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
- [ ] `ollama create sashi-llama-fast -f Modelfile.fast` — rebuild model
- [ ] `sashi status` shows v3.2.1 + USB + WiFi ADB status lines
- [x] lib/sh/aliases.sh has HF alias: shf='sashi hf'
- [x] .env has HF_TOKEN and HF_MODEL entries

## Deliverables
- `~/ollama-local/sashi` v3.2.1
- `~/ollama-local/Modelfile.fast` updated
- `~/ollama-local/.env` — HF_TOKEN + HF_MODEL added

## Status: IN PROGRESS
Code done, model rebuild pending (ollama create sashi-llama-fast)
