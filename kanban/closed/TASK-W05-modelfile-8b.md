# TASK-W05: Modelfile.8b + Build sashi-llama-8b

- **Status:** closed
- **Labels:** model, sashi, priority:med
- **Assignee:** tmdev012
- **Sprint:** S00 (pre-season)
- **Time:** 15m
- **Milestone:** S01 — v3.2.0 Ship
- **Created:** 2026-02-17

## Description

Create Modelfile.8b with same v3.2.0 system prompt as Modelfile.fast but targeting llama3.1:8b. Build model via ollama create.

## Acceptance Criteria

- [ ] `~/ollama-local/Modelfile.8b` created
- [ ] FROM llama3.1:8b
- [ ] num_ctx 4096, num_predict 1024, num_thread 2, temperature 0.7
- [ ] `ollama create sashi-llama-8b -f Modelfile.8b` succeeds

## Files

- `~/ollama-local/Modelfile.8b` (CREATE)

---

*Card created: 2026-02-17*
