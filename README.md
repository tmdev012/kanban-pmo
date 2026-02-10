# Gazette Support MCP Framework

> Python-based multi-repo framework with gRPC communication, Ollama/Llama integration, Docker orchestration, and SQLite persistence. Designed for arm64v8/Termux mobile testing environments.

[![Python](https://img.shields.io/badge/python-3.10+-blue)]()
[![gRPC](https://img.shields.io/badge/gRPC-enabled-green)]()
[![Docker](https://img.shields.io/badge/docker-compose-blue)]()
[![SQLite](https://img.shields.io/badge/sqlite-persistence-orange)]()

---

## Architecture

![Gazette Architecture](docs/diagrams/gazette-architecture.svg)

---

## Features

| Component | Description | Status |
|-----------|-------------|--------|
| **CLI** | `gazette` command replacing bash aliases | Backlog |
| **API** | FastAPI with rate limiting | Backlog |
| **PAT** | Personal Access Token management | Backlog |
| **SmartDoc** | Document generation with anonymization | Backlog |
| **Kanban** | Task board with CSV/JSON/Docker export | Backlog |
| **gRPC** | Multi-repo communication | Backlog |
| **Training** | Llama 3.2 fine-tuning on terminal dialogs | Backlog |

---

## Quick Start

```bash
# Clone
git clone git@github.com:tmdev012/gazette-support-mcp-framework.git
cd gazette-support-mcp-framework

# Install
pip install -e .

# Or Docker
docker-compose up -d
```

---

## CLI Commands (Planned)

```bash
# AI queries
gazette ask "explain this code"
gazette code "write a sorting function"

# Document generation
gazette doc init "Project Name"
gazette doc tech --from-commits HEAD~5
gazette doc qm --sprint 12

# Git pipeline
gazette push "commit message"
gazette push --version v1.0.0

# Kanban
gazette board show
gazette board add "New task" --priority high
gazette board export --format csv

# Auth
gazette auth add github --name cli-token
gazette auth limits

# Training
gazette training export --format jsonl
gazette training inject --last 50
```

---

## Directory Structure

```
gazette-support-mcp-framework/
├── api/                    # FastAPI REST endpoints
│   ├── routes/
│   ├── middleware/         # Rate limiting
│   └── schemas/
├── auth/                   # Authentication
│   ├── pat/                # Personal Access Tokens
│   ├── oauth/              # GitHub, Google OAuth
│   └── keys/               # SSH, GPG (not committed)
├── cli/                    # Python CLI (gazette)
│   ├── commands/
│   └── utils/
├── db/                     # SQLite databases
├── docker/                 # Docker configs
├── docs/                   # Documentation
│   └── diagrams/           # SVG process maps
├── grpc/                   # gRPC services
│   ├── protos/             # .proto definitions
│   ├── services/           # Server implementations
│   └── clients/            # Client SDK
├── kanban/                 # Kanban board system
│   ├── models/
│   ├── exports/
│   └── views/
├── mcp/                    # Model Context Protocol
│   ├── claude/
│   ├── deepseek/
│   ├── llama/
│   ├── voice/
│   └── gmail/
├── scripts/                # Shell utilities
├── termux/                 # Termux sync configs
└── training/               # Llama fine-tuning
    ├── dialogs/
    ├── models/
    └── exports/
```

---

## GPG vs SSH Keys

### SSH Keys (You have these)
- **Purpose**: Authentication to remote servers (GitHub, SSH)
- **Files**: `~/.ssh/id_ed25519`, `~/.ssh/id_ed25519.pub`
- **Usage**: `git push`, `ssh user@host`

### GPG Keys (You don't have these)
- **Purpose**: Signing commits and encrypting data
- **What it does**:
  - Signs commits with cryptographic signature (verified badge on GitHub)
  - Encrypts/decrypts files
  - Signs releases and artifacts
- **Not required for**: Basic git operations, API access
- **When needed**: If you want signed commits, encrypted secrets storage

```bash
# Generate GPG key (optional)
gpg --full-generate-key

# Export for GitHub
gpg --armor --export your@email.com

# Sign commits
git config --global commit.gpgsign true
```

---

## PAT (Personal Access Token) vs SSH

| | SSH Key | PAT |
|---|---------|-----|
| **Auth type** | Asymmetric crypto | Bearer token |
| **Best for** | Git operations | API calls, CI/CD |
| **Scope control** | All or nothing | Fine-grained permissions |
| **Rotation** | Manual | Easy, with expiry |
| **Required for** | Git over SSH | GitHub API, gh CLI |

```bash
# Your current setup uses SSH for git
git remote -v  # git@github.com:...

# PAT needed for:
gh api /user  # GitHub CLI API calls
curl -H "Authorization: token ghp_xxx" api.github.com/user
```

---

## Rate Limiting Design

```python
# Token bucket algorithm
RPM_LIMIT = 60       # Requests per minute
RPD_LIMIT = 1000     # Requests per day

# Headers returned
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1707321600
```

---

## Termux Sync

Bidirectional sync between Linux desktop and Android/Termux:

```bash
# Push to mobile
gazette sync push

# Pull from mobile
gazette sync pull

# Synced files
~/.bashrc
~/.zshrc
~/.bash_history
/storage/emulated/0/  # Termux shared storage
```

---

## 8GB VRAM Optimization (arm64v8)

```yaml
# docker-compose.yml
ollama:
  environment:
    OLLAMA_NUM_PARALLEL: 1
    OLLAMA_MAX_LOADED_MODELS: 1
  deploy:
    resources:
      limits:
        memory: 6G
```

```python
# Model parameters
num_ctx = 2048      # Reduced context
num_predict = 512   # Limited output
temperature = 0.7
```

---

## Backlog Tasks

1. **PAT Management** - Token storage, rate limiting
2. **SmartDoc** - Document generation, anonymization
3. **Python CLI** - Replace bash aliases
4. **gRPC Server** - Multi-repo communication
5. **Kanban System** - Task board with exports
6. **Llama Training** - Fine-tune on terminal dialogs

---

## License

MIT

---

*Scaffolded with Claude Code - Feb 2026*
