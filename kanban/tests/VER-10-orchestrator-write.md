# VER-10: ai-orchestrator --write Creates File
- **Type:** verification | **Labels:** verify, sashi | **Sprint:** S00 | **Blocks:** W04
## Test
```bash
ai-orchestrator --write /tmp/test-orch-write.txt "hello"
```
## Expected
File created at /tmp/test-orch-write.txt.
---
*Created: 2026-02-17*
