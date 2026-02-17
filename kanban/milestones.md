# Milestones — FY2026-27 (March 2026 – February 2027)

> 52-week financial year. 1-week sprints. Tools shape time. Ship weekly or explain why.

---

## Q1: Foundation & Hardening (Mar 1 – May 31, 2026)

| Sprint | Week | Dates | Milestone | Deliverable |
|--------|------|-------|-----------|-------------|
| S01 | W01 | Mar 02 – Mar 08 | **v3.1.0 Ship** | Banner, probe integration, kanban CLI, 8B model |
| S02 | W02 | Mar 09 – Mar 15 | **Test Scaffold** | pytest structure, sashi smoke tests |
| S03 | W03 | Mar 16 – Mar 22 | **Unit Tests: Core** | sashi CLI commands, ollama run wrapper |
| S04 | W04 | Mar 23 – Mar 29 | **Unit Tests: Orchestrator** | ai-orchestrator modes, flag parsing |
| S05 | W05 | Mar 30 – Apr 05 | **OpenRouter Key** | Online fallback live, rate limiting |
| S06 | W06 | Apr 06 – Apr 12 | **Online Routing** | Smart model selection (local vs online) |
| S07 | W07 | Apr 13 – Apr 19 | **Training Export** | JSONL pipeline from history.db |
| S08 | W08 | Apr 20 – Apr 26 | **Modelfile Iteration** | Eval harness, prompt tuning |
| S09 | W09 | Apr 27 – May 03 | **Probe Credentials** | GitHub PAT rotation automation |
| S10 | W10 | May 04 – May 10 | **Credential Audit** | Dashboard, expiry alerts |
| S11 | W11 | May 11 – May 17 | **Kanban Export** | CSV/JSON board export |
| S12 | W12 | May 18 – May 24 | **Sprint Velocity** | Auto-calculated velocity per sprint |
| S13 | W13 | May 25 – May 31 | **Q1 Retro** | Burndown review, scope Q2 |

## Q2: Intelligence & Automation (Jun 1 – Aug 31, 2026)

| Sprint | Week | Dates | Milestone | Deliverable |
|--------|------|-------|-----------|-------------|
| S14 | W14 | Jun 01 – Jun 07 | **Multi-Model Router** | Hot-swap 3B/8B per query complexity |
| S15 | W15 | Jun 08 – Jun 14 | **Online Fallback** | Auto-escalate to OpenRouter on timeout |
| S16 | W16 | Jun 15 – Jun 21 | **Embedding Search** | Vector similarity over history.db |
| S17 | W17 | Jun 22 – Jun 28 | **RAG Pipeline** | Context retrieval for prompts |
| S18 | W18 | Jun 29 – Jul 05 | **Smart Push v2** | Auto-changelog from commits |
| S19 | W19 | Jul 06 – Jul 12 | **PR Draft** | AI-generated PR descriptions |
| S20 | W20 | Jul 13 – Jul 19 | **gRPC Proto** | Service definitions, proto files |
| S21 | W21 | Jul 20 – Jul 26 | **gRPC Bridge** | ollama-local ↔ kanban-pmo comm |
| S22 | W22 | Jul 27 – Aug 02 | **SmartDoc Core** | Tech doc generation from git log |
| S23 | W23 | Aug 03 – Aug 09 | **SmartDoc Templates** | QM, sprint report, release notes |
| S24 | W24 | Aug 10 – Aug 16 | **Termux Sync** | Bidirectional mobile ↔ desktop |
| S25 | W25 | Aug 17 – Aug 23 | **Termux Polish** | Conflict resolution, selective sync |
| S26 | W26 | Aug 24 – Aug 31 | **Q2 Retro / Mid-Year** | Half-year review, reforecast |

## Q3: Scale & Polish (Sep 1 – Nov 30, 2026)

| Sprint | Week | Dates | Milestone | Deliverable |
|--------|------|-------|-----------|-------------|
| S27 | W27 | Sep 01 – Sep 07 | **TUI Dashboard** | Terminal board view, model stats |
| S28 | W28 | Sep 08 – Sep 14 | **TUI Velocity** | Live sprint velocity widget |
| S29 | W29 | Sep 15 – Sep 21 | **Plugin Arch** | Extensible sashi command loader |
| S30 | W30 | Sep 22 – Sep 28 | **Plugin: Git** | git-aware context injection |
| S31 | W31 | Sep 29 – Oct 05 | **CI: Lint** | shellcheck + pytest in GitHub Actions |
| S32 | W32 | Oct 06 – Oct 12 | **CI: Build** | Docker build + push on tag |
| S33 | W33 | Oct 13 – Oct 19 | **Voice: STT** | Whisper speech-to-text input |
| S34 | W34 | Oct 20 – Oct 26 | **Voice: Pipeline** | STT → llama → TTS end-to-end |
| S35 | W35 | Oct 27 – Nov 02 | **Security: Scan** | Credential leak detection |
| S36 | W36 | Nov 03 – Nov 09 | **Security: Rotate** | Automated key rotation |
| S37 | W37 | Nov 10 – Nov 16 | **Perf: Cache** | Query result caching layer |
| S38 | W38 | Nov 17 – Nov 23 | **Perf: Preload** | Model preload on shell init |
| S39 | W39 | Nov 24 – Nov 30 | **Q3 Retro** | Review, burndown, scope Q4 |

## Q4: Production & Governance (Dec 1, 2026 – Feb 28, 2027)

| Sprint | Week | Dates | Milestone | Deliverable |
|--------|------|-------|-----------|-------------|
| S40 | W40 | Dec 01 – Dec 07 | **v4.0.0 Alpha** | Feature freeze, integration tests |
| S41 | W41 | Dec 08 – Dec 14 | **Integration Tests** | Cross-repo test suite green |
| S42 | W42 | Dec 15 – Dec 21 | **Man Pages** | `man sashi`, `man ai-orchestrator` |
| S43 | W43 | Dec 22 – Dec 28 | **Architecture Docs** | SVG diagrams, data flow maps |
| S44 | W44 | Dec 29 – Jan 04 | **Docker Compose** | Full stack, health checks |
| S45 | W45 | Jan 05 – Jan 11 | **Docker Prod** | Restart policies, resource limits |
| S46 | W46 | Jan 12 – Jan 18 | **Logging** | Structured logs, rotation |
| S47 | W47 | Jan 19 – Jan 25 | **Metrics** | Local Prometheus (optional) |
| S48 | W48 | Jan 26 – Feb 01 | **Edge Cases** | Error handling sweep |
| S49 | W49 | Feb 02 – Feb 08 | **Graceful Degradation** | Offline mode, fallback chains |
| S50 | W50 | Feb 09 – Feb 15 | **v4.0.0 RC** | Release candidate, changelog |
| S51 | W51 | Feb 16 – Feb 22 | **v4.0.0 Release** | Tag, GitHub release, announcement |
| S52 | W52 | Feb 23 – Feb 28 | **FY Retro** | Year review, FY2027-28 planning |

---

## Sprint Cadence (1-week)

```
Mon:    Plan — scope cards, pull from backlog → WIP
Tue-Thu: Build — implement, test, iterate
Fri AM: Ship — merge, verify, close cards
Fri PM: Retro — velocity check, next sprint prep
```

## Velocity Tracking

| Metric | Target | Measurement |
|--------|--------|-------------|
| Cards closed/sprint | 2-4 | `ls kanban/closed/ \| wc -l` delta per sprint |
| Commits/sprint | 5-10 | `git log --since="1 week ago" --oneline \| wc -l` |
| Model accuracy | Improving | Manual eval 5 prompts/sprint |
| Test coverage | >60% by S13 | `pytest --cov` |
| Response time (3B) | <5s | `time ollama run fast-sashi "test"` |
| Response time (8B) | <15s | `time ollama run sashi-llama-8b "test"` |
| Sprint completion | >80% | closed / (wip + open) at sprint end |

## Current Sprint

**Sprint:** S00 (Pre-season — v3.1.0 build)
**Window:** Feb 17, 2026 → Feb 28, 2026
**Status:** WIP
**Goal:** Ship v3.1.0, populate kanban, commit baseline

---

*Created: 2026-02-17 | FY: 2026-27 | Author: tmdev012*
