---
type: context_guide
topic: claude_code
subtopic: hook_system
created: 2026-03-27
updated: 2026-04-03
sources: ["Claude Code hooks documentation", "aDNA operational patterns", "Shell scripting best practices"]
context_version: "1.0"
token_estimate: ~2500
last_edited_by: agent_init
runtime: claude_code
tags: [context, claude_code, hooks, lifecycle, automation, guard]
quality_score: 4.2
signal_density: 5
actionability: 5
coverage_uniformity: 4
source_diversity: 2
cross_topic_coherence: 5
freshness_category: stable
last_evaluated: 2026-04-03
---

# System Configuration: Hook System

> **Runtime scope:** This file documents the Claude Code implementation. The underlying pattern applies to any runtime; only the implementation details are Claude Code-specific.

Claude Code fires shell scripts at six lifecycle events, enabling guardrails, automation, and state management without modifying the agent itself. Hooks are the primary mechanism for enforcing vault invariants at runtime.

---

## Key Principles

| # | Principle | Rule |
|---|-----------|------|
| 1 | **Six lifecycle events** | `SessionStart` (session begins), `PreToolUse` (before any tool call), `PostToolUse` (after any tool call), `PermissionRequest` (when agent needs approval), `PreCompact` (before context window compression), `SessionEnd` (session closes). Each event can trigger multiple shell scripts, executed in order. |
| 2 | **Guard pattern** | PreToolUse hooks act as guardrails. The script receives the tool name and input as JSON on stdin, returns a JSON decision: `{"decision":"allow"}` or `{"decision":"block","reason":"..."}`. Guards enforce invariants (e.g., `.claude/` is read-only) without relying on agent compliance. |
| 3 | **Auto-approve pattern** | PermissionRequest hooks can auto-approve safe operations to reduce friction. Common auto-approvals: read-only tools, `git status`, `git log`, file search, glob. Destructive operations (writes, bash commands that modify state) should still require explicit approval. |
| 4 | **Session bookends** | SessionStart initializes the environment: load AgentDB state, check pending work, verify git status. SessionEnd finalizes: save state, commit session logs, cleanup temporary files. Every session is bracketed by these two hooks. |
| 5 | **Pre-compaction safety** | PreCompact fires before Claude Code compresses conversation history to reclaim context window space. Use this to auto-commit unsaved work, checkpoint AgentDB state, or write a recovery note. Work not persisted before compaction is effectively lost. |
| 6 | **Blocking vs async execution** | PreToolUse and PermissionRequest hooks are **blocking** — the agent waits for the result before proceeding. PostToolUse hooks run **asynchronously** — the agent continues without waiting. Design guard logic for blocking hooks (fast, deterministic). Design logging and telemetry for async hooks. |
| 7 | **Configuration location** | Hooks are defined in `settings.local.json` (gitignored, personal) or `.claude/settings.json` (shared). Each hook specifies: event type, matcher (tool name filter), command to execute, and timeout in milliseconds. |

---

## Event Reference

| Event | When it fires | Blocking | Stdin receives | Expected stdout |
|-------|--------------|----------|----------------|-----------------|
| `SessionStart` | Session begins | Yes | Session metadata JSON | Ignored (exit 0 = success) |
| `PreToolUse` | Before each tool call | Yes | `{"tool_name":"...","tool_input":{...}}` | `{"decision":"allow"}` or `{"decision":"block","reason":"..."}` |
| `PostToolUse` | After each tool call | No (async) | `{"tool_name":"...","tool_input":{...},"tool_output":{...}}` | Ignored |
| `PermissionRequest` | Agent needs approval | Yes | `{"tool_name":"...","tool_input":{...}}` | `{"decision":"allow"}`, `{"decision":"deny"}`, or no output (fall through to user) |
| `PreCompact` | Before context compression | Yes | Compaction metadata JSON | Ignored (exit 0 = success) |
| `SessionEnd` | Session closes | Yes | Session summary JSON | Ignored (exit 0 = success) |

---

## Matcher Syntax

| Matcher value | Scope |
|---------------|-------|
| `""` (empty string) | Fires on ALL tool calls for that event |
| `"Write"` | Fires only on Write tool calls |
| `"Write\|Edit"` | Fires on Write OR Edit tool calls |
| `"Bash"` | Fires only on Bash tool calls |

Matchers apply to PreToolUse, PostToolUse, and PermissionRequest. SessionStart, PreCompact, and SessionEnd ignore matchers (they fire once per event).

---

## Recommended Hook Set

Start with these four. Add more only when a specific need arises.

| Hook | Event | Matcher | Purpose | Timeout |
|------|-------|---------|---------|---------|
| `session-start.sh` | SessionStart | `""` | Initialize AgentDB, check pending work, log session start | 10000ms |
| `guard-claude-dir.sh` | PreToolUse | `"Write\|Edit"` | Block writes to `.claude/` directory | 5000ms |
| `auto-approve-safe.sh` | PermissionRequest | `""` | Auto-approve read-only operations | 5000ms |
| `session-end.sh` | SessionEnd | `""` | Save state, move session file to history | 60000ms |

Optional additions:

| Hook | Event | Matcher | Purpose | Timeout |
|------|-------|---------|---------|---------|
| `guard-secrets.sh` | PreToolUse | `"Write\|Edit"` | Scan for hardcoded secrets before file writes | 5000ms |
| `pre-compact-save.sh` | PreCompact | `""` | Auto-commit and checkpoint before compaction | 30000ms |
| `log-tool-use.sh` | PostToolUse | `""` | Append tool call telemetry to `_meta/logs/` | 5000ms |

---

## Configuration Example

`settings.local.json` (gitignored — references local paths):

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "",
      "hooks": [{"type": "command", "command": "bash .claude/hooks/session-start.sh", "timeout": 10000}]
    }],
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{"type": "command", "command": "bash .claude/hooks/guard-claude-dir.sh", "timeout": 5000}]
    }],
    "PermissionRequest": [{
      "matcher": "",
      "hooks": [{"type": "command", "command": "bash .claude/hooks/auto-approve-safe.sh", "timeout": 5000}]
    }],
    "PreCompact": [{
      "matcher": "",
      "hooks": [{"type": "command", "command": "bash .claude/hooks/pre-compact-save.sh", "timeout": 30000}]
    }],
    "SessionEnd": [{
      "matcher": "",
      "hooks": [{"type": "command", "command": "bash .claude/hooks/session-end.sh", "timeout": 60000}]
    }]
  }
}
```

---

## Script Patterns

### Guard: Protect .claude/ from writes

```bash
#!/bin/bash
# guard-claude-dir.sh — Enforce .claude/ read-only invariant
# Receives: {"tool_name":"Write","tool_input":{"file_path":"...","content":"..."}}
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [[ "$FILE_PATH" == *".claude/"* ]]; then
  echo '{"decision":"block","reason":".claude/ is read-only — route output to _meta/"}'
  exit 0
fi

echo '{"decision":"allow"}'
```

### Auto-approve: Reduce friction for safe operations

```bash
#!/bin/bash
# auto-approve-safe.sh — Auto-approve read-only and low-risk tools
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty')

# Read-only tools: always approve
case "$TOOL" in
  Read|Glob|Grep) echo '{"decision":"allow"}'; exit 0 ;;
esac

# Bash: approve read-only commands
if [[ "$TOOL" == "Bash" ]]; then
  CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
  case "$CMD" in
    "git status"*|"git log"*|"git diff"*|"git branch"*|ls*|pwd|cat*|head*|wc*)
      echo '{"decision":"allow"}'; exit 0 ;;
  esac
fi

# Everything else: fall through to user approval (no output)
```

### Session start: Initialize environment

```bash
#!/bin/bash
# session-start.sh — Session initialization
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
META_DIR="$PROJECT_ROOT/_meta"
LOG_DIR="$META_DIR/logs"

mkdir -p "$LOG_DIR"

# Log session start
echo "{\"event\":\"session_start\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"cwd\":\"$PROJECT_ROOT\"}" \
  >> "$LOG_DIR/sessions.jsonl"

# Check for pending work
if [ -d "$PROJECT_ROOT/how/sessions/active" ]; then
  ACTIVE=$(ls "$PROJECT_ROOT/how/sessions/active/" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$ACTIVE" -gt 0 ]; then
    echo "WARNING: $ACTIVE active session(s) found" >&2
  fi
fi

exit 0
```

### Pre-compact: Save before context compression

```bash
#!/bin/bash
# pre-compact-save.sh — Checkpoint before compaction
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# Stage and commit any unsaved work
cd "$PROJECT_ROOT" || exit 0
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  git add -A
  git commit -m "chore(auto): pre-compaction checkpoint" --no-verify 2>/dev/null
  echo "Pre-compaction commit created" >&2
fi

exit 0
```

### Session end: Finalize and log

```bash
#!/bin/bash
# session-end.sh — Session cleanup and state persistence
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
LOG_DIR="$PROJECT_ROOT/_meta/logs"

mkdir -p "$LOG_DIR"

# Log session end
echo "{\"event\":\"session_end\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" \
  >> "$LOG_DIR/sessions.jsonl"

exit 0
```

---

## Anti-Patterns

| Anti-pattern | Risk | Fix |
|-------------|------|-----|
| No guard on `.claude/` | Agents overwrite configuration files | Add `guard-claude-dir.sh` on PreToolUse for Write/Edit |
| Network calls in blocking hooks | Timeouts cause agent hangs and degraded UX | Move network logic to PostToolUse (async) or cache results |
| No PreCompact hook | Unsaved work lost during context compression | Add checkpoint script that auto-commits dirty state |
| Hardcoded absolute paths | Scripts break across machines and clones | Use `git rev-parse --show-toplevel` or `$PROJECT_ROOT` |
| No hook failure logging | Debugging invisible failures wastes hours | Log stderr to `_meta/logs/hook-errors.log` |
| Overly aggressive guards | Agents route around restrictions or sessions stall | Guard only true invariants; use auto-approve for safe operations |
| Guard scripts with side effects | Unpredictable state mutations on every tool call | Guards should only read and decide, never write |
| Missing `exit 0` in non-blocking hooks | Non-zero exit may be treated as hook failure | Always exit 0 unless intentionally signaling an error |

---

## Timeout Guidelines

| Hook type | Recommended timeout | Rationale |
|-----------|-------------------|-----------|
| Guards (PreToolUse) | 3000-5000ms | Fast, deterministic checks only |
| Auto-approve (PermissionRequest) | 3000-5000ms | Pattern matching, no I/O |
| Session start/end | 10000-60000ms | May run git operations, file I/O |
| Pre-compact | 15000-30000ms | May need to stage and commit files |
| Logging (PostToolUse) | 5000ms | Async, append-only file writes |

If a blocking hook times out, Claude Code proceeds as if the hook returned no output (default behavior for that event type). This means timed-out guards default to **allow** — keep guard logic fast to avoid silent permission bypasses.

---

## Sources

- Claude Code hooks documentation — event lifecycle, matcher syntax, JSON protocol
- aDNA operational patterns — session management, state persistence, `.claude/` invariant
- Shell scripting best practices — fast execution, structured output, error handling
