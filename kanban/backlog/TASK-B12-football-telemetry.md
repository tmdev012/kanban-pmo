# TASK-B12: football-telemetry — PMO Onboarding & Integration

- **Status:** backlog
- **Labels:** domain-project, telemetry, docker, fastapi, react, priority:medium
- **Assignee:** tmdev012
- **Sprint:** S02
- **Time:** 2h
- **Milestone:** S02 — Repo Consolidation
- **Created:** 2026-02-23

## Description

New repo `football-telemetry` has been pushed to GitHub. Wire it into the PMO ecosystem.

**Remote:** `git@github.com:tmdev012/football-telemetry.git`
**Local:** `/home/tmdev012/football-telemetry`
**Stack:** FastAPI + React + Docker + nginx + MCP

## Acceptance Criteria

- [ ] `.env` created from `.env.example` with valid API keys (football API key)
- [ ] Docker Compose stack boots cleanly (`make up` or `docker compose up`)
- [ ] Frontend accessible at `http://localhost:5173`
- [ ] Backend API docs at `http://localhost:8000/docs`
- [ ] Wired into `sashi probe` — tracked in `probe.db`
- [ ] `integrate.py` picks up `football-telemetry` in repo scan
- [ ] MCP tools registered and callable from `sashi`
- [ ] Added to `kanban-pmo/config/repos.yml` ✅ (done 2026-02-23)

## Notes

- Repo was local-only (no commits, no remote) until 2026-02-23 — now live on GitHub
- Stack mirrors `ollama-telemetry` pattern — check that repo for reference
- `src/Api/football_client.py` — check which external API is used (API-Football / RapidAPI)
