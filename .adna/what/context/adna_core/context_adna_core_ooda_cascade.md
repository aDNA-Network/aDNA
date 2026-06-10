---
type: context_guide
topic: adna_core
subtopic: ooda_cascade
created: 2026-03-17
updated: 2026-03-18
sources: ["OODA loop (Boyd, 1987)", "aDNA Campaign AGENTS.md protocol", "aDNA Session protocol", "Lattice Protocol war ontology (adapted)"]
context_version: "1.0"
token_estimate: ~1000
last_edited_by: agent_init
tags: [context, adna_core, ooda, execution_hierarchy, evaluation]
quality_score: 4.2
signal_density: 4
actionability: 5
coverage_uniformity: 4
source_diversity: 4
cross_topic_coherence: 5
freshness_category: durable
last_evaluated: 2026-03-17
---

# aDNA Core: OODA Cascade

## Key Principles

1. **Every level runs its own OODA loop.** Observe → Orient → Decide → Act operates at session, mission, and campaign levels. Each level's output feeds the level above.

2. **Three levels, one cascade.** aDNA uses a 3-level evaluation hierarchy: Campaign (strategic) → Mission (tactical) → Session (execution). This is sufficient for most projects. Add higher levels only if your project requires multi-campaign coordination.

3. **Anomalies propagate upward.** A session discovery that affects the mission gets flagged in the mission file. A mission blocker that affects the campaign gets flagged in the campaign doc. Never bury findings.

4. **Restructuring flows downward.** A campaign OODA decision to merge or reorder missions results in mission updates, which result in session replanning.

5. **OODA is opt-in enhancement.** The execution hierarchy (Campaign → Mission → Session) works without formal OODA loops. Adding OODA evaluation points improves quality but isn't required for simple projects.

## The Three OODA Loops

### Session OODA (Execution)

**Frequency**: Continuous within the session.

| Phase | Activity |
|-------|----------|
| **Observe** | Current file state. Test results. Build output. User feedback. |
| **Orient** | Does current state match the objective? What's the most efficient path? |
| **Decide** | What to build, modify, test, or validate next. |
| **Act** | Execute. Create files. Run tests. Produce deliverables. |

**Close-out**: SITREP feeds Mission OODA.

### Mission OODA (Tactical)

**Frequency**: At session close-out (SITREP) and mission completion (AAR).

| Phase | Activity |
|-------|----------|
| **Observe** | Session deliverables. Files created/modified. Objectives completed vs. planned. |
| **Orient** | Is the mission on track? Are remaining objectives correctly scoped? Did the session reveal new requirements? |
| **Decide** | Adjust session plan, request additional context, add objectives, flag mission as blocked. |
| **Act** | Update mission file. Plan next session. Feed findings into campaign OODA if significant. |

**Close-out**: AAR feeds Campaign OODA. GO/NO-GO assessment.

### Campaign OODA (Strategic)

**Frequency**: At mission completion boundaries and phase gates.

| Phase | Activity |
|-------|----------|
| **Observe** | Mission completion status. Deliverable quality. Blockers. Resource consumption vs. estimate. |
| **Orient** | Are missions achieving the campaign objective? Is the mission sequence still optimal? Are there emerging dependencies? |
| **Decide** | Reorder missions, add reconnaissance missions, merge/split missions, escalate blockers. |
| **Act** | Update campaign master document. Adjust mission sequence. Communicate changes. |

## Cascade Dynamics

```
Session SITREP  → feeds → Mission OODA
Mission AAR     → feeds → Campaign OODA
Campaign gate   → restructures → Mission sequence
Mission update  → replans → Session objectives
```

### Upward Flow (Anomalies)

| Discovery Level | Action |
|----------------|--------|
| Session finds design flaw | Flag in SITREP → mission file → campaign doc if significant |
| Mission blocked | Flag in mission file → campaign doc → `#needs-human` if critical |
| Multiple missions blocked | Campaign OODA evaluation → restructure or escalate |

### Downward Flow (Restructuring)

| Decision Level | Effect |
|---------------|--------|
| Campaign reorders missions | Update mission sequence → replan affected sessions |
| Campaign adds reconnaissance mission | Insert into sequence → adjust dependencies |
| Campaign merges two missions | Consolidate objectives → adjust session plans |

## OODA Triggers

| Level | Trigger | Action |
|-------|---------|--------|
| Session | Every action cycle | Continuous observe-orient-decide-act |
| Mission | Session SITREP filed | Review progress, adjust objectives |
| Mission | Mission complete | Run AAR protocol (5-step) |
| Campaign | Phase gate reached | Review all mission AARs, GO/NO-GO for next phase |
| Campaign | Mission blocked >2 sessions | Evaluate whether to restructure |
| Campaign | Scope change requested | Evaluate impact, document decision |

## Anti-Patterns

1. **Skipping session OODA.** Acting without observing file state leads to conflicts and wasted work.
2. **Burying findings.** A session discovery that affects the campaign must propagate upward — don't log it only in the session file.
3. **No AAR on mission close.** Without AARs, gaps accumulate silently. Always run the 5-step AAR protocol.
4. **Auto-advancing through phase gates.** Phase gates require user approval. Never auto-advance campaigns between phases.
5. **OODA without artifacts.** Each OODA cycle should produce a traceable artifact — SITREP, AAR, or campaign doc update. If there's no artifact, the evaluation didn't happen.

## Sources

1. Boyd, J. (1987) — OODA loop framework (Observe-Orient-Decide-Act)
2. aDNA Campaign Protocol (`how/campaigns/AGENTS.md`) — phase gates, mission sequencing
3. aDNA Session Protocol (`how/sessions/AGENTS.md`) — SITREP format, session close-out
4. Lattice Protocol war ontology — adapted 4-level cascade to 3-level aDNA hierarchy
