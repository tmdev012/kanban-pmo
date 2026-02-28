# TASK-B16: HuggingFace Online Model Integration

**Column:** Backlog
**Sprint:** S03 (2026-03-08 → 2026-03-14)
**Priority:** P2

## Goal
Full HuggingFace integration as secondary online model behind OpenRouter.

## Acceptance Criteria
- [x] `sashi hf <prompt>` routes to HuggingFace Inference API
- [x] Fallback chain: OpenRouter → HuggingFace (when OPENROUTER_API_KEY absent)
- [x] HF_TOKEN + HF_MODEL in .env template
- [ ] Add HF model list: `sashi models hf` shows available free HF models
- [ ] Log HF queries to history.db with model tag "huggingface:*"
- [ ] Update Modelfile.fast when HF token is set (note it in system prompt)

## Notes
- Free tier: ~5 req/min without token, ~30 req/min with HF_TOKEN
- Best free model: meta-llama/Llama-3.2-3B-Instruct (matches local 3B)
- Fallback order: local → OpenRouter → HuggingFace → error

## Status: PARTIALLY DONE — sashi hf works, model list and logging pending
