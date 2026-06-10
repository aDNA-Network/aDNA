---
type: context_guide
topic: adna_core
subtopic: campaign_dispatch
created: 2026-02-20
updated: 2026-03-18
sources: ["aDNA Standard v2.1 (§9 Mission System)", "Campaign AGENTS.md protocol", "campaign_adna_review — worked example (18 missions, 7 phases)"]
context_version: "1.0"
token_estimate: ~1500
last_edited_by: agent_init
tags: [context, adna_core, campaign, mission, execution_hierarchy, dispatch]
quality_score: 4.0
signal_density: 4
actionability: 5
coverage_uniformity: 4
source_diversity: 3
cross_topic_coherence: 4
freshness_category: stable
last_evaluated: 2026-02-20
---

# aDNA Core: Campaign Dispatch Guide

## Key Principles

1. **The execution hierarchy is Campaign → Mission → Objective.** Campaigns coordinate multiple missions toward a strategic goal. Missions decompose tasks across sessions. Objectives are atomic work units tracked per session.

2. **Phased execution with user gates.** Campaigns organize missions into phases. User approval is required before advancing between phases. This prevents runaway execution and ensures alignment.

3. **Missions are the unit of decomposition.** A mission is a task too large for one session. It has objectives, acceptance criteria, and dependencies. Agents claim objectives by session and hand off via SITREP.

4. **Campaign missions live inside the campaign directory.** `how/campaigns/campaign_{name}/missions/` — not in standalone `how/missions/`. Standalone missions live at `how/missions/`.

## Campaign Structure

### Directory Layout

```
how/campaigns/campaign_{name}/
├── campaign_{name}.md             # Master campaign doc
├── missions/
│   ├── mission_{name}_m00.md      # M0
│   ├── mission_{name}_m01.md      # M1
│   └── ...
└── provenance/                    # Source artifacts (optional)
```

### Campaign Document Sections

| Section | Purpose |
|---------|---------|
| **Goal** | 1-2 paragraphs — what the campaign achieves |
| **Context** | What exists now, what's missing, why this campaign |
| **Scope** | In scope / out of scope / subsumes |
| **Phases & Missions** | Phase table with mission list, deps, status |
| **Decision Points** | User gates between phases |
| **Risk Register** | Known risks with severity and mitigation |
| **Verification Strategy** | Per-mission, per-phase, and campaign-level checks |
| **Timeline** | Phase → missions → sessions → calendar estimate |
| **Execution Constraints** | Rules agents must follow |
| **Completion Summary** | Filled when campaign closes |

### Mission Document Sections

| Section | Purpose |
|---------|---------|
| **Objective** | What this mission achieves |
| **Context** | Dependencies, prior work, why now |
| **Acceptance Criteria** | How you know it's done |
| **Objectives** | Numbered list with status per objective |
| **Deliverables** | Files created/modified |
| **Dependencies** | Other missions that must complete first |

## How to Design a Campaign

### Step 1: Define Goal and Scope

- One clear strategic goal (not a laundry list)
- Explicit in-scope / out-of-scope boundaries
- List what this campaign subsumes (absorbs from backlog/missions)

### Step 2: Decompose into Phases

| Phase Design Rule | Rationale |
|-------------------|-----------|
| 3-7 phases | Fewer = too broad; more = too granular |
| Each phase has a clear exit gate | User approval prevents drift |
| Dependencies flow forward (no backward deps) | Clean execution order |
| Research before implementation | Phase 1 = research/foundation |

### Step 3: Classify and Decompose Missions

Assign a `mission_class` to each mission to clarify its nature:

| Class | When to Use | Phase Pattern |
|-------|-------------|---------------|
| `reconnaissance` | Phase 0/1 — research, gap analysis, scope validation | Usually first phase |
| `implementation` | Core build phases — creating deliverables | Middle phases |
| `verification` | Testing, auditing, pre-release validation | Before phase gates |
| `integration` | Cross-system wiring, merge, coherence | Late phases |
| `closeout` | Final validation, AARs, knowledge graduation | Final phase |

### Decompose into Mission Objectives

| Mission Design Rule | Rationale |
|--------------------|-----------|
| 1-3 missions per phase | Manageable scope per phase |
| 3-7 objectives per mission | Each claimable in one session |
| Clear dependencies between missions | Topological ordering |
| Session estimates per mission | Planning and progress tracking |

### Step 4: Define Decision Points

```markdown
| # | When | Decision | Status |
|---|------|----------|--------|
| 1 | Phase 0 | Scope confirmation | pending |
| 2 | Before Phase 2 | Research findings review | pending |
```

Decision points are user gates — the campaign pauses until the user approves.

## Worked Example: campaign_adna_review

| Property | Value |
|----------|-------|
| Goal | Make adna world-class for cold-start users |
| Missions | 18 (M0-M17) |
| Phases | 7 (Kickoff → Research → Core Standard → Schema → Federation → Context → Integration) |
| Sessions (actual) | 15+ |
| Decision points | 6 |
| Scope changes | 4 recorded |
| Deliverables | 7 spec docs, quality rubric, 25+ AGENTS.md, 6 example lattices, 3 protocol documents |

**Key patterns from this campaign**:
- Phase 0 (kickoff) validates scope before any execution
- Research phases (1) produce no file modifications — findings only
- Decision points record concerns and adjustments, not just "approved"
- Scope changes are documented in the campaign doc with rationale
- Subsumption absorbs backlog ideas and standalone missions into campaign scope

## Mission Execution Protocol

### Starting a Mission Objective

1. Read campaign doc — understand current phase and progress
2. Read mission doc — identify unclaimed objectives
3. Claim objective by creating session with `mission_id` in frontmatter
4. Execute the objective
5. SITREP at session close — report completed/in-progress/next-up

### Handoff Between Sessions

The SITREP + next-session prompt ensures continuity:

```markdown
## Next Session Prompt

campaign_adna_review M12, Phase 5. Previous session completed objectives 1-3
(paradigm overview, convergence model, ontology design context files). Objectives
4-8 remain: lattice design, context engineering, federation, ontology unification,
campaign dispatch. Source materials are loaded. Quality rubric threshold is 3.5+
composite, no floor violations.
```

## Evaluation Loops

Each level of the execution hierarchy can run an OODA (Observe-Orient-Decide-Act) evaluation loop. This is an opt-in enhancement that improves quality without changing the basic hierarchy:

| Level | OODA Frequency | Key Output |
|-------|---------------|------------|
| Session | Continuous | SITREP at session close |
| Mission | Session boundaries | AAR at mission close (5-step protocol) |
| Campaign | Phase gates | Phase review, GO/NO-GO assessment |

Anomalies discovered at lower levels propagate upward. Strategic restructuring flows downward. Full specification: `context_adna_core_ooda_cascade.md`.

## Strategic Compass (Optional)

For projects running multiple campaigns, a **strategic compass** defines 3-7 immutable principles that ensure coherence across parallel work streams. Template: `template_strategic_compass.md`.

| Property | Rule |
|----------|------|
| **Alignment** | Every campaign must serve at least one compass principle |
| **Retirement test** | If a campaign serves no principle, retire or restructure it |
| **Immutability** | Principles don't change mid-phase — revise only at phase gates |

The compass is optional. Simple projects with 1-2 campaigns don't need one. Add it when you have 3+ active campaigns that need coordination.

## Anti-Patterns

1. **Unbounded campaigns.** A campaign without phases and exit gates never converges. Always define phases.
2. **Skipping Phase 0.** Launching without scope confirmation leads to rework.
3. **Too many objectives per mission.** More than 7 objectives means the mission should be split.
4. **Implicit dependencies.** Always declare mission dependencies explicitly in the phase table.
5. **No decision record.** Decision points must record what was decided and any concerns — not just "approved."

## Sources

1. aDNA Standard v2.1 — §9 (Mission System), §8 (Session Model)
2. Campaign AGENTS.md — campaign protocol, phase gates, mission claiming
3. campaign_adna_review — 18-mission, 7-phase worked example with 6 decision points
