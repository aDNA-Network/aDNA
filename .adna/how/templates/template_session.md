---
type: session
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_edited_by: agent_{username}
tags: [session]
session_id: session_{user}_{YYYYMMDD}_{HHMMSS}_{descriptor}
user: {username}
started: {ISO_TIMESTAMP}
status: active
intent: "Brief description of what this session will do"
mission:           # optional (v8.12) — the mission_id this session serves, if any
# lease:           # optional (v8.12) — declare it when you hold a single-writer lease on shared files
#   mode: exclusive | shared
#   fence: <monotonic token, e.g. the commit SHA or ISO timestamp the lease was taken at>
#   read_graphs: []            # other vaults read (not written) under this lease
#   declared_at: {ISO_TIMESTAMP}
files_modified: []
files_created: []
completed:
---

## Activity Log

- HH:MM — Session started

## SITREP

**Completed**:
**In progress**:
**Next up**:
**Blockers**:
**Files touched**:

## Next Session Prompt

{Self-contained paragraph for the next agent: what was accomplished, what remains, key context, recommended approach.}

<!--
Tier 2 additions (add when editing shared configs or performing vault-wide operations):

machine: {machine_name}
tier: 2
scope:
  directories:
    - {dir1}
  files:
    - {file1}
heartbeat: {ISO_TIMESTAMP}
-->
