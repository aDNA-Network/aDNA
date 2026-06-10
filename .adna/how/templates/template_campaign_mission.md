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
