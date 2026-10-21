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
executor_tier_default: fable | opus | sonnet   # the tier a mission inherits unless it declares its own
executor_runtime: ""                   # optional — the agent runtime executing the campaign (e.g. claude)
token_budget_estimated: "<kT, per ADR-016>"    # campaign total; missions carry their own estimate + actual
token_budget_unit: kT_content_load
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
last_edited_by: agent_<username>
tags: [campaign]
---

# Campaign: <% tp.file.title %>

> **Naming discipline — grep the codename before you set it.** A codename (e.g. "Operation <Name>") is a
> fleet-unique key. Before committing to one, run `grep -ril "Operation <Name>" ~/aDNA`; if it resolves to any
> existing or closed campaign, pick another — a collision produces ambiguous cross-fleet references that route
> cold-start agents to the wrong campaign.

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

*(v8.13.)* Decision rows name the question and the gate that rules it; **options listed before that gate are tagged INFERRED** and re-drawn from the tree at the gate's premise pass (see the mission template's `## Premise pass`). An options column is optional: `| … | Decision | Options (INFERRED until the gate) | Status |`.

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

**Instrument discipline** *(v8.14)*. A check whose green anyone acts on must earn that trust in two ways:

1. **Demonstrated to fail.** Before relying on it, make it go red on purpose: mutate what it asserts, watch it fail,
   restore, watch it pass. Record that this was done.
2. **Reached its target.** It must show that it measured the thing it names (a success status, the expected host, a
   non-empty scope), and it must say **CANNOT VERIFY** rather than pass when it did not. An honest gap beats a false
   green. Corollary: *presence is not conformance*; checking that a field exists is weaker than checking its value.

### Per-Phase

| Check | Method | Gate? |
|-------|--------|-------|
| All mission AARs are GO | Review AAR readiness assessments | Yes — phase cannot advance with NO-GO missions |
| Phase exit criteria met | Campaign doc phase exit gate | Yes — user approval required |
| Risk register updated | Campaign doc risk register | No — recommended |
| Scope changes documented | Campaign doc scope section | Yes — all changes recorded |
| Boundary AAR-light filed *(v8.13)* | `template_aar_lightweight.md` §Boundary AAR-light: a gap register read from the **live system**, improvements each dispositioned by name, a campaign update for the operator | No — recommended at every phase seam, beside the D5-triggered AAR-light and the closing AAR |

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

**Estimation guidance** *(v8.13; the field `calibrated_sessions` above points here).* A phase (or slice) costs, beyond its build sessions, **three gate rows the table must draw**: **close** (the report) · **verdict** (independent, fresh-context) · **rulings / next plan gate**. Size a phase **at its plan gate, from the tree** (carries + the counted work items + the ruled build items), never from the charter alone; **re-base the band at every phase close**; the drift trigger (> 2× the band, ADR-016 of `aDNA.aDNA`) reads against the **re-based** band, not the genesis one. *(Evidence: 64 sittings against a 22–32 band in Terminal's Bastide campaign — wrong by 1.5–4× wherever sized before the tree existed, right wherever a plan gate read the tree.)*

## Notes

[Cross-cutting observations, architectural decisions, coordination notes]

## Completion Summary

*Fill out when setting `status: completed`.*

### Deliverables
- [Concrete outputs: repos, files, systems, records]

### Descoped
- [Missions skipped or deferred, with justification]
- *(v8.13)* A carry handed across a gate is dispositioned **by name with a pointer** — MET `file:line` · retired (reason) · next (reason) — or it is open; the AAR's `## Carries` section holds the ledger and its count line.

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
