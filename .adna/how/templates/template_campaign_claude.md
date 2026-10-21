---
type: governance
subtype: campaign_claude
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_edited_by: agent_{username}
tags: [governance, campaign]
---

# CLAUDE.md — Campaign: {campaign_name}

## Campaign Identity

| Field | Value |
|-------|-------|
| Campaign | `{campaign_id}` |
| Owner | {username} |
| Status | {planning / active / completed} |
| Current Phase | Phase {N}: {phase_name} |
| Live pointer | {≤ 200 characters: the one next act and where it is recorded — e.g. "M03 next (opus), prompt in missions/session_prompts.md; DP2 open"} |

> **Keep the live pointer short and current.** It answers "what happens next?" in one line, ≤ 200 characters.
> History, findings and counts belong in the campaign master doc and `STATE.md`; a pointer that grows into a log
> stops being read and starts disagreeing with them. Rewrite it at every mission close — never append to it.

## Quick Start

1. Read this file (auto-loaded)
2. Read `campaign_{name}.md` — master campaign doc
3. Check current mission status in the phase table
4. Claim next unclaimed objective
5. Create session file and begin work

## Key Files

| File | Purpose |
|------|---------|
| `campaign_{name}.md` | Master campaign document — phases, missions, scope |
| `missions/mission_{name}_m{NN}.md` | Individual mission files |
| `artifacts/` | Campaign deliverables and AARs |
| `context/` | Campaign-specific context (if any) |

## Standing Orders

{Campaign-specific rules that agents must follow. Examples:}

- {All changes must pass validation before committing}
- {Never modify {specific file} without checking with user}
- {Load {specific context file} before starting any mission}

## Context Loading

Load these subtopics for campaign work:

| Subtopic | When |
|----------|------|
| {context_file} | {always / specific missions} |
| {context_file} | {always / specific missions} |

## Delegation Notes

{Information for agents who didn't start this campaign but are picking it up mid-stream. Include: what's been done, what's in progress, any non-obvious decisions made during execution.}
