# Kanban-PMO Manifesto

> Documentation is not a description of the system. It IS the system.

---

## Core Principles

### 1. Documentation Runs

If it doesn't execute, constrain, or govern — it's not documentation, it's a journal entry. Every document in this framework either:

- **Configures runtime behavior** (Modelfile system prompts, .env files)
- **Defines governance boundaries** (BDPM swimlanes, workflow policies)
- **Tracks verifiable state** (kanban cards, milestone gates, VER test cases)
- **Encodes decisions** (architecture diagrams, schema definitions)

A README that drifts from reality is worse than no README. A Modelfile that drifts from reality breaks the model. We prefer the second kind — documentation that fails loudly when it lies.

### 2. Schema Before Code

Derived from the IIE DBMS exam format: three questions that, when combined, produce a complete database schema with prerequisite constraints, edge cases, and expected outputs. The schema IS the program. If the schema is correct, the implementation is mechanical. If the schema is wrong, no amount of clean code saves you.

Applied here:

- SQLite schema defines what the system can know
- Kanban directory structure defines what states work can be in
- BDPM swimlanes define which layer owns which responsibility
- Modelfile system prompt defines what the AI can reason about

None of these are code. All of them determine what the code does.

### 3. Index Everything

An unindexed database works. An indexed database works 1000x faster. The same principle applies to every layer:

| Layer | Unindexed | Indexed | Effect |
|-------|-----------|---------|--------|
| Database | Full table scan | B-tree lookup | 50ms context retrieval vs 2-5 seconds |
| Filesystem | Flat directory | `kanban/wip/TASK-W04.md` | Path IS the query |
| Architecture | Tribal knowledge | BDPM swimlane diagram | One glance = full understanding |
| AI context | Vague system prompt | Schema-informed Modelfile | Model stops hallucinating |

Indexing is pre-computing the answer to "where is it?" so runtime never has to search. Every document, every directory name, every diagram is an index.

### 4. Policies Over Implementation

Code can be rewritten. People leave. Products get copied. Policies survive all three.

The BDPM governance model answers questions before they get asked:

- **Where does new work start?** → Business swimlane, kanban intake
- **Who owns the build?** → Development swimlane, git + smart-push
- **Who owns the deploy?** → Production swimlane, gRPC pipeline
- **How do we know it's working?** → Monitoring swimlane, health check + compliance
- **What triggers what?** → Cross-lane arrows (card-create → git, smart-push → gRPC, DB log → audit, compliance → velocity review)

Without policy, three developers on the same codebase make three different decisions about where to put things. With policy, they all put things in the same place without asking. That's the moat.

### 5. Traceability Is Non-Negotiable

Good intentions without traceability are indistinguishable from no intentions at all. An audit cannot tell the difference because there is nothing to audit.

Every decision in this framework is traceable:

- **Kanban cards** → who moved what, when, why
- **Git commits** → smart-push logs to SQLite with categories, line counts, version tags
- **Credential operations** → logged to credential_audit table
- **AI queries** → logged with model, prompt, response length, duration
- **Architecture changes** → documented in diagrams before implemented in code

The gap between "we followed the process" and "we can prove we followed the process" is the gap between a functioning team and a team that appears to function.

### 6. Build-Time Write, Runtime Read

The Modelfile is compiled once (`ollama create`). Every query reads it as immutable context. The SQLite schema is defined once. Every query reads indexed rows. The BDPM diagram is drawn once. Every architectural decision references it.

This is the immutable array principle: write at build time, read-only at runtime. Fewer write surfaces = fewer race conditions = O(1) reasoning about state.

Applied to documentation: documents are build artifacts. They are authored deliberately, reviewed against reality, and consumed as read-only references. A document that changes every sprint is a log. A document that holds stable across sprints is a policy.

### 7. Single Source of Truth

One database (`history.db`) shared by three repos via symlink. One orchestrator (`ai-orchestrator`) with all paths pointing to it. One Modelfile per model profile. One kanban board per project.

Duplication is entropy. Every copy is a potential lie. Symlinks, not copies. Delegation, not reimplementation. If two files say the same thing, delete one and point to the other.

---

## The BDPM Model

**B**usiness · **D**evelopment · **P**roduction · **M**onitoring

Four layers. Four owners. Four swimlanes. Cross-lane arrows define event triggers.

See: [`docs/diagrams/bdpm-swimlanes.svg`](diagrams/bdpm-swimlanes.svg)

This is not an aspiration. It is a description of how the three-repo ecosystem (`ollama-local`, `kanban-pmo`, `persist-memory-probe`) currently operates. The diagram was drawn after the system was built, not before — making it a validation artifact, not a planning artifact.

---

## Intellectual Lineage

| Source | Contribution |
|--------|-------------|
| **IIE DBMS exam format** | Schema-first thinking: 3 questions → complete schema with constraints and expected outputs |
| **Edwin Seibel's file handling** | Filesystem as data structure: sequential, indexed, relative files as the foundation before databases existed |
| **Agile/Kanban** | Work-in-progress limits, pull-based flow, board as single source of project state |
| **CMMI** | Maturity levels as governance milestones, not bureaucratic overhead |
| **Content-addressable storage** | Immutable, hash-based, O(1) lookup — the principle behind git, and behind our build-time/runtime separation |
| **MCP (Model Context Protocol)** | Protocols scaffolded on filesystem containers — the model originates from file handling principles |

---

## Anti-Patterns We Reject

| Anti-Pattern | Why It Fails | Our Alternative |
|-------------|-------------|-----------------|
| Documentation as afterthought | Drifts from reality, nobody trusts it, nobody reads it | Documentation that executes or governs |
| Copy-paste deployment | Every copy diverges, creates ghost state | Symlinks and single-source delegation |
| Tribal knowledge | Leaves when people leave, invisible to auditors | Schema + policy + traceable decisions |
| Test-only validation | Proves code runs, doesn't prove architecture is correct | Documentation-driven validation: if the diagram is wrong, the system is wrong |
| AI-generated boilerplate | MVC scaffolding anyone can produce | Policy frameworks that determine what gets built and why |

---

## Versioning

| Version | Date | Milestone |
|---------|------|-----------|
| v3.1.0 | 2026-02-17 | Three-repo integration, BDPM governance, 43-file commit, kanban board live |

---

*Kanban-PMO Manifesto · 2026-02-17 · Framework ownership over implementation delegation*
