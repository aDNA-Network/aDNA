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
# issued_by:      # optional (v8.13) — set when this sitting runs UNATTENDED under another station's order: `<station> <stamp>` (e.g. `berthier_automator S30-terminal-1`); then also carry:
#   order: |                 # the order's text, verbatim
#   halt_list: []            # what the sitting was forbidden or told to halt on
#   recommended_taken: []    # every "(Recommended)" option taken as such, so a reader sees no human was present
# continues:      # optional (v8.13) — the session_id this record continues, when one sitting was split (a context clear, a usage pause) into two records
# Record-identity rule (v8.13): ONE record names ONE sitting. A split sitting names the record it continues (`continues:`); a delegated sitting names its issuer (`issued_by:`); a record whose transcript or ids are not this sitting's is refused before any write.
files_modified: []
files_created: []
completed:
---

## Activity Log

- HH:MM — Session started. **Open reads** *(v8.13)*: `ls who/coordination/inbox/` · `ls who/coordination/` · `git status`; cite any new memo where it acts.
- …
- HH:MM — **Seal reads**: the same three reads, before "sealed" / `status: completed`.

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
