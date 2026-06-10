---
campaign_id: campaign_<name>
type: campaign
title: "Human-readable campaign title"
owner: <username>
status: planning
phase_count: <N>
mission_count: <N>
estimated_sessions: "<min>-<max>"
calibrated_sessions: "<min>-<max>"     # Post-compression estimate (see estimation guidance below)
estimation_class: ""                   # infrastructure | governance-tight | governance-broad | content-novel
priority: high | medium | low
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
last_edited_by: agent_<username>
tags: [campaign]
---

# Campaign: <% tp.file.title %>

## Goal

[One-paragraph strategic objective. What does the world look like when this campaign is complete?]

## Context

[Why this campaign exists. What triggered it. What prior work it builds on. Link to R&D artifacts, backlog ideas, or strategic decisions.]

## Scope

### In Scope

- [Major deliverable or capability 1]
- [Major deliverable or capability 2]

### Out of Scope

- [Explicitly excluded work and rationale]

### Subsumes

| Plan/Mission | Status at Subsumption | Tasks Absorbed By |
|-------------|----------------------|-------------------|
| [[plan_or_mission]] | active (tasks N-M remaining) | Missions X, Y |

## Phases & Missions

### Phase 1: [Phase Name]

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| 0 | [Mission title] | 2-3 | — | planned |
| 1 | [Mission title] | 2 | M0 | planned |

**Phase exit gate**: [What must be true before Phase 2 begins]

### Phase 2: [Phase Name]

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| 2 | [Mission title] | 2 | M1 | planned |

**Phase exit gate**: [Exit criteria]

## Decision Points

| # | When | Decision | Status |
|---|------|----------|--------|
| 1 | Before Mission N | [What needs user approval] | pending |

## Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| [Risk description] | Critical / High / Medium / Low | [Mitigation strategy] |

## Verification Strategy

### Per-Mission

| Check | Method | Gate? |
|-------|--------|-------|
| SITREP filed | Session closure protocol | Yes — mission cannot close without SITREP |
| AAR produced | 5-step AAR protocol | Yes — scorecard + GO/NO-GO required |
| Deliverables validated | AAR scorecard (validated/total) | Yes — all deliverables must be validated or justified |
| Files committed | Git status clean | Yes — no orphaned changes |

### Per-Phase

| Check | Method | Gate? |
|-------|--------|-------|
| All mission AARs are GO | Review AAR readiness assessments | Yes — phase cannot advance with NO-GO missions |
| Phase exit criteria met | Campaign doc phase exit gate | Yes — user approval required |
| Risk register updated | Campaign doc risk register | No — recommended |
| Scope changes documented | Campaign doc scope section | Yes — all changes recorded |

### Campaign Validation

| Check | Method |
|-------|--------|
| Cross-file coherence | All new files referenced from parent AGENTS.md |
| Token budget measured | Sum token_estimate across new/modified context files |
| Template index complete | All new templates listed in `how/templates/AGENTS.md` |
| Skill index complete | All new skills listed in `how/skills/AGENTS.md` |
| Context graduation run | `skill_context_graduation` executed on campaign deliverables |
| STATE.md updated | Campaign status reflected in operational state |

## Timeline

| Phase | Missions | Sessions |
|-------|----------|----------|
| Phase 1 | 0-N | X-Y |
| **Total** | **N missions** | **X-Y sessions** |

## Notes

[Cross-cutting observations, architectural decisions, coordination notes]

## Completion Summary

*Fill out when setting `status: completed`.*

### Deliverables
- [Concrete outputs: repos, files, systems, records]

### Descoped
- [Missions skipped or deferred, with justification]

### Key Findings
- [Insights and discoveries from campaign execution]

### Scope Changes
- [Missions added or removed during execution, and why]

### Follow-Up Campaigns
- [Scoped follow-up initiatives]

## Campaign AAR

*Mandatory before setting `status: completed`. See `how/templates/template_aar_lightweight.md`.*

- **Worked**: [what went well across all missions — one line]
- **Didn't**: [what didn't work or surprised us — one line]
- **Finding**: [key insight or discovery — one line]
- **Change**: [process change for next time — one line, or "none"]
- **Follow-up**: [link to backlog/mission/issue, or "none"]
