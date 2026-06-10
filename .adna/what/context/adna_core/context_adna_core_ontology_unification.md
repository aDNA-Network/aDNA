---
type: context_guide
topic: adna_core
subtopic: ontology_unification
created: 2026-02-20
updated: 2026-03-18
sources: ["Ontology Unification Protocol v1.0 (ontology_unification.md)", "aDNA Standard v2.1 (§5.1 ontology artifact)", "Keet (2021) conflict resolution framework"]
context_version: "1.0"
token_estimate: ~1000
last_edited_by: agent_init
tags: [context, adna_core, ontology, unification, merge, conflict_resolution]
quality_score: 4.4
signal_density: 5
actionability: 4
coverage_uniformity: 4
source_diversity: 4
cross_topic_coherence: 4
freshness_category: durable
last_evaluated: 2026-02-20
---

# aDNA Core: Ontology Unification Guide

## Key Principles

1. **Unification happens when instances integrate.** When a sub-lattice is imported into a parent instance, their ontologies must be unified — base entities aligned, extensions reconciled, conflicts resolved.

2. **Base invariance is the anchor.** 14 base entity types are structurally invariant across all instances at the same major version. No renaming, removal, or triad reassignment. Extensions are additive.

3. **The merge algorithm is 4 steps.** Validate base → Collect extensions → Detect conflicts → Resolve and produce merged artifact. Given identical inputs and resolutions, the algorithm is deterministic.

4. **10 conflict types in 4 groups.** Adapted from Keet (2021):

| Group | Types | Severity | Resolution |
|-------|-------|----------|-----------|
| **A: Foundational** | A1 base version, A2 triad assignment, A3 theory | Blocking | Upgrade or restructure |
| **B: Domain** | B1 type name, B2 discriminator, B3 relationship, B4 field semantics | High-Medium | Namespace or rename |
| **C: Axiom** | C1 cardinality, C2 constraint | Low | Adopt more permissive |
| **D: Style** | D1 naming convention | Low | Adopt target convention |

## 4-Step Merge Algorithm

### Step 1: Validate Base Compatibility

```
Source.base_version.major == Target.base_version.major?
  YES → COMPATIBLE (proceed)
  NO  → HALT (upgrade older instance)
```

Minor version differences are OK — additive fields from newer version included in merge.

### Step 2: Collect and Classify Extensions

| Classification | Action |
|---------------|--------|
| **Source-only** (new to target) | Add to merged with namespace prefix |
| **Target-only** (already in target) | Keep as-is |
| **Present in both** (shared) | Check for conflicts → auto-merge or resolve |

### Step 3: Detect Conflicts

For each extension present in both instances, check:

| Check | Conflict Type |
|-------|--------------|
| Same type name, different schema | B1: Type name collision |
| Same discriminator, incompatible values | B2: Discriminator conflict |
| Same relation name, different semantics | B3: Relationship ambiguity |
| Same field name, different meaning | B4: Field semantics mismatch |

### Step 4: Resolve and Produce

| Strategy | When |
|----------|------|
| **Namespace prefix** | Type name collision (most common) — `formation_team` |
| **Union values** | Compatible discriminator values — merge both sets |
| **Rename with qualifier** | Relationship ambiguity — `crm_owns` vs `gov_owns` |
| **Adopt target convention** | Style conflicts — naming, formatting |
| **Adopt more permissive** | Axiom conflicts — cardinality, constraints |
| **User decision** | Ambiguous cases requiring human judgment |

## Worked Example Summary

**Scenario**: org_formation (12 entities) merged with Lattice Labs vault (22 entities).

| Metric | Value |
|--------|-------|
| Source entities | 12 |
| Target entities | 22 |
| Base-compatible (auto-merge) | 3 (Decision, Session, ContextTopic) |
| Source-only extensions (namespaced) | 7 → `formation_*` |
| Conflicts detected | 2 |
| Merged total | **32 entities** |

**Conflict resolutions**:
- `Team` → `formation_team` (B1: org unit ≠ team member profile)
- `Module` → `formation_module` (B1+B4: formation step ≠ compute module)

**Token narrowing post-merge**:

| Level | Types | Reduction |
|-------|-------|-----------|
| Full merged | 32 | — |
| Campaign: org_formation | 22 | 31% |
| Mission: Role Architecture | 5 | 77% |
| Objective: Draft charters | 2 | 60% |

## Namespace Quick Reference

| Namespace | Domain | Status |
|-----------|--------|--------|
| `base_` | Reserved (base types are unprefixed) | Reserved |
| `crm_` | Customer relationship management | Active |
| `bio_` | Biotech / life science | Active |
| `formation_` | Organization formation | Active |
| `compute_` | Compute infrastructure | Available |
| `custom_` | User-defined | Available |

**Rules**: 2-20 chars, lowercase alphanumeric + underscore, no double underscores, starts with letter.

## Pre-Merge Checklist

- [ ] Both instances at same base major version
- [ ] Source namespace identified (e.g., `formation_`)
- [ ] All source entity types enumerated and classified
- [ ] Collision detection run
- [ ] Conflict resolution decisions prepared

## Post-Merge Checklist

- [ ] Merged ontology document exists with all entity types
- [ ] Provenance records source of every entity type
- [ ] All conflict resolutions recorded with rationale
- [ ] Namespace prefixes applied consistently
- [ ] Cross-references updated
- [ ] AGENTS.md files updated to reference merged ontology

## Sources

1. Ontology Unification Protocol v1.0 — full 4-step algorithm, 10-type taxonomy, worked example
2. aDNA Standard v2.1 — §5.1 (ontology artifact, registry pattern)
3. Keet, C.M. (2021). "Toward a Systematic Conflict Resolution Framework for Ontologies." *Applied Sciences*, 11(15), 6903.
