---
type: context_guide
topic: adna_core
subtopic: ontology_workshop
created: 2026-03-17
updated: 2026-03-18
sources: ["aDNA ontology_design guide", "prompt_engineering/ontology_design (entity-relationship patterns)", "MODL — Modular Ontology Design Library", "Operational experience from Lattice Protocol vault (14 base + 12 extension types)"]
context_version: "1.0"
token_estimate: ~1500
last_edited_by: agent_init
tags: [context, adna_core, ontology, workshop, multi_entity, domain_design]
quality_score: 4.2
signal_density: 4
actionability: 5
coverage_uniformity: 4
source_diversity: 4
cross_topic_coherence: 5
freshness_category: durable
last_evaluated: 2026-03-17
---

# aDNA Core: Multi-Entity Ontology Design Workshop

> **Scope note**: `ontology_design` covers extending the base ontology with single entity types. This file walks through designing a coherent multi-entity domain from scratch — entity discovery, relationship mapping, namespace design, and validation.

## Key Principles

1. **Domains emerge from language.** Listen to how domain experts describe their work. Nouns become entities, verbs become relationships, adjectives become discriminator values.
2. **Start with 3-5 entities, not 15.** Most domains need fewer entity types than you expect. Merge similar concepts early. Split only when discriminators can't distinguish them.
3. **Relationships are the hard part.** Entity discovery is straightforward; getting relationships right determines whether the ontology serves agents effectively.
4. **The triad distributes naturally.** Even domain-specific entities follow the WHO/WHAT/HOW pattern. If an entity doesn't clearly belong to one leg, it may need splitting.

## Phase 1: Domain Discovery

### Entity Extraction

Collect domain language from stakeholders, documents, or existing systems. For each candidate entity, apply the **entity test**:

| Test | Question | If YES | If NO |
|------|----------|--------|-------|
| Instance test | "Can I create multiple instances of this?" | Likely an entity | Likely an attribute |
| Independence test | "Does this exist independently of another entity?" | Primary entity | Attribute or subtype |
| Lifecycle test | "Does this have its own status/lifecycle?" | Likely an entity | Attribute of another |

### Worked Example: Research Lab Domain

Raw domain language: *"We run experiments on compounds using protocols. Teams submit proposals for funding. Each experiment produces datasets that other teams can reuse."*

| Candidate | Instance? | Independent? | Lifecycle? | → Decision |
|-----------|-----------|-------------|------------|------------|
| Experiment | Yes | Yes | Yes (planned→running→complete) | Entity |
| Compound | Yes | Yes | Yes (candidate→validated→retired) | Entity |
| Protocol | Yes | Yes | Yes (draft→approved→deprecated) | Entity |
| Team | Yes | Yes | Yes (active→dissolved) | Entity |
| Funding | Yes | Depends on proposal | Yes (applied→awarded→expended) | Entity |
| Dataset | Yes | Yes | Yes (raw→processed→published) | Entity (use base `datasets`) |
| Proposal | Yes | No — belongs to Funding lifecycle | Substage of funding | Merge into Funding |

**Result**: 5 domain entities + 1 base entity reused.

## Phase 2: Triad Classification

Apply the question test to each entity:

| Entity | WHAT? | HOW? | WHO? | → Triad | Namespace |
|--------|-------|------|------|---------|-----------|
| Experiment | ✓ Knowledge product | | | WHAT | `lab_` |
| Compound | ✓ Knowledge object | | | WHAT | `lab_` |
| Protocol | | ✓ Procedure | | HOW | `lab_` |
| Team | | | ✓ People | WHO | `lab_` |
| Funding | | ✓ Operational process | | HOW | `lab_` |
| Dataset | ✓ (use base type) | | | WHAT | — (base) |

## Phase 3: Relationship Mapping

### Relationship Pattern Reference

| Pattern | Implementation | When to Use |
|---------|---------------|-------------|
| **1:many** (parent→children) | Wikilinks in child's frontmatter | Experiment → Datasets, Team → Members |
| **Many:many** | Tags or array frontmatter fields | Compounds ↔ Experiments, Protocols ↔ Experiments |
| **Hierarchical status** | `status` field with defined values | Protocol lifecycle (draft→approved→deprecated) |
| **Temporal** | `created`/`updated` + `start_date`/`end_date` | Funding periods, experiment runs |
| **Cross-triad** | Wikilinks between triad legs | Team (WHO) → Experiment (WHAT) via `lead_team` |

### Relationship Matrix (Research Lab Example)

| From → To | Relationship | Pattern | Field |
|-----------|-------------|---------|-------|
| Experiment → Compound | tests | many:many | `compounds: [compound_x, compound_y]` |
| Experiment → Protocol | follows | many:1 | `protocol: protocol_abc` |
| Experiment → Dataset | produces | 1:many | `experiment: experiment_123` (on dataset) |
| Team → Experiment | leads | 1:many | `lead_team: team_alpha` (on experiment) |
| Funding → Experiment | funds | 1:many | `funding: funding_2026_q1` (on experiment) |

## Phase 4: Directory Structure

Map entities to directories following the triad:

```
who/
├── teams/                    # lab_team
│   ├── AGENTS.md
│   └── team_{name}.md

what/
├── experiments/              # lab_experiment
│   ├── AGENTS.md
│   └── experiment_{name}.md
├── compounds/                # lab_compound
│   ├── AGENTS.md
│   └── compound_{name}.md
├── datasets/                 # datasets (base type)
│   └── ...

how/
├── protocols/                # lab_protocol
│   ├── AGENTS.md
│   └── protocol_{name}.md
├── funding/                  # lab_funding
│   ├── AGENTS.md
│   └── funding_{name}.md
```

## Phase 5: Validation Checklist

Before committing a multi-entity ontology design:

| # | Check | Pass? |
|---|-------|-------|
| 1 | Every entity passes the 3-part entity test | |
| 2 | Every entity maps to exactly one triad leg | |
| 3 | All entities share a single namespace prefix | |
| 4 | No collision with existing base types or extensions | |
| 5 | Every relationship has a defined pattern and field name | |
| 6 | Every directory has an AGENTS.md with Load/Skip decision | |
| 7 | `what/ontology.md` updated with all new types and relationships | |
| 8 | Template files created for each new entity type | |

## When to Split vs. Merge

| Signal | Action |
|--------|--------|
| Two entities share >80% of fields | **Merge** — use a discriminator to distinguish |
| One entity has two distinct lifecycles | **Split** — each lifecycle is a separate entity |
| Entity has >15 type-specific fields | Consider **split** — may be two entities in one |
| Two entities never appear independently | **Merge** — one is an attribute of the other |
| Entity instances are always 1:1 with another | **Merge** — unless they serve different triad legs |

## Anti-Patterns

1. **Starting with too many entities.** Begin with 3-5 and expand. Most domains need fewer types than initial analysis suggests.
2. **Namespace per entity.** All domain entities should share one namespace. `lab_experiment` + `chem_compound` fragments the domain — use `lab_` for both.
3. **Skipping the relationship matrix.** Entity discovery without relationship mapping produces a flat list, not a useful ontology.
4. **Putting everything in WHAT.** Protocols are HOW (procedures), teams are WHO (people). Apply the question test rigorously.
5. **Entity for every noun.** "Reagent" is probably an attribute of Compound, not a separate entity. Apply the entity test.

## Sources

1. aDNA ontology_design guide — base/extension partitioning, namespace spec, question test
2. prompt_engineering/ontology_design — entity-relationship patterns, flat schema patterns, GraphRAG
3. MODL — Modular Ontology Design Library (modular decomposition patterns)
4. Operational experience — Lattice Protocol vault extension from 14 base → 26 types (CRM, bio, compute, formation)
