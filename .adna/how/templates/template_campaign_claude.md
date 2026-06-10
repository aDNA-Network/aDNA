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
