# TASK-B20: Restore Archived Pipelines (since 2026-02-08)

- **Status:** closed
- **Closed:** 2026-03-01
- **Sprint:** S02

## Done
- .github/workflows/ci.yml — ShellCheck + Python lint + sashi syntax
- .github/workflows/docker.yml — Docker build/compose validation
- mcp/llama/tools/ai-code — code assistant (phi3:mini → llama3.2)
- mcp/llama/tools/ai-fast — fast query (phi3:mini → llama3.2)
- scripts/ollama-chat.sh — interactive ollama wrapper
- lib/sh/env-guard.sh — CMMI4 pre-commit secret blocker
- lib/sh/git-autonomous.sh — autonomous repo create pipeline
- lib/py/sashi_db.py — consolidated SQLite module (bridge/file/sync/cred)
