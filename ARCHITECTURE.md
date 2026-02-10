# Gazette Support MCP Framework - Architecture

## Overview

Multi-repo Python framework with gRPC communication, Ollama integration, and SQLite persistence.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         GAZETTE-SUPPORT-MCP                              │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │   CLI   │  │   API   │  │  gRPC   │  │ Kanban  │  │Training │       │
│  │ gazette │  │ FastAPI │  │ Server  │  │  Board  │  │ Llama   │       │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘       │
│       │            │            │            │            │             │
│       └────────────┴────────────┴────────────┴────────────┘             │
│                              │                                           │
│                     ┌────────▼────────┐                                  │
│                     │    SQLite DB    │                                  │
│                     │  (persistence)  │                                  │
│                     └─────────────────┘                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 1. PAT Management & Rate Limiting

### Directory: `auth/`

```
auth/
├── pat/
│   ├── tokens.db          # Encrypted PAT storage
│   ├── manager.py         # CRUD for tokens
│   └── validator.py       # Token validation
├── oauth/
│   ├── github.py          # GitHub OAuth flow
│   ├── google.py          # Google OAuth (Gmail)
│   └── callback.py        # OAuth callback handler
└── keys/
    ├── .gitkeep
    └── README.md          # Instructions (keys NOT committed)
```

### PAT Schema (SQLite)

```sql
CREATE TABLE personal_access_tokens (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,              -- "github-cli", "deepseek-api"
    token_hash TEXT NOT NULL,        -- SHA256 hash (never store plaintext)
    token_prefix TEXT,               -- First 8 chars for identification
    provider TEXT NOT NULL,          -- "github", "deepseek", "openai"
    scopes TEXT,                     -- JSON array: ["repo", "read:user"]
    rate_limit_rpm INTEGER DEFAULT 60,
    rate_limit_rpd INTEGER DEFAULT 1000,
    requests_today INTEGER DEFAULT 0,
    last_request_at DATETIME,
    expires_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    revoked_at DATETIME
);

CREATE TABLE rate_limit_log (
    id INTEGER PRIMARY KEY,
    token_id INTEGER REFERENCES personal_access_tokens(id),
    endpoint TEXT,
    status_code INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_pat_provider ON personal_access_tokens(provider);
CREATE INDEX idx_pat_expires ON personal_access_tokens(expires_at);
CREATE INDEX idx_rate_log_token ON rate_limit_log(token_id, timestamp);
```

### Rate Limiting (Token Bucket)

```python
# api/middleware/rate_limiter.py
from datetime import datetime, timedelta
import sqlite3

class TokenBucketRateLimiter:
    def __init__(self, db_path: str):
        self.db = sqlite3.connect(db_path)

    def check_limit(self, token_id: int) -> tuple[bool, dict]:
        """Returns (allowed, info)"""
        cur = self.db.execute("""
            SELECT rate_limit_rpm, requests_today, last_request_at
            FROM personal_access_tokens WHERE id = ?
        """, (token_id,))
        row = cur.fetchone()

        rpm_limit, requests_today, last_req = row

        # Reset daily counter at midnight
        # Check RPM with sliding window
        # Return headers: X-RateLimit-Remaining, X-RateLimit-Reset

        return allowed, {
            "remaining": rpm_limit - current_minute_requests,
            "reset": next_minute_timestamp
        }
```

### CLI Commands

```bash
# Add PAT
gazette auth add github --name "cli-token" --scopes repo,read:user

# List tokens
gazette auth list

# Revoke
gazette auth revoke github-cli-token

# Check rate limits
gazette auth limits
```

---

## 2. SmartDoc System

### Directory: `cli/commands/smartdoc/`

```
cli/commands/smartdoc/
├── __init__.py
├── generator.py           # Document generation engine
├── anonymizer.py          # Scope anonymization
├── templates/
│   ├── project_initiation.md
│   ├── tech_report.md
│   ├── qm_report.md
│   ├── daily_task.md
│   └── oneoff_task.md
└── exports/
    └── .gitkeep
```

### SmartDoc Schema

```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    doc_type TEXT NOT NULL,           -- "project_init", "tech_report", "qm_report", "daily", "oneoff"
    title TEXT,
    content TEXT,
    anonymized_content TEXT,          -- Redacted version
    metadata JSON,                    -- {"project": "...", "author": "..."}
    git_context JSON,                 -- {"branch": "...", "commits": [...]}
    version INTEGER DEFAULT 1,
    parent_id INTEGER,                -- For versioning
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);

CREATE TABLE doc_anonymization_rules (
    id INTEGER PRIMARY KEY,
    pattern TEXT NOT NULL,            -- Regex pattern
    replacement TEXT NOT NULL,        -- "[REDACTED]", "[CLIENT]", "[PROJECT]"
    category TEXT,                    -- "name", "email", "company", "ip"
    enabled INTEGER DEFAULT 1
);

CREATE INDEX idx_docs_type ON documents(doc_type);
CREATE INDEX idx_docs_created ON documents(created_at);
```

### Anonymization Rules

```python
# cli/commands/smartdoc/anonymizer.py
DEFAULT_RULES = [
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]'),
    (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[IP_ADDRESS]'),
    (r'\b(tmdev012|gazette|sashi)\b', '[PROJECT]'),
    (r'\b(John|Jane|Client\s+\w+)\b', '[PERSON]'),
    (r'sk-[a-zA-Z0-9]{32,}', '[API_KEY]'),
    (r'ghp_[a-zA-Z0-9]{36}', '[GITHUB_TOKEN]'),
]
```

### CLI Usage

```bash
# Generate project initiation doc
smartdoc init "API Gateway v2" --template project_initiation

# Tech report from git history
smartdoc tech --from-commits HEAD~5..HEAD --anonymize

# QM report
smartdoc qm --sprint 12 --metrics coverage,bugs,velocity

# Daily task
smartdoc daily "Implement rate limiting"

# One-off task
smartdoc task "Migrate database schema" --priority high --due 2026-02-14

# Export all docs
smartdoc export --format pdf --anonymize
```

---

## 3. Python CLI (Replacing Bash Aliases)

### Directory: `cli/`

```
cli/
├── __init__.py
├── main.py                # Entry point: gazette
├── commands/
│   ├── __init__.py
│   ├── ask.py             # gazette ask "question"
│   ├── code.py            # gazette code "prompt"
│   ├── doc.py             # gazette doc (smartdoc)
│   ├── push.py            # gazette push (smartpush)
│   ├── sync.py            # gazette sync (termux)
│   ├── auth.py            # gazette auth
│   └── kanban.py          # gazette board
└── utils/
    ├── db.py              # SQLite helpers
    ├── ollama.py          # Ollama API client
    ├── config.py          # Config management
    └── output.py          # Rich console output
```

### Entry Point

```python
# cli/main.py
import typer
from rich.console import Console

app = typer.Typer(name="gazette", help="Gazette Support MCP CLI")
console = Console()

@app.command()
def ask(prompt: str, model: str = "deepseek"):
    """Quick question to AI"""
    ...

@app.command()
def code(prompt: str, context: str = None):
    """Code generation with context"""
    ...

@app.command()
def push(message: str = None, version: str = None):
    """Smart git push with categorization"""
    ...

if __name__ == "__main__":
    app()
```

### Docker Compose

```yaml
# docker-compose.yml
version: "3.8"

services:
  gazette-cli:
    build: .
    volumes:
      - ./db:/app/db
      - ~/.ssh:/root/.ssh:ro
      - ~/.gitconfig:/root/.gitconfig:ro
    environment:
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
      - OLLAMA_HOST=http://ollama:11434
    depends_on:
      - ollama
      - api

  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///db/gazette.db

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api

volumes:
  ollama_data:
```

---

## 4. gRPC Multi-Repo Communication

### Directory: `grpc/`

```
grpc/
├── protos/
│   ├── gazette.proto      # Service definitions
│   ├── docs.proto         # Document sync
│   └── tasks.proto        # Task broadcast
├── services/
│   ├── __init__.py
│   ├── server.py          # gRPC server
│   ├── doc_sync.py        # Document sync service
│   ├── model_query.py     # Model query service
│   └── task_broadcast.py  # Task broadcast service
└── clients/
    ├── __init__.py
    └── gazette_client.py  # Python client SDK
```

### Proto Definition

```protobuf
// grpc/protos/gazette.proto
syntax = "proto3";

package gazette;

service GazetteService {
    // Document operations
    rpc SyncDocument(Document) returns (SyncResponse);
    rpc GetDocument(DocumentRequest) returns (Document);

    // Model queries (cross-repo)
    rpc QueryModel(ModelRequest) returns (ModelResponse);

    // Task broadcasting
    rpc BroadcastTask(Task) returns (TaskAck);
    rpc SubscribeTasks(TaskFilter) returns (stream Task);
}

message Document {
    string id = 1;
    string type = 2;
    string content = 3;
    string repo_origin = 4;
    int64 timestamp = 5;
    map<string, string> metadata = 6;
}

message ModelRequest {
    string prompt = 1;
    string model = 2;  // "llama3.2", "deepseek", "claude"
    string context = 3;
    int32 max_tokens = 4;
}

message Task {
    string id = 1;
    string title = 2;
    string status = 3;  // "backlog", "todo", "in_progress", "done"
    string assignee = 4;
    string repo = 5;
    int64 created_at = 6;
}
```

### Server Implementation

```python
# grpc/services/server.py
import grpc
from concurrent import futures
import gazette_pb2
import gazette_pb2_grpc

class GazetteServicer(gazette_pb2_grpc.GazetteServiceServicer):
    def QueryModel(self, request, context):
        # Route to appropriate model
        if request.model == "llama3.2":
            response = self.ollama_query(request.prompt)
        elif request.model == "deepseek":
            response = self.deepseek_query(request.prompt)

        return gazette_pb2.ModelResponse(content=response)

    def BroadcastTask(self, request, context):
        # Store in local DB, notify subscribers
        self.db.insert_task(request)
        self.notify_subscribers(request)
        return gazette_pb2.TaskAck(success=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gazette_pb2_grpc.add_GazetteServiceServicer_to_server(
        GazetteServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
```

---

## 5. Kanban System

### Directory: `kanban/`

```
kanban/
├── models/
│   ├── __init__.py
│   ├── board.py           # Board model
│   ├── card.py            # Card/task model
│   └── column.py          # Column model
├── exports/
│   ├── csv_export.py
│   ├── json_export.py
│   ├── npm_export.py      # Generate package.json scripts
│   └── docker_export.py   # Docker labels
└── views/
    ├── terminal.py        # Rich terminal view
    └── web.py             # HTML export
```

### Schema

```sql
CREATE TABLE boards (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    repo TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE columns (
    id INTEGER PRIMARY KEY,
    board_id INTEGER REFERENCES boards(id),
    name TEXT NOT NULL,
    position INTEGER,
    wip_limit INTEGER       -- Work-in-progress limit
);

CREATE TABLE cards (
    id INTEGER PRIMARY KEY,
    column_id INTEGER REFERENCES columns(id),
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT DEFAULT 'medium',  -- low, medium, high, critical
    labels JSON,            -- ["bug", "feature", "docs"]
    assignee TEXT,
    due_date DATE,
    story_points INTEGER,
    git_branch TEXT,
    git_commits JSON,       -- Array of commit hashes
    llama_suggestions JSON, -- AI-generated suggestions
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);

CREATE INDEX idx_cards_column ON cards(column_id);
CREATE INDEX idx_cards_priority ON cards(priority);
CREATE INDEX idx_cards_due ON cards(due_date);
```

### CLI Commands

```bash
# Create board
gazette board create "Sprint 12"

# Add card
gazette board add "Implement gRPC server" --column todo --priority high

# Move card
gazette board move 15 --to in_progress

# View board (terminal)
gazette board show

# Export
gazette board export --format csv > sprint12.csv
gazette board export --format npm >> package.json  # Adds scripts
gazette board export --format docker > docker-compose.override.yml

# AI suggestions
gazette board suggest 15  # Get Llama suggestions for card #15
```

---

## 6. Llama 3.2 Training on Terminal Dialogs

### Directory: `training/`

```
training/
├── dialogs/
│   ├── capture.py         # Capture terminal LLM dialogs
│   └── parser.py          # Parse dialog format
├── models/
│   ├── Modelfile          # Ollama custom model definition
│   └── adapter.py         # LoRA adapter management
└── exports/
    ├── jsonl_export.py    # Export for fine-tuning
    └── context_inject.py  # Inject history as context
```

### Dialog Capture Schema

```sql
CREATE TABLE terminal_dialogs (
    id INTEGER PRIMARY KEY,
    session_id TEXT NOT NULL,
    turn_number INTEGER,
    role TEXT NOT NULL,           -- "user", "assistant", "system"
    content TEXT NOT NULL,
    model TEXT,                   -- "llama3.2", "deepseek", "claude"
    tokens_used INTEGER,
    latency_ms INTEGER,
    context_window TEXT,          -- Previous N turns for context
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE training_datasets (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    dialog_ids JSON,              -- Array of dialog IDs included
    format TEXT DEFAULT 'jsonl',  -- "jsonl", "parquet"
    file_path TEXT,
    created_at DATETIME
);

CREATE INDEX idx_dialogs_session ON terminal_dialogs(session_id);
CREATE INDEX idx_dialogs_model ON terminal_dialogs(model);
CREATE INDEX idx_dialogs_ts ON terminal_dialogs(timestamp);
```

### JSONL Export Format

```jsonl
{"messages": [{"role": "system", "content": "You are SASHI, a shell assistant..."}, {"role": "user", "content": "explain git rebase"}, {"role": "assistant", "content": "Git rebase moves commits..."}]}
{"messages": [{"role": "user", "content": "convert this to python"}, {"role": "assistant", "content": "```python\ndef..."}]}
```

### Modelfile for Custom Model

```dockerfile
# training/models/Modelfile
FROM llama3.2

# System prompt with persistent context
SYSTEM """
You are SASHI, a terminal AI assistant with access to:
- Git history and project context
- Previous conversation history from SQLite
- Kanban board state
- Document generation capabilities

You remember previous sessions through the context injection system.
"""

# Training data path (after fine-tuning)
ADAPTER /path/to/gazette-lora.gguf

# Parameters optimized for 8GB VRAM
PARAMETER num_ctx 2048
PARAMETER num_predict 512
PARAMETER temperature 0.7
PARAMETER repeat_penalty 1.1
```

### Training Pipeline

```bash
# 1. Capture dialogs (automatic via sashi wrapper)
gazette training capture --enable

# 2. Export training data
gazette training export --from 2026-01-01 --format jsonl > training_data.jsonl

# 3. Fine-tune (using ollama create)
ollama create gazette-llama -f training/models/Modelfile

# 4. Inject context for session
gazette training inject --last 50  # Inject last 50 turns as context
```

### Context Injection (Persistence Memory)

```python
# training/exports/context_inject.py
def build_context_prompt(session_limit: int = 50) -> str:
    """Build context from recent dialogs for model injection"""
    dialogs = db.execute("""
        SELECT role, content, model FROM terminal_dialogs
        ORDER BY timestamp DESC LIMIT ?
    """, (session_limit,)).fetchall()

    context = "Previous conversation context:\n"
    for role, content, model in reversed(dialogs):
        context += f"[{role}]: {content[:200]}...\n"

    return context
```

---

## Intervention Assessment

### Correct Approach

1. **SQLite for Persistence** - Lightweight, portable, no server needed
2. **gRPC for Inter-Repo** - Efficient binary protocol, streaming support, code generation
3. **Ollama for Local AI** - Native llama.cpp, model management, API compatible
4. **Docker Compose** - Service orchestration, GPU passthrough for Ollama

### Considerations for 8GB VRAM (arm64v8/Termux)

```yaml
# Optimized for mobile/low-VRAM
ollama:
  environment:
    - OLLAMA_NUM_PARALLEL=1      # Single request at a time
    - OLLAMA_MAX_LOADED_MODELS=1 # Only one model in memory
  deploy:
    resources:
      limits:
        memory: 6G               # Leave 2GB for system
```

### Model Parameters for 8GB

```
num_ctx: 2048      # Reduced from 8192
num_predict: 512   # Limit output tokens
num_gpu: 99        # Offload all layers to GPU
num_thread: 4      # ARM cores
```

---

## Next Steps (Priority Order)

1. **Task #1**: PAT management - Foundation for API access
2. **Task #3**: Python CLI - Core infrastructure
3. **Task #2**: SmartDoc - Document generation
4. **Task #5**: Kanban - Task management
5. **Task #4**: gRPC - Multi-repo (after 2+ repos exist)
6. **Task #6**: Training - Requires dialog history accumulation

---

*Generated: 2026-02-07*
