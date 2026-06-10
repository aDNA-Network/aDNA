---
type: skill
skill_type: process
created: 2026-03-28
updated: 2026-03-28
status: proposed
category: operations
trigger: "Multiple agents sharing a project, session conflicts hard to detect, learnings accumulating without validation signal, cross-session queries needed"
last_edited_by: agent_aria
tags: [skill, sqlite, persistence, sessions, coordination, learnings, cli]

requirements:
  tools: ["sqlite3 (CLI — standard on macOS/Linux)"]
  context: ["how/sessions/AGENTS.md", "who/coordination/AGENTS.md"]
  permissions: ["read/write to project state directory"]
---

# Skill: SQLite Persistence Pattern

## Overview

aDNA's canonical state lives in Markdown: session files, coordination notes, mission objectives, learnings files. Markdown is human-readable, git-diffable, and Obsidian-browsable. That is intentional and does not change.

The limitation surfaces when agents need to **query** state rather than read it: "Find sessions with overlapping scope." "Which learnings have been validated more than once?" "What failed in the last 7 days?" These require reading and parsing every file manually — slow, expensive, and error-prone.

This skill adds a **SQLite layer alongside** the existing Markdown system. SQLite is zero-dependency, file-based, and requires only `sqlite3` — standard on macOS and Linux. No server, no network, no setup beyond creating the database file.

**The two layers are complementary:**
- **Markdown** — canonical, human-facing, git-tracked, Obsidian-browsable. Always authoritative.
- **SQLite** — agent-facing query index, derived from Markdown state. If they diverge, Markdown wins.

This skill also documents how to build a **project CLI tool** — a small shell script that wraps `sqlite3` commands into named operations (`read-start`, `write-end`, `learn`, `checkpoint`). Projects can name this tool whatever fits their identity. The CLI is optional but makes the pattern ergonomic for agents to call consistently.

## Trigger

Invoke when:
- 3+ agents work concurrently and session conflict detection requires file scanning
- Learnings have accumulated but no way to tell which are validated vs. written once and ignored
- "What changed across sessions?" is a question you need answered more than weekly
- Multi-agent coordination relies on reading coordination note files rather than structured status

Do not invoke prematurely. If you have one agent and occasional sessions, stay Markdown-only.

## Parameters

None — process skill. Covers a pattern and an optional setup procedure.

## Implementation

### Step 1: Understand What You Already Have

Map your existing Markdown state before adding anything:

| Location | What It Tracks | Query Limitation |
|----------|---------------|-----------------|
| `how/sessions/active/` | Active sessions | Conflict detection requires frontmatter scan of all files |
| `how/sessions/history/` | Completed sessions | No cross-session aggregation |
| `who/coordination/` | Cross-agent notes | No structured status or scope tracking |
| `how/missions/` objectives | Progress | No aggregation across missions |
| `how/backlog/` | Ideas | No priority or recency ordering |
| Frontmatter `status:` fields | Per-file state | Cannot join across files |

The SQLite layer indexes this state. It does not move or replace any of it.

---

### Step 2: Choose a Location and Name

Create a directory for the database inside your project. A `state/` directory at project root is a common convention, but any location works.

> **Always use absolute paths.** Relative paths silently route to the wrong database when agents run from different working directories. Hard-code the absolute path in your project's governance file or agent protocol.

Example layout:
```
my_project/
├── state/
│   └── agent.db          # SQLite database
│   └── db                # CLI tool (optional — see Step 5)
├── how/
├── what/
└── who/
```

The CLI tool and database name are yours to choose. Examples: `agentdb`, `statedb`, `db`, `memory`. Pick what fits your project's identity.

---

### Step 3: Initialize the Database

Run once to create the schema:

```bash
sqlite3 /absolute/path/to/state/agent.db << 'EOF'
PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = 5000;
PRAGMA synchronous = NORMAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sessions (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id  TEXT UNIQUE NOT NULL,
  agent       TEXT NOT NULL,
  intent      TEXT,
  status      TEXT CHECK(status IN ('active', 'completed', 'abandoned')) DEFAULT 'active',
  branch      TEXT,
  scope_paths TEXT,                 -- JSON array of files/dirs this session will touch
  started_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  ended_at    DATETIME,
  heartbeat   DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS learnings (
  id                  INTEGER PRIMARY KEY AUTOINCREMENT,
  type                TEXT CHECK(type IN ('pattern', 'failure', 'gotcha')) NOT NULL,
  what                TEXT NOT NULL,
  evidence            TEXT,
  reinforcement_count INTEGER DEFAULT 0,
  created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
  last_reinforced     DATETIME
);

CREATE TABLE IF NOT EXISTS coordination (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  goal             TEXT NOT NULL,
  owner_session    TEXT REFERENCES sessions(session_id),
  files_in_scope   TEXT,            -- JSON array
  tier             INTEGER,
  status           TEXT CHECK(status IN ('active', 'completed', 'blocked')) DEFAULT 'active',
  success_criteria TEXT,
  created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
  completed_at     DATETIME
);

CREATE TABLE IF NOT EXISTS checkpoints (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  coordination_id  INTEGER REFERENCES coordination(id),
  agent            TEXT,
  commit_ref       TEXT,
  files_touched    TEXT,            -- JSON array
  evidence         TEXT,
  created_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS errors (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  tool       TEXT,
  message    TEXT,
  context    TEXT,
  session_id TEXT REFERENCES sessions(session_id),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

PRAGMA user_version = 1;
EOF
```

**What each table indexes:**

| Table | Mirrors | Unlocks |
|-------|---------|---------|
| `sessions` | `how/sessions/` files | Scope conflict detection, session aggregation |
| `learnings` | Project learnings file | Reinforcement tracking, decay filtering |
| `coordination` | `who/coordination/` notes | Structured multi-agent task handoff |
| `checkpoints` | Mission objective notes | Progress snapshots with commit references |
| `errors` | (not in Markdown) | Cross-session failure pattern detection |

---

### Step 4: Integrate with the Session Lifecycle

Agents interact with the database at three points: session start, during work, and session end. The Markdown session file is always created first — the database entry follows.

#### Session Start

```sql
-- 1. Register this session
INSERT INTO sessions (session_id, agent, intent, branch, scope_paths)
VALUES (
  'session_aria_20260328_103000_context',
  'aria',
  'Refactor context library',
  'feat/context-refactor',
  '["what/context/"]'
);

-- 2. Check for scope conflicts with other active sessions
SELECT session_id, agent, intent, scope_paths
FROM sessions
WHERE status = 'active'
  AND session_id != 'session_aria_20260328_103000_context'
  AND heartbeat > datetime('now', '-30 minutes');
-- Non-empty result = warn before touching shared files

-- 3. Load validated learnings (reinforced 2+ times)
SELECT type, what, evidence
FROM learnings
WHERE reinforcement_count >= 2
ORDER BY last_reinforced DESC
LIMIT 20;

-- 4. Load recent failures (last 7 days)
SELECT tool, message, context
FROM errors
WHERE created_at > datetime('now', '-7 days')
ORDER BY created_at DESC;

-- 5. Load active coordination contracts
SELECT goal, files_in_scope, tier, success_criteria
FROM coordination
WHERE status = 'active';
```

#### During Work

```sql
-- Heartbeat (every ~10 minutes for long sessions)
UPDATE sessions SET heartbeat = CURRENT_TIMESTAMP
WHERE session_id = 'session_aria_...';

-- Record errors as they occur
INSERT INTO errors (tool, message, context, session_id)
VALUES ('bash', 'exit code 1: pyenv python not found', 'running tests', 'session_aria_...');

-- Checkpoint multi-agent work
INSERT INTO checkpoints (coordination_id, agent, commit_ref, files_touched, evidence)
VALUES (1, 'aria', 'a1b2c3d', '["what/context/AGENTS.md"]', 'updated, tests pass');
```

#### Session End

```sql
-- Record new learning
INSERT INTO learnings (type, what, evidence)
VALUES ('pattern', 'Absolute DB paths prevent silent routing failures', 'Confirmed in 3 projects');

-- Reinforce an existing learning encountered again
UPDATE learnings
SET reinforcement_count = reinforcement_count + 1,
    last_reinforced = CURRENT_TIMESTAMP
WHERE what LIKE '%absolute%path%';

-- Close this session
UPDATE sessions
SET status = 'completed', ended_at = CURRENT_TIMESTAMP
WHERE session_id = 'session_aria_...';

-- Close coordination contract if finished
UPDATE coordination
SET status = 'completed', completed_at = CURRENT_TIMESTAMP
WHERE id = 1;
```

---

### Step 5: Build a CLI Tool (Optional but Recommended)

A small shell script turns raw SQL into named operations agents can call consistently. The script lives in your project (e.g., `state/db` or `bin/agentdb`) and is committed to the repo so every agent uses the same interface.

Name it whatever fits your project. The operations below are a recommended baseline — extend or trim as needed.

```bash
#!/usr/bin/env bash
# Project state CLI — wraps sqlite3 for agent use
# Usage: ./state/db <command> [args]
# Rename this script to whatever fits your project identity.

set -euo pipefail

# Hard-code the absolute path. Never rely on $PWD.
DB="/absolute/path/to/state/agent.db"

cmd="${1:-help}"
shift || true

case "$cmd" in

  read-start)
    # Load context for session start: failures, patterns, active work
    echo "=== Recent Failures (7d) ==="
    sqlite3 "$DB" "SELECT tool, message, context FROM errors WHERE created_at > datetime('now','-7 days') ORDER BY created_at DESC;"
    echo "=== Validated Patterns ==="
    sqlite3 "$DB" "SELECT type, what FROM learnings WHERE reinforcement_count >= 2 ORDER BY last_reinforced DESC LIMIT 20;"
    echo "=== Active Coordination ==="
    sqlite3 "$DB" "SELECT goal, files_in_scope, tier FROM coordination WHERE status='active';"
    echo "=== Scope Conflicts ==="
    sqlite3 "$DB" "SELECT session_id, agent, intent FROM sessions WHERE status='active' AND heartbeat > datetime('now','-30 minutes');"
    ;;

  write-end)
    # Usage: db write-end '{"session_id":"...","learned":["pattern: x"]}'
    json="${1:-}"
    sid=$(echo "$json" | python3 -c "import sys,json; print(json.load(sys.stdin).get('session_id',''))" 2>/dev/null || echo "")
    if [[ -n "$sid" ]]; then
      sqlite3 "$DB" "UPDATE sessions SET status='completed', ended_at=CURRENT_TIMESTAMP WHERE session_id='$sid';"
      echo "Session $sid closed."
    fi
    ;;

  learn)
    # Usage: db learn pattern|failure|gotcha "what happened" "evidence"
    type="${1:-pattern}"
    what="${2:-}"
    evidence="${3:-}"
    sqlite3 "$DB" "INSERT INTO learnings (type, what, evidence) VALUES ('$type', '$what', '$evidence');"
    echo "Recorded $type learning."
    ;;

  reinforce)
    # Usage: db reinforce <learning_id>
    id="${1:-}"
    sqlite3 "$DB" "UPDATE learnings SET reinforcement_count=reinforcement_count+1, last_reinforced=CURRENT_TIMESTAMP WHERE id=$id;"
    echo "Reinforced learning $id."
    ;;

  contract)
    # Usage: db contract '{"goal":"...","files":["..."],"tier":2}'
    json="${1:-}"
    goal=$(echo "$json" | python3 -c "import sys,json; print(json.load(sys.stdin).get('goal',''))" 2>/dev/null || echo "")
    files=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get('files',[])))" 2>/dev/null || echo "[]")
    tier=$(echo "$json" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tier',1))" 2>/dev/null || echo "1")
    sqlite3 "$DB" "INSERT INTO coordination (goal, files_in_scope, tier) VALUES ('$goal', '$files', $tier);"
    sqlite3 "$DB" "SELECT id FROM coordination ORDER BY id DESC LIMIT 1;"
    ;;

  checkpoint)
    # Usage: db checkpoint '{"coordination_id":1,"commit":"abc123","files":["..."],"evidence":"..."}'
    json="${1:-}"
    coord_id=$(echo "$json" | python3 -c "import sys,json; print(json.load(sys.stdin).get('coordination_id',''))" 2>/dev/null || echo "")
    commit=$(echo "$json" | python3 -c "import sys,json; print(json.load(sys.stdin).get('commit',''))" 2>/dev/null || echo "")
    files=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get('files',[])))" 2>/dev/null || echo "[]")
    evidence=$(echo "$json" | python3 -c "import sys,json; print(json.load(sys.stdin).get('evidence',''))" 2>/dev/null || echo "")
    sqlite3 "$DB" "INSERT INTO checkpoints (coordination_id, commit_ref, files_touched, evidence) VALUES ($coord_id, '$commit', '$files', '$evidence');"
    echo "Checkpoint recorded."
    ;;

  error)
    # Usage: db error "tool" "message" "context" "session_id"
    sqlite3 "$DB" "INSERT INTO errors (tool, message, context, session_id) VALUES ('${1:-}', '${2:-}', '${3:-}', '${4:-}');"
    echo "Error recorded."
    ;;

  prune)
    # Remove stale learnings (never reinforced, older than 30 days)
    deleted=$(sqlite3 "$DB" "DELETE FROM learnings WHERE reinforcement_count=0 AND created_at < datetime('now','-30 days'); SELECT changes();")
    echo "Pruned $deleted stale learnings."
    # Mark abandoned sessions (heartbeat > 8 hours, still active)
    sqlite3 "$DB" "UPDATE sessions SET status='abandoned' WHERE status='active' AND heartbeat < datetime('now','-8 hours');"
    echo "Abandoned stale sessions."
    ;;

  query)
    # Usage: db query "SELECT ..."
    sqlite3 "$DB" "${1:-SELECT 'no query provided';}"
    ;;

  status)
    echo "=== DB: $DB ==="
    echo "Sessions (active):"
    sqlite3 "$DB" "SELECT count(*) FROM sessions WHERE status='active';"
    echo "Learnings (total / validated):"
    sqlite3 "$DB" "SELECT count(*), sum(CASE WHEN reinforcement_count>=2 THEN 1 ELSE 0 END) FROM learnings;"
    echo "Coordination (active):"
    sqlite3 "$DB" "SELECT count(*) FROM coordination WHERE status='active';"
    echo "Errors (7d):"
    sqlite3 "$DB" "SELECT count(*) FROM errors WHERE created_at > datetime('now','-7 days');"
    ;;

  help|*)
    echo "Usage: $(basename "$0") <command>"
    echo ""
    echo "Commands:"
    echo "  read-start              Load session context (failures, patterns, active work)"
    echo "  write-end <json>        Close session: {session_id}"
    echo "  learn <type> <what> <evidence>  Record pattern|failure|gotcha"
    echo "  reinforce <id>          Increment reinforcement count on a learning"
    echo "  contract <json>         Create coordination contract: {goal, files, tier}"
    echo "  checkpoint <json>       Record progress: {coordination_id, commit, files, evidence}"
    echo "  error <tool> <msg> <ctx> <sid>  Record a tool error"
    echo "  prune                   Remove stale learnings, abandon dead sessions"
    echo "  query <sql>             Run arbitrary SQL"
    echo "  status                  Database health summary"
    ;;
esac
```

Make it executable and commit it:

```bash
chmod +x state/db
git add state/db state/
git commit -m "chore: add project state CLI"
```

Agents invoke it as: `./state/db read-start`, `./state/db learn pattern "x" "evidence"`, etc. Always use the path relative to project root, or the absolute path — never rely on `$PATH` resolution.

---

### Step 6: Multi-Level Isolation (Optional)

For workspaces with multiple projects, the same pattern applies at multiple levels:

```
workspace/
├── state/
│   └── workspace.db      # Cross-project patterns only
├── project_alpha/
│   └── state/
│       └── agent.db
└── project_beta/
    └── state/
        └── agent.db
```

**Data flows upward only.** A learning promoted from a project database to the workspace database is copied — not moved. Project databases are authoritative for their own scope. Workspace databases aggregate promoted signals only.

This mirrors the aDNA execution hierarchy: Campaign → Mission → Objective. Each level has bounded scope; findings propagate upward via explicit promotion.

---

### Step 7: Maintain the Database

SQLite is operational memory, not an archive. Keep it lean.

| Task | Frequency | Command |
|------|-----------|---------|
| Prune stale learnings | Monthly | `./state/db prune` |
| Check status | Any time | `./state/db status` |
| Backup before schema changes | Before migrations | `cp state/agent.db state/agent.db.bak` |
| Archive old sessions | Monthly | Delete `completed` sessions older than 90 days — history is in Markdown |

Target: under 200 active learnings, under 500KB total database size.

---

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `state/agent.db` | SQLite file | Queryable index of project state |
| CLI tool | Shell script | Named operations for agent use |
| Session conflict report | Query result | Active sessions with overlapping scope |
| Validated learnings | Query result | Learnings reinforced 2+ times |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Wrong database written | Relative path in sub-repo | Use absolute paths everywhere; hard-code in governance file |
| `database is locked` | Concurrent write without WAL | Ensure `PRAGMA journal_mode=WAL` is set; `busy_timeout=5000` handles most contention |
| Schema mismatch | Partial migration | Restore from `.bak`, reapply migration, increment `PRAGMA user_version` |
| Query store diverges from Markdown | Manual edits not reflected | Markdown is authoritative; rebuild from source if divergence is significant |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Replacing Markdown with SQLite | Breaks human browsability, Obsidian, git diffs | Keep both; SQLite is a derived index |
| Relative path to `agent.db` | Silent routing to wrong database in sub-repos | Hard-code absolute path |
| Storing file contents in DB | Bloat, defeats purpose | Store references (paths, commit hashes) only |
| One global database for all projects | Cross-project pollution | One database per project; promote upward explicitly |
| Never pruning learnings | Signal diluted by noise | Monthly prune; `reinforcement_count=0` after 30 days = candidate for deletion |
| Adding this before feeling the pain | Setup cost with no payoff | Stay Markdown-only until the specific limitations in the Trigger section apply |

## Related

- **Session protocol**: `how/sessions/AGENTS.md`
- **Coordination notes**: `who/coordination/AGENTS.md`
- **Orchestration tiers**: `how/skills/skill_orchestration_tiers.md` — coordination contracts map directly to the `coordination` table
- **Skills protocol**: `how/skills/AGENTS.md`
