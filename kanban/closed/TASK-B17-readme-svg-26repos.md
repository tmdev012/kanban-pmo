# TASK-B17: README SVG Cleanup — 26 Repos

**Column:** Backlog
**Sprint:** S04 (2026-03-15 → 2026-03-21)
**Priority:** P3 — batch operation

## Goal
Fix outdated SVG code in all 26 repo README files. All repos share identical structure.
Replace raw SVG tags with shield.io badges and mermaid architecture diagrams.

## Acceptance Criteria
- [ ] `~/ollama-local/scripts/fix-readme-svg.sh` created and tested
- [ ] All 26 README.md files have no raw `<svg>` tags
- [ ] Architecture diagrams use mermaid fenced code blocks
- [ ] Badges use shields.io markdown format `![badge](https://img.shields.io/...)`
- [ ] Each repo committed via smartpush with message "docs(readme): replace SVG with mermaid/shields"

## Approach
- Script reads repos.yml, iterates all 26 repos
- Detects SVG patterns: `<svg`, `<!-- svg-start -->`, raw base64 SVG
- Replaces with markdown equivalents
- Commits per-repo via smartpush

## Status: PENDING
