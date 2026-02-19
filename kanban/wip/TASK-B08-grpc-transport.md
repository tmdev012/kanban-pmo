# TASK-B08: gRPC Transport Layer — kanban-pmo Service Interface

- **Status:** wip
- **Labels:** grpc, infra, priority:high
- **Parent:** TASK-B06 (T2 of 5)
- **Assignee:** tmdev012
- **Sprint:** S01
- **Time:** 1.5h (estimated)
- **Milestone:** S01 — Governance Prerequisite
- **Created:** 2026-02-19

## Description

Define the gRPC service contracts for kanban-pmo's governance layer.
The proto schema covers repo registry queries, authorised file writes,
issue event streaming, and persist-memory-probe sync operations.

## Deliverables

- [x] `proto/kanban.proto` — service definitions: RepoRegistry, FileWrite, IssueEvent, ProbeSync
- [x] `server/grpc_server.py` — servicer implementations wrapping governor layer
- [ ] `generated/` — compiled Python stubs (kanban_pb2.py, kanban_pb2_grpc.py)

## Acceptance Criteria

- [ ] `python -m grpc_tools.protoc` compiles `proto/kanban.proto` without errors
- [ ] `grpc_server.ListRepos()` returns registry entries matching governor.list_repos()
- [ ] `grpc_server.WriteFile()` delegates to governor.write_file() with auth check
- [ ] stub files present in `generated/` after protoc run

---

*Card created: 2026-02-19 | Sub-task: B06-T2*
