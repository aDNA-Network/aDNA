---
plan_id: mission_<short_name>
type: plan
title: "Human-readable mission title"
owner: <username who created the mission>
status: active
campaign_id: campaign_<name>
campaign_phase: <N>
campaign_mission_number: <N>
mission_class:                        # Optional: reconnaissance | implementation | verification | integration | closeout
executor_tier: fable | opus | sonnet  # planned model-routing class (see pattern_model_tiered_campaign_execution)
token_budget_estimated: "<kT, per ADR-016>"   # per-mission budget declaration
token_budget_actual: "<kT, filled at close>"  # the ONE actuals key — record actuals here, not under another name
executor_lane: oauth | key | local      # optional (v8.12) — how the executor is reached: a subscription/OAuth session, an API key, or a local model; distinct from the tier (what class), this names the lane (which route)
gate:             # optional — pointer to the gate this mission is waiting on (e.g. how/gates/<gate_id>.md or an ISS gate URL); set with awaiting_operator / escalated
depends_on: []    # optional — missions that must complete first (the forward edge; "what this unblocks" is derived from it, never kept by hand)
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
last_edited_by: agent_<username>
tags: [plan, campaign]
---

# Mission: <% tp.file.title %>

**Campaign**: [[how/campaigns/campaign_<name>/campaign_<name>|campaign_<name>]]
**Phase**: <N> — [Phase Name]
**Mission**: <N> of <total>

## Goal

One-paragraph description of what this mission achieves when all objectives are complete. How it advances the parent campaign.

## Exit Gate

[Specific, verifiable criteria that must be true for this mission to be considered complete. Copied from the campaign master document.]

### Acceptance coherence

*(v8.14.)* Before a gate ratifies this mission's budget, the author reads the criteria against each other and asks one
question: **can the stated method satisfy the stated test?** This is not a review of whether the criteria are good or the
budget right. Run the question against **every** pair of a method-bearing criterion and a test-bearing criterion, not
only the pairs that look suspicious, and record which pairs were read. A partial pass and a complete pass otherwise
produce the same sentence, and the ratifying operator cannot tell them apart.

| Method criterion | Test criterion | Can the method satisfy the test? |
|---|---|---|
| {criterion} | {criterion} | {yes / no — and what changed} |

## Premise pass

*(v8.13.)* Every premise this card depends on, re-read **first-hand, read-only, on the tree at `<HEAD>`** at the plan gate, with its result. A bounded grep or count is a premise until it is re-run first-hand at the sitting that depends on it. **A premise pass may delegate the search; it never delegates the read**: every `file:line` in this card is tagged `[D]` (VERIFIED — this sitting read the line) or `[R]` (REPORTED — the subagent or peer that returned it, named), the vault's own provenance tags. "No premises beyond the card's own inputs" is a valid single row.

| # | Premise | Where read (`file:line` @ HEAD) | Result | Tag |
|---|---|---|---|---|
| 1 | {what the card assumes to be true} | {path:line @ sha} | {holds / corrected to … } | [D] / [R] (by whom) |

## Objectives

### 1. Objective title
- **Status**: planned
- **Session**:
- **Description**: What needs to be done
- **Files**: Key files this objective will create or modify
- **Depends on**: none

### 2. Next objective title
- **Status**: planned
- **Session**:
- **Description**: ...
- **Files**: ...
- **Depends on**: 1

## Campaign Context

### Previous Mission Outputs
- [What Mission N-1 produced that this mission builds on]

### Next Mission Inputs
- [What this mission must produce for Mission N+1]

## Notes

Any cross-cutting observations, risks, or decisions made during execution.

## Completion Summary

*Fill out when setting `status: completed`.*

### Deliverables
- [List of concrete outputs: files created, systems built, records populated]

### Descoped
- [Objectives skipped or deferred, with justification]
- *(v8.13)* A carry handed in across a gate is dispositioned **by name with a pointer** — MET `file:line` · retired (reason) · next (reason) — or it is open ("none vanishes").

### Key Findings
- [Insights, patterns, or discoveries from execution]

### Scope Changes
- [Objectives added or removed during execution, and why]

## AAR

*Mandatory before setting `status: completed`. See `how/templates/template_aar_lightweight.md`.*

- **Worked**: [what went well — one line]
- **Didn't**: [what didn't work or surprised us — one line]
- **Finding**: [key insight or discovery — one line]
- **Change**: [process change for next time — one line, or "none"]
- **Follow-up**: [link to backlog/mission/issue, or "none"]
