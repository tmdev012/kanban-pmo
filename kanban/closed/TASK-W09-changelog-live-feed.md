# TASK-W09: CHANGELOG as Live Data Feed

- **Status:** closed
- **Labels:** docs, infra, data-feed, priority:high
- **Assignee:** tmdev012
- **Sprint:** S01 (2026-02-22)
- **Milestone:** S01 — v3.3.0 Ship
- **Closed:** 2026-02-22
- **Effort:** ~20m

## Description

Replace scattered version notes with a single canonical `CHANGELOG.md` in ollama-local. Symlink to Desktop so it's always visible. Inject latest entry into both Modelfile.fast and Modelfile.8b as `## Latest Changes` section. Add `sashi changelog` command. Show latest entry in `sashi status`. Create `scripts/rebuild-models.sh` that auto-injects changelog before `ollama create`.

## Acceptance Criteria

- [x] `~/ollama-local/CHANGELOG.md` — canonical single source of truth
- [x] `~/Desktop/SASHI-CHANGELOG.md` → symlink to CHANGELOG.md
- [x] `Modelfile.fast` has `## Latest Changes — v3.2.0` section
- [x] `Modelfile.8b` has `## Latest Changes — v3.2.0` section
- [x] `sashi changelog` prints full CHANGELOG.md
- [x] `sashi status` shows latest entry (15 lines via awk)
- [x] `scripts/rebuild-models.sh` — injects changelog, runs ollama create for both models

## Solution

### Single source, always fresh
```bash
# One file, always current
~/ollama-local/CHANGELOG.md

# Desktop symlink — never copy again
ln -sf ~/ollama-local/CHANGELOG.md ~/Desktop/SASHI-CHANGELOG.md

# Both models read same entry at build time
## Latest Changes — v3.2.0 (2026-02-22)   ← injected into BOTH Modelfiles
```

### sashi status shows it live
```bash
# awk extracts first ## v block, stops at second
awk '/^## v/{found++} found==1{print "  "$0} found==2{exit}' CHANGELOG.md | head -15
```

### Rebuild script wires it all
```bash
bash ~/ollama-local/scripts/rebuild-models.sh
# → injects latest changelog into Modelfile.fast + Modelfile.8b
# → runs: ollama create fast-sashi + ollama create sashi-llama-8b
```

### Reproducibility
```bash
sashi changelog          # full CHANGELOG
sashi status             # shows "Latest Changes:" section at bottom
ls -la ~/Desktop/SASHI-CHANGELOG.md   # confirms symlink
```

## Commits
- `ollama-local 7270dee` — chore: bump all version strings → v3.2.0
- `ollama-local [unstaged]` — CHANGELOG.md, Modelfile.fast, Modelfile.8b, sashi, rebuild-models.sh

## Files
- `~/ollama-local/CHANGELOG.md` (CREATE — canonical)
- `~/Desktop/SASHI-CHANGELOG.md` (SYMLINK)
- `~/ollama-local/Modelfile.fast` (MODIFIED — Latest Changes section)
- `~/ollama-local/Modelfile.8b` (MODIFIED — Latest Changes section)
- `~/ollama-local/sashi` (MODIFIED — changelog cmd + status display)
- `~/ollama-local/scripts/rebuild-models.sh` (CREATE)

---
*Closed: 2026-02-22 | Sprint S01 | v3.3.0*
