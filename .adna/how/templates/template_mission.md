---
plan_id: plan_{short_name}
type: plan
title: "{Human-readable plan title}"
owner: {username}
status: active   # active | awaiting_operator | escalated | completed | abandoned  (v8.12: the two gate states are additive — `awaiting_operator` = halted at a ⛩ human gate; `escalated` = blocked on a decision above the mission; use with `gate:`)
gate:             # optional — pointer to the gate this mission is waiting on (e.g. how/gates/<gate_id>.md or an ISS gate URL); set with awaiting_operator / escalated
mission_class: reconnaissance | implementation | verification | integration | closeout
executor_tier: fable | opus | sonnet   # planned model-routing class (see pattern_model_tiered_campaign_execution)
executor_lane: oauth | key | local      # optional (v8.12) — how the executor is reached: a subscription/OAuth session, an API key, or a local model; distinct from the tier (what class), this names the lane (which route)
# harness:                              # optional (v8.12) — the agent harness that ran the mission; evidence-bearing, never a brand claim
#   name: <harness name>
#   version: <version string>
#   capability_evidence: <path or ref to the record that shows the harness did what the mission relied on>
token_budget_estimated: "<kT, per ADR-016>"   # per-mission budget declaration (SO-11 / ADR-016)
token_budget_actual: "<kT, filled at close>"   # actuals side of the contract; rough is fine
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_edited_by: agent_{username}
tags: [plan]
---

# {Plan Title}

## Goal

One-paragraph description of what this plan achieves when all tasks are complete.

## Premise pass

*(v8.13.)* Every premise this card depends on, re-read **first-hand, read-only, on the tree at `<HEAD>`** at the plan gate, with its result. A bounded grep or count is a premise until it is re-run first-hand at the sitting that depends on it. **A premise pass may delegate the search; it never delegates the read**: every `file:line` in this card is tagged `[D]` (VERIFIED — this sitting read the line) or `[R]` (REPORTED — the subagent or peer that returned it, named), the vault's own provenance tags. "No premises beyond the card's own inputs" is a valid single row.

| # | Premise | Where read (`file:line` @ HEAD) | Result | Tag |
|---|---|---|---|---|
| 1 | {what the card assumes to be true} | {path:line @ sha} | {holds / corrected to … } | [D] / [R] (by whom) |

## Tasks

### 1. {Task title}
- **Status**: planned
- **Session**:
- **Description**: What needs to be done
- **Files**: Key files this task will create or modify
- **Depends on**: none

### 2. {Next task title}
- **Status**: planned
- **Session**:
- **Description**: ...
- **Files**: ...
- **Depends on**: 1

## Notes

Any cross-cutting observations, risks, or decisions made during execution.

## Completion Summary

*Fill out when setting `status: completed`.*

### Deliverables
- {List of concrete outputs: files created, systems built, records populated}

### Descoped
- {Tasks skipped or deferred, with justification}
- *(v8.13)* A carry handed in across a gate is dispositioned **by name with a pointer** — MET `file:line` · retired (reason) · next (reason) — or it is open ("none vanishes").

### Key Findings
- {Insights, patterns, or discoveries from execution}

### Scope Changes
- {Tasks added or removed during execution, and why}

## AAR

*Mandatory before setting `status: completed`. See `how/templates/template_aar_lightweight.md`.*

- **Worked**: [what went well — one line]
- **Didn't**: [what didn't work or surprised us — one line]
- **Finding**: [key insight or discovery — one line]
- **Change**: [process change for next time — one line, or "none"]
- **Follow-up**: [link to backlog/mission/issue, or "none"]
