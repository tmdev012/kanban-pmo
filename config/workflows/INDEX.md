# Workflow Configuration Index

> Training document for ai-orchestrator, sashi, gatekeeper. Source: `workflows.ini`.

## Architecture
- **One file**: `workflows.ini` — single parent, 12 workflows
- **Multi-ternary**: fields = `true|false|inherit`. Omitted = inherit from `[defaults]`
- **CSV input**: `workflows.csv` for bulk edit
- **JSON output**: `dispatch.sh` for scripts/Actions
- **Versioned**: `[meta] revision` bumps on edit, git tracks history
- **Prefix<->suffix**: `[card.close]` = composable workflow ID

## Schema
| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| enabled | true/false/inherit | true | Active? |
| trigger | push/schedule/dispatch/pr | push | What fires it |
| paths | glob list | — | File patterns |
| schedule | cron | — | Cron (if schedule) |
| cache | none/sprint/session | none | TTL strategy |
| lock | true/false/inherit | false | Lock files? |
| revert | none/last/tag:X | none | Revert strategy |
| gitignore | glob list | — | Exclude patterns |
| audit | true/false/inherit | true | Log to audit? |
| payload | key:val list | — | Custom data |

## Registry (12 workflows)
| ID | Trigger | On | Description |
|----|---------|-----|-------------|
| card.create | push | kanban/*/TASK-*.md | Track creation |
| card.close | push | kanban/closed/* | Validate closed |
| card.move | push | kanban/*/TASK-*.md | Track moves |
| sprint.plan | Mon 8am | — | Planning snapshot |
| sprint.retro | Fri 4pm | — | Velocity retro |
| doc.sync | push | *.md | Doc-code sync |
| cred.audit | push,pr | * | Credential scan |
| model.build | push | Modelfile* | Model tracking |
| verify.run | dispatch | — | Run VER tests |
| git.ignore | push | .gitignore | Enforce patterns |
| git.lock | dispatch | — | Patch freeze (off) |
| git.revert | dispatch | — | Revert state (off) |

## Usage
```bash
dispatch.sh list          # JSON: all 12 workflows
dispatch.sh list --csv    # CSV format
dispatch.sh get card.close # Single workflow JSON
dispatch.sh status        # Board counts + workflow states
dispatch.sh enable git.lock # Turn on patch freeze
dispatch.sh disable sprint.retro # Turn off retro
dispatch.sh version       # v3.1.0 rev1
```

*Created: 2026-02-17 | v3.1.0 | tmdev012*
