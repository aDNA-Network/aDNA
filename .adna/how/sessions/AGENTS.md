---
type: directory_index
created: 2026-02-17
updated: 2026-02-19
last_edited_by: agent_init
tags: [directory_index, sessions]
---

# Session Protocol

## Purpose

Every agent session creates a tracking file before modifying project files. Sessions provide audit trail, conflict detection, and handoff continuity across multiple users and machines.

## Directory Structure

```
how/sessions/
├── AGENTS.md                  # This file (session protocol)
├── active/                    # One file per running session
│   └── session_{user}_{YYYYMMDD}_{HHMMSS}_{descriptor}.md
└── history/
    └── YYYY-MM/               # Completed sessions bucketed by month
        └── session_{user}_{YYYYMMDD}_{HHMMSS}_{descriptor}.md
```

## Two-Tier System

### Tier 1 — Lightweight (default for all sessions)

Every agent session MUST create a session file before modifying project files.

**On start:**
1. Generate session ID: `session_{user}_{YYYYMMDD}_{HHMMSS}_{descriptor}`
2. Create session file in `how/sessions/active/` with minimal frontmatter

**During work:**
3. Follow collision prevention rules (read-before-write, check `updated`, set `last_edited_by`)
4. Append file paths to `files_modified` / `files_created` as work happens

**On end:**
5. Write SITREP + Next Session Prompt
6. Set `status: completed` and `completed: {ISO_TIMESTAMP}`
7. Move file from `sessions/active/` to `sessions/history/YYYY-MM/`

### Tier 2 — Full (opt-in for shared config edits)

Use Tier 2 **only when** editing shared configs (governance files, plugin configs) or performing project-wide bulk operations.

Adds to Tier 1:
- **Scope declaration**: List directories and files the session will touch in frontmatter
- **Conflict scan**: Before starting, scan `how/sessions/active/` for overlapping scopes
- **Heartbeat**: Update `heartbeat` field every ~10 minutes
- **Stale detection**: Sessions with heartbeat >30 min old are considered potentially stale; >8 hours auto-abandoned

When scope overlap is detected, warn the user before proceeding.

## Session File Format

### Tier 1 (minimum)

```yaml
---
type: session
session_id: session_{user}_{YYYYMMDD}_{HHMMSS}_{descriptor}
user: {username}
started: {ISO_TIMESTAMP}
status: active
intent: "Brief description of what this session will do"
files_modified: []
files_created: []
completed:
---

## Activity Log

- HH:MM — Session started
```

### Tier 2 (adds scope + heartbeat)

```yaml
---
session_id: session_{user}_{YYYYMMDD}_{HHMMSS}_{descriptor}
user: {username}
machine: {machine_name}
started: {ISO_TIMESTAMP}
status: active
tier: 2
intent: "Editing CLAUDE.md and shared config"
scope:
  directories:
    - {dir1}
  files:
    - {file1}
heartbeat: {ISO_TIMESTAMP}
files_modified: []
files_created: []
completed:
---

## Activity Log

- HH:MM — Session started
```

## History & Archiving

- Completed sessions move to `how/sessions/history/YYYY-MM/`
- No auto-deletion — files are ~1 KB each, accumulation is negligible
- History enables: audit trails, pattern detection, debugging, session analytics
- Manual cleanup of folders older than 6 months if desired

## Session Closure (SITREP)

Every session ends with a structured status report:

```markdown
## SITREP

**Completed**: [what was finished]
**In progress**: [what was started but not finished, with handoff notes]
**Next up**: [recommended next actions]
**Blockers**: [anything preventing progress]
**Files touched**: [created, modified, moved]
```

## Next-Session Prompt

Every session MUST include a next-session prompt after the SITREP:

```markdown
## Next Session Prompt

[Self-contained paragraph that a fresh agent can read to continue this work.
Include: what was accomplished, what remains, key context, recommended approach.]
```

The next-session prompt ensures continuity. A fresh agent reading this prompt and STATE.md should be able to continue the work without reading the full session history.

Template: `how/templates/template_session.md`

## Load/Skip Decision

**Load this directory when**:
- Creating a new session file at the start of agent work (startup checklist step 9)
- Checking `how/sessions/active/` for conflicting sessions (startup checklist step 4)
- Debugging session protocol issues — stale sessions, missing SITREPs, broken handoffs
- Closing a session — writing SITREP and moving file to history

**Skip when**:
- Mid-session and not creating, checking, or closing sessions
- Reading session history for analytics (scan `history/` directly)
- Already created the session file and remember the Tier 1/Tier 2 rules

**Token cost**: ~1,100 tokens (this AGENTS.md)
