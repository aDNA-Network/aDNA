---
type: prd
project_slug: <project_slug>
project_title: "<Human-readable title>"
version: "1.0"
owner: <owner>
reviewers: []
approved_by:
approved_date:
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
last_edited_by: agent_<username>
tags: [prd, <project_slug>]
---

# PRD: <% tp.file.title %>

## Problem Statement

[Concise description of the problem this product/feature solves. Reference research findings. Who is affected, what's the impact, why now?]

## Users & Stakeholders

| Role | Description | Impact |
|------|------------|--------|
| | | Primary / Secondary / Informed |
| | | |

## Requirements

### Must Have

| ID | Requirement | Acceptance Criteria | Notes |
|----|------------|-------------------|-------|
| REQ-{SLUG}-001 | | | |
| REQ-{SLUG}-002 | | | |

### Should Have

| ID | Requirement | Acceptance Criteria | Notes |
|----|------------|-------------------|-------|
| REQ-{SLUG}-010 | | | |

### Could Have

| ID | Requirement | Acceptance Criteria | Notes |
|----|------------|-------------------|-------|
| REQ-{SLUG}-020 | | | |

### Won't Have (this version)

| ID | Requirement | Rationale |
|----|------------|-----------|
| REQ-{SLUG}-090 | | |

## Scope

### In Scope

- [Feature / component / behavior included]

### Out of Scope

- [Feature / component / behavior explicitly excluded and why]

## Dependencies

| Dependency | Type | Status | Risk |
|-----------|------|--------|------|
| | Internal / External / Technical | Available / In Progress / Blocked | Low / Medium / High |
| | | | |

## Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| | | |
| | | |

## Timeline

| Milestone | Target Date | Dependencies |
|-----------|------------|--------------|
| | | |
| | | |

## Open Questions

- [ ] [Question 1 — who needs to answer, deadline if any]
- [ ] [Question 2]

## Related

- **Research**: [[how/pipelines/prd_rfc/01_research/]]
- **RFC**: [[how/pipelines/prd_rfc/03_design/]]
- **Plan**: [[how/missions/]]
