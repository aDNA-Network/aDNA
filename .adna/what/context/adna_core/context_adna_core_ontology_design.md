---
type: context_guide
topic: adna_core
subtopic: ontology_design
created: 2026-02-20
updated: 2026-03-18
sources: ["aDNA Standard v2.1 (§5, §7)", "Ontology Unification Protocol v1.0", "aDNA Design Document (§3, §9)"]
context_version: "1.0"
token_estimate: ~1000
last_edited_by: agent_init
tags: [context, adna_core, ontology, entity_types, base_extension]
quality_score: 4.4
signal_density: 5
actionability: 4
coverage_uniformity: 4
source_diversity: 3
cross_topic_coherence: 4
freshness_category: durable
last_evaluated: 2026-02-20
---

# aDNA Core: Ontology Design Guide

> **Scope note**: This file is the aDNA-specific prescriptive guide for designing and extending ontologies within the standard. For general ontology design principles for LLM agents (flat vs. deep, discriminator patterns, GraphRAG, academic research), see `prompt_engineering/ontology_design`.

## Key Principles

1. **14 base entity types are structurally invariant.** Every aDNA instance shares these types — no renaming, removal, or triad reassignment.

| Triad | Entity Types | Count |
|-------|-------------|-------|
| **WHO** | governance, team, coordination | 3 |
| **WHAT** | context, decisions, modules, lattices | 4 |
| **HOW** | campaigns, missions, sessions, templates, skills, pipelines, backlog | 7 |

2. **Extensions are additive and namespaced.** Domain-specific entity types use `{domain}_{entity_type}` syntax (e.g., `crm_customer`, `bio_target`, `formation_role`). Extensions never modify base types.

3. **The question test classifies content.** Ask: "Is this about WHAT we know, HOW we work, or WHO is involved?" One answer, one triad leg, one home.

4. **Flat schemas with discriminators beat deep hierarchies.** Use `type` field + type-specific optional fields. Single Table Inheritance for knowledge files.

## How to Extend the Base Ontology

### Step 1: Apply the Question Test

| Your Entity | "Is this about WHAT we know?" | "HOW we work?" | "WHO is involved?" | → Triad |
|-------------|------|------|------|---------|
| Customer records | ✗ | ✗ | ✓ People/orgs we work with | WHO |
| ML model specs | ✓ Knowledge about capabilities | ✗ | ✗ | WHAT |
| Deployment procedures | ✗ | ✓ Operational process | ✗ | HOW |

### Step 2: Choose Namespace

| Namespace | Domain | Status |
|-----------|--------|--------|
| `crm_` | Customer relationship management | Active |
| `bio_` | Biotech / life science | Active |
| `formation_` | Organization formation | Active |
| `compute_` | Compute infrastructure | Available |
| `custom_` | User-defined | Available |

**Namespace rules**: 2-20 lowercase alphanumeric + underscore. No double underscores. No reserved prefixes (`base_`). Starts with letter.

### Step 3: Define Entity Type

```yaml
# Example: Adding a customer entity type
---
type: crm_customer            # namespaced type
created: 2026-02-20
updated: 2026-03-18
status: prospect               # discriminator value
segment: bio                   # type-specific field
deal_stage: pitching           # type-specific field
last_edited_by: agent_init
tags: [crm_customer]
---
```

### Step 4: Create Directory Infrastructure

```
who/customers/                # New directory for crm_customer
├── AGENTS.md                 # Purpose, key files, patterns, Load/Skip
├── customer_acme.md          # Entity file
└── customer_beta.md
```

### Step 5: Update Ontology Artifact

Add entity to `what/ontology.md` with:
- Mermaid ER diagram entry
- Triad classification
- Relationships to existing entities
- Extension namespace

## Frontmatter System

### Required Base Fields (every aDNA file)

| Field | Purpose |
|-------|---------|
| `type` | Entity classification (e.g., `session`, `crm_customer`) |
| `created` | Date of creation (YYYY-MM-DD) |
| `updated` | Date of last modification — critical for collision prevention |
| `last_edited_by` | Attribution — who last modified |
| `tags` | Categorization array |

### Type-Specific Fields

Templates define additional fields per type. Examples:

| Type | Additional Fields |
|------|------------------|
| `session` | `session_id`, `status`, `tier`, `intent` |
| `mission` | `mission_id`, `objectives`, `dependencies` |
| `crm_customer` | `segment`, `deal_stage`, `contacts` |

## Merge Compatibility

When two instances integrate, the Ontology Unification Protocol governs:

| Scenario | Action |
|----------|--------|
| Same base version | Proceed — extensions are additive |
| Different base major version | HALT — upgrade older instance first |
| Extension name collision, same schema | Auto-merge (union fields) |
| Extension name collision, different schema | Namespace the source (e.g., `formation_team` vs base `team`) |

Full merge algorithm: see `adna_core/ontology_unification`.

## Multi-Entity Design

For designing a coherent multi-entity domain from scratch (3+ entity types, relationship mapping, namespace design), see `context_adna_core_ontology_workshop.md`. This file covers single-entity extension; the workshop covers domain-level design.

## Anti-Patterns

1. **Renaming base types.** `missions` → `quests` breaks invariance. Never do this.
2. **Deep inheritance.** `entity > knowledge_entity > scientific_entity > bio_entity` wastes tokens. Use `type: bio_target` instead.
3. **Unprefixed extensions.** `type: customer` without namespace risks collision during federation. Use `crm_customer`.
4. **Skipping the question test.** If classifying feels ambiguous, the triad test produces one answer — use it.

## Sources

1. aDNA Standard v2.1 — §5 (Directory Structure), §7 (Frontmatter System)
2. Ontology Unification Protocol v1.0 — §2 (Base Invariance), §5 (Namespace Specification)
3. aDNA Design Document — §3 (Triad Rationale), §9 (Frontmatter as Integration Layer)
