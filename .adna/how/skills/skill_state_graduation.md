---
type: skill
skill_type: agent
created: 2026-07-24
updated: 2026-07-24
status: active
category: operations
trigger: "A STATE.md (or CHANGELOG) has accreted past its keep-set — a campaign/operation just closed, a vault crossed an era boundary (rename/pivot), or the >100 KB health-check tripwire fired — and aged content must move to a history file verbatim, never deleted."
last_edited_by: agent_init
tags: [skill, state, graduation, state_history, frontmatter_bloat, doc_health, lifecycle]

requirements:
  tools: [Read, Bash, Edit, Write]
  context: [STATE.md, STATE_history.md (or the vault's existing archive convention)]
  permissions: [file_write]
---

# Skill: STATE Graduation

## Overview

`STATE.md` is the **first read of every session** — the cold-start orientation surface. Left ungoverned it
accretes monotonically: fossil `## Current Phase` sections outlive their era, `updated:` frontmatter carries its
whole history as a single-line comment, closed-mission breadcrumbs pile up, and the file eventually exceeds the
read-tooling limit (a large `STATE.md` is exactly what motivates the heavy-file Read convention). **STATE
graduation** is the lifecycle discipline that keeps the live surface small while preserving every aged byte in an
append-only history file — **archive, never delete** (Standing Order 6 / SO-7).

> **Plain-language version:** think of `STATE.md` as the whiteboard by the door — it should say what's happening
> *now* so anyone walking in gets oriented in seconds. Over months the whiteboard fills with old notes nobody
> erases. Graduation is the move of copying the old notes into a bound logbook (`STATE_history.md`) — word for
> word, nothing thrown away — so the whiteboard is legible again but the history is permanent. The logbook is
> append-only: you add to it, you never rewrite it.

This skill codifies a **proven practice, not an aspiration**: a fleet-wide graduation pass has compacted many
vaults' STATE files by roughly an order of magnitude (megabytes → hundreds of KB live), every move verbatim and
byte-exact loss-checked. Upstream normative anchor: the aDNA Standard's STATE.md / archive-never-delete provisions
(`what/docs/adna_standard.md`).

## When to Invoke

- **Primary trigger — era boundary.** A campaign or operation just closed, or the vault crossed a rename/pivot.
  **An era boundary outranks a raw day-count** for choosing the cut line (see the Keep-Set Rule).
- **Secondary trigger — the size tripwire.** The base health check (`skill_node_health_check`, the `>100 KB
  STATE.md` step) flagged the file. The remediation is *graduation*, never deletion.
- **Manual trigger.** An agent observes fossil sections mis-orienting cold starts, or a `STATE.md` that has grown
  slow/heavy to read.
- **CHANGELOG variant.** The identical doctrine applies to a long `CHANGELOG.md` — see §CHANGELOG Variant.

> **Compaction without a guard re-bloats.** A light manual pass is not graduation: a one-off manual compaction of
> a vault's `STATE.md` was undone within a month, the file back to several times its trimmed size. Graduation is
> guarded (the loss-gate + the history file + the tripwire), so it holds.

## The Doctrine (six rules, as proven)

### 1. The `STATE_history.md` convention
A sibling **append-only** file. Aged content moves **verbatim** under a dated `## Graduated YYYY-MM-DD — <reason>`
section; the live `STATE.md` keeps a `state_history:` frontmatter pointer to it. Headings are preserved so
existing anchors resolve in the history file. Archive-never-delete (SO-6/SO-7) — byte-for-byte, forever. Seed:
`template_STATE_history.md`.

### 2. The Keep-Set Rule (what stays live)
Keep in `STATE.md`:
- **Door-state / posture frontmatter** — the small set of keys a cold start needs (`status`, `phase`,
  `campaigns`, `mission`, `updated`, `state_history`).
- **The newest ~3 session/entry blocks** *or* the **live campaign arc**, whichever is the honest live surface.
- **The Resume-Here / ⏭ QUEUED banner** (the single most important cold-start block).
- **Armed registers / pins** — anything still load-bearing (open watch-items, pending gates).
- **Reference sections a *live* campaign still cites.**

Everything else graduates. **A vault's own era boundary (rename / pivot / campaign close) outranks a raw
day-count** for the cut line — graduate at a close, not at a calendar tick.

### 3. The `>100 KB` auto-graduate tripwire
The base health check flags any `STATE.md` (or `CHANGELOG.md`) over **100 KB**. The remediation is *graduate*,
never delete (SO-6). Landing surface: `skill_node_health_check` (the STATE-size step).

### 4. Frontmatter is a first-class graduation class
Frontmatter is routinely **~half the bloat**, in **five distinct faces** — all graduate exactly like body
sections:

| Face | What it looks like | Graduation move |
|------|--------------------|-----------------|
| 1. Repeated-key PRIOR-chain | `updated:` carrying its whole history | keep the current value; move the chain verbatim to history |
| 2. Mega-`tags:` line | one many-KB `tags:` line | keep the live tag set; graduate the accreted remainder |
| 3. Frontmatter-as-changelog | hundreds of accumulated keys (~6 permanent keys per closed mission) | keep door-state keys; graduate closed-mission keys |
| 4. Inline PRIOR-chain comment | a large single-line `# ...` comment on one key | keep the current note; move the inline chain verbatim to history |
| 5. Frozen mega-`status:` breadcrumb | a stale multi-line `status:` self-marked stale by its own NOTE | keep a one-line live status; graduate the breadcrumb |

**Fossil standing sections** (a stale `## Current Phase` / What's-Working / Next-Steps outliving its era) recur
in nearly every vault and **actively mislead cold starts** — graduate them on sight.

### 5. The two supremacy caveats (load-bearing)
- **A vault's own sanctioned compaction convention outranks this default recipe.** If a vault ships its own
  `skill_state_compaction` with a defined keep-window, honor it — do not overwrite it with the default keep-set.
- **Check for an existing archive convention before creating `STATE_history.md`.** If the vault already has one
  (e.g. a `STATE_archive.md` with its own section grammar), **append to it** — do not fork a second history file.
  Match the existing file's section-header grammar.

### 6. The loss-gate (verify before you trim)
Graduation is a **move**, not a rewrite — content is **never summarized on graduation**. Before the live block is
trimmed, verify **byte-exactly**: every non-blank line of the original is present in `(new live ∪ history)`. Only
then write. If the check fails, stop — do not trim. (A `python` set-membership check over non-blank lines is
sufficient.)

## Procedure

1. **Detect & scope.** Read `STATE.md`. Identify the trigger (era boundary / tripwire / manual). Check for a
   **sanctioned compaction convention** and an **existing archive file** (caveat 5) — if either exists, defer to
   it. Determine the cut line by era boundary first, day-count second (rule 2).
2. **Partition.** Split the file into **keep-set** (rule 2) and **graduate-set** (everything else, incl. the five
   frontmatter faces of rule 4 and any fossil standing sections).
3. **Snapshot for the loss-gate.** Record every non-blank line of the current file (rule 6).
4. **Append to history — verbatim.** Add a dated `## Graduated YYYY-MM-DD — <reason>` section (or the vault's
   existing grammar) to `STATE_history.md` (or the existing archive file) holding the graduate-set **byte-for-
   byte**, headings preserved. Never edit prior history sections (append-only).
5. **Trim the live file.** Remove the graduated content from `STATE.md`; keep the keep-set. Ensure the
   `state_history:` pointer is present in frontmatter.
6. **Run the loss-gate.** Verify each snapshot line ∈ `(new STATE.md ∪ history file)`. If any line is missing,
   **revert and stop** (`#needs-human`).
7. **Record.** Note the graduation in the live `STATE.md` handoff (size before→after, files touched) and in the
   session SITREP. Single-writer lease: re-read `updated` before write, stamp on write, one batch.

## Self-Reference (Standing Order 8)

In a mature vault the pattern is visible in the vault's own structure: `STATE.md` is the small live router and
`STATE_history.md` (or an existing archive file) is its append-only immortal spine — its dated graduation sections
are moves, verbatim, never deleted. The `state_history:` pointer in `STATE.md`'s frontmatter is the live→history
link this skill installs. The doctrine produced the very file you would edit.

## CHANGELOG Variant

A long `CHANGELOG.md` graduates by the **same doctrine**: keep the recent-arc window live, move older entries
**verbatim** to `CHANGELOG_archive.md` under dated sections, honor the loss-gate, and let the same `>100 KB`
tripwire flag it. The keep-set for a CHANGELOG is the current-version arc plus the most recent releases; older
release blocks graduate. No separate skill — this variant rides this one.

## Failure Modes

- **Summarizing on graduation** — forbidden; graduation is a verbatim move (rule 6). Summaries lose provenance.
- **Forking a second history file** when one exists — check first (caveat 5).
- **Overwriting a vault's own keep-window** — its sanctioned convention wins (caveat 5).
- **Trimming before the loss-gate passes** — never; the gate is a hard precondition.
- **Treating frontmatter as exempt** — it is routinely half the bloat; it graduates too (rule 4).

## See Also

- `skill_node_health_check` — hosts the `>100 KB` tripwire (rule 3)
- `template_STATE_history.md` — the history-file seed (rule 1)
- `skill_context_graduation` — the *sibling* graduation skill (promotes mission deliverables into the context
  library); distinct from STATE lifecycle but the same "archive, never delete" spirit
