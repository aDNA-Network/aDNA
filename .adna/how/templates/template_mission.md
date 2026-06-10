---
plan_id: plan_{short_name}
type: plan
title: "{Human-readable plan title}"
owner: {username}
status: active
mission_class: reconnaissance | implementation | verification | integration | closeout
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_edited_by: agent_{username}
tags: [plan]
---

# {Plan Title}

## Goal

One-paragraph description of what this plan achieves when all tasks are complete.

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
