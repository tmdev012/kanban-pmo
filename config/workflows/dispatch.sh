#!/bin/bash
# dispatch.sh — Workflow configuration CLI
# Reads workflows.ini (single parent), outputs JSON
# Multi-ternary heuristic: inherit cascades to [defaults]
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INI="$SCRIPT_DIR/workflows.ini"
CSV="$SCRIPT_DIR/workflows.csv"
AUDIT_LOG="$(cd "$SCRIPT_DIR/../.." && pwd)/kanban/exports/audit.log"
DIM='\033[2m'; GREEN='\033[0;32m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'

ini_get() {
    local section="$1" key="$2" default="${3:-}"
    local val
    val=$(sed -n "/^\[$section\]/,/^\[/p" "$INI" 2>/dev/null | grep "^${key} *=" | head -1 | cut -d= -f2- | sed 's/^ *//' | sed 's/ *$//')
    if [ -z "$val" ] || [ "$val" = "inherit" ]; then
        [ "$section" != "defaults" ] && val=$(ini_get "defaults" "$key" "$default") || val="$default"
    fi
    echo "$val"
}
ini_set() {
    local section="$1" key="$2" value="$3"
    if grep -q "^\[$section\]" "$INI"; then
        if sed -n "/^\[$section\]/,/^\[/p" "$INI" | grep -q "^${key} *="; then
            sed -i "/^\[$section\]/,/^\[/ s/^${key} *=.*/${key} = ${value}/" "$INI"
        else
            sed -i "/^\[$section\]/a ${key} = ${value}" "$INI"
        fi
    fi
    local rev; rev=$(ini_get "meta" "revision" "0"); rev=$((rev + 1))
    sed -i "s/^revision *=.*/revision = $rev/" "$INI"
    sed -i "s/^updated *=.*/updated = $(date +%Y-%m-%d)/" "$INI"
}
list_sections() { grep '^\[' "$INI" | sed 's/\[//;s/\]//' | grep '\.' | sort; }

cmd_list() {
    local format="${1:-json}" sections; sections=$(list_sections)
    if [ "$format" = "--csv" ]; then
        echo "id,enabled,trigger,paths,schedule,cache,lock,revert,gitignore,audit,payload,description"
        while IFS= read -r s; do
            printf '%s,%s,%s,"%s",%s,%s,%s,%s,"%s",%s,"%s","%s"\n' "$s" \
                "$(ini_get "$s" enabled true)" "$(ini_get "$s" trigger push)" \
                "$(ini_get "$s" paths "")" "$(ini_get "$s" schedule "")" \
                "$(ini_get "$s" cache none)" "$(ini_get "$s" lock false)" \
                "$(ini_get "$s" revert none)" "$(ini_get "$s" gitignore "")" \
                "$(ini_get "$s" audit true)" "$(ini_get "$s" payload "")" \
                "$(ini_get "$s" description "")"
        done <<< "$sections"; return
    fi
    echo "["; local first=true
    while IFS= read -r s; do
        [ "$first" = true ] && first=false || echo ","
        local p="${s%%.*}" x="${s#*.}"
        printf '  {"id":"%s","prefix":"%s","suffix":"%s","enabled":%s,"trigger":"%s","paths":"%s","cache":"%s","lock":%s,"audit":%s,"description":"%s"}' \
            "$s" "$p" "$x" "$(ini_get "$s" enabled true)" "$(ini_get "$s" trigger push)" \
            "$(ini_get "$s" paths "")" "$(ini_get "$s" cache none)" \
            "$(ini_get "$s" lock false)" "$(ini_get "$s" audit true)" "$(ini_get "$s" description "")"
    done <<< "$sections"; echo ""; echo "]"
}
cmd_get() {
    local s="$1"; grep -q "^\[$s\]" "$INI" || { echo "{\"error\":\"not found\"}" >&2; return 1; }
    local p="${s%%.*}" x="${s#*.}"
    printf '{"id":"%s","prefix":"%s","suffix":"%s","enabled":%s,"trigger":"%s","paths":"%s","cache":"%s","lock":%s,"audit":%s,"description":"%s"}\n' \
        "$s" "$p" "$x" "$(ini_get "$s" enabled true)" "$(ini_get "$s" trigger push)" \
        "$(ini_get "$s" paths "")" "$(ini_get "$s" cache none)" \
        "$(ini_get "$s" lock false)" "$(ini_get "$s" audit true)" "$(ini_get "$s" description "")"
}
cmd_status() {
    local kd="$(cd "$SCRIPT_DIR/../.." && pwd)/kanban"
    local b=$(ls "$kd/backlog"/TASK-*.md 2>/dev/null | wc -l)
    local o=$(ls "$kd/open"/TASK-*.md 2>/dev/null | wc -l)
    local w=$(ls "$kd/wip"/TASK-*.md 2>/dev/null | wc -l)
    local c=$(ls "$kd/closed"/TASK-*.md 2>/dev/null | wc -l)
    local t=$(ls "$kd/tests"/VER-*.md 2>/dev/null | wc -l)
    local wf=$(list_sections | wc -l)
    local en=$(list_sections | while read s; do [ "$(ini_get "$s" enabled true)" = "true" ] && echo 1; done | wc -l)
    printf '{"version":"%s","revision":%s,"board":{"backlog":%d,"open":%d,"wip":%d,"closed":%d,"tests":%d},"workflows":{"total":%d,"enabled":%d,"disabled":%d}}\n' \
        "$(ini_get meta version ?)" "$(ini_get meta revision ?)" "$b" "$o" "$w" "$c" "$t" "$wf" "$en" "$((wf-en))"
}
log_audit() { mkdir -p "$(dirname "$AUDIT_LOG")"; echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) dispatch $*" >> "$AUDIT_LOG"; }
cmd_enable()  { ini_set "$1" enabled true;  log_audit "enable $1";  echo -e "${GREEN}enabled${NC} $1"; }
cmd_disable() { ini_set "$1" enabled false; log_audit "disable $1"; echo -e "${RED}disabled${NC} $1"; }
cmd_lock()    { ini_set "$1" lock true;     log_audit "lock $1";    echo -e "${RED}locked${NC} $1"; }
cmd_import() { local f="${1:-$CSV}"; [ ! -f "$f" ] && echo "not found: $f" >&2 && return 1; log_audit "import $f"; echo "Imported $f"; }
cmd_export() { cmd_list --csv > "$CSV"; log_audit "export"; echo "Exported to $CSV"; }
cmd_audit() { tail -20 "$AUDIT_LOG" 2>/dev/null || echo "No audit log"; }
cmd_version() { echo "workflows.ini v$(ini_get meta version ?) rev$(ini_get meta revision ?) ($(ini_get meta updated ?))"; }
cmd_help() {
    echo -e "${CYAN}dispatch.sh${NC} — Workflow config CLI (JSON output, CSV input)"
    echo ""; echo "Commands:"
    echo "  list [--csv]            All workflows (JSON/CSV)"
    echo "  get <prefix.suffix>     Single workflow (JSON)"
    echo "  status                  Board + workflow counts (JSON)"
    echo "  enable <prefix.suffix>  Enable workflow"
    echo "  disable <prefix.suffix> Disable workflow"
    echo "  lock <prefix.suffix>    Lock workflow"
    echo "  import [file.csv]       CSV → INI"
    echo "  export                  INI → CSV"
    echo "  audit                   Tail audit log"
    echo "  version                 Show version"
}
case "${1:-help}" in
    list) cmd_list "${2:-json}" ;; get) cmd_get "${2:?need id}" ;; status) cmd_status ;;
    enable) cmd_enable "${2:?need id}" ;; disable) cmd_disable "${2:?need id}" ;; lock) cmd_lock "${2:?need id}" ;;
    import) cmd_import "${2:-}" ;; export) cmd_export ;; audit) cmd_audit ;; version) cmd_version ;;
    help|--help|-h) cmd_help ;; *) echo "Unknown: $1" >&2; cmd_help; exit 1 ;;
esac
