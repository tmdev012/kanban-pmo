# TASK-B15: Football-Telemetry Task 2

**Column:** Backlog
**Sprint:** S04 (2026-03-15 → 2026-03-21)
**Priority:** P2 — blocked by B12 task1 completion
**Depends on:** TASK-B12 (task1), TASK-B13 (USB/WiFi)

## Goal
Add real-time and wireless companion features to football-telemetry after task1 baseline.

## Acceptance Criteria
- [ ] WebSocket streaming for live match score updates
- [ ] WiFi-based mobile companion route (React Native or PWA)
- [ ] `sashi wifi logcat com.football` — tail mobile app logs during match
- [ ] Telemetry events logged to ~/ollama-local/db/history.db
- [ ] sashi probe can sync football-telemetry repo to probe.db

## Notes
- Task 1 (B12): Fix broken routes, complete CRUD, connect MCP tools
- Task 2 (B15): Live score WebSocket + WiFi mobile companion
- Stack: FastAPI :8000 + React/Vite :5173 + API-Football v3 (free: 100 req/day)

## Status: BLOCKED — waiting for B12 task1 completion
