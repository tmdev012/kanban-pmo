# kanban-pmo - Lightweight shell-based PMO tool
FROM ubuntu:24.04

LABEL maintainer="tmdev012"
LABEL version="1.0.0"
LABEL description="Kanban PMO - shell-based project management with SQLite"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    git \
    jq \
    curl \
    bash \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/kanban-pmo
COPY . .

RUN chmod +x sashi scripts/*.sh lib/sh/* 2>/dev/null || true

CMD ["bash"]
