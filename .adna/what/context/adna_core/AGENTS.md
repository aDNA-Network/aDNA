---
type: directory_index
created: 2026-02-20
updated: 2026-03-18
token_estimate: 13100
last_edited_by: agent_init
tags: [directory_index, context, adna_core]
---

# aDNA Core — Context Index

## Overview

Foundational knowledge for the aDNA paradigm — enough base context for an agent to bootstrap into the standard and begin designing ontologies, lattices, and campaigns. Distilled from the aDNA Standard v2.1, Design Document, and Phase 4 protocol deliverables (ontology unification, federation, interop).

## Subtopics

| # | Subtopic | File | ~Tokens | Subtype | Key Content |
|---|----------|------|---------|---------|-------------|
| 1 | Paradigm Overview | `context_adna_core_paradigm_overview.md` | ~1,000 | context_core | Triad, governance files, deployment forms, cold-start, collision prevention |
| 2 | Convergence Model | `context_adna_core_convergence_model.md` | ~500 | context_core | Operational quick-ref for token narrowing, design decisions, anti-patterns |
| 3 | Ontology Design | `context_adna_core_ontology_design.md` | ~1,000 | context_guide | Base/extension partitioning, namespace spec, frontmatter system, merge compatibility |
| 4 | Lattice Design | `context_adna_core_lattice_design.md` | ~1,000 | context_guide | YAML schema, node/edge types, execution modes, federation readiness, validation |
| 5 | Context Engineering | `context_adna_core_context_engineering.md` | ~1,000 | context_guide | Writing context files, quality rubric, format selection, topic organization |
| 6 | Federation | `context_adna_core_federation.md` | ~1,000 | context_guide | 5-capability lifecycle, URI scheme, composition patterns, seam edges, interop |
| 7 | Ontology Unification | `context_adna_core_ontology_unification.md` | ~1,000 | context_guide | 4-step merge algorithm, 10-type conflict taxonomy, namespace spec, worked example |
| 8 | Campaign Dispatch | `context_adna_core_campaign_dispatch.md` | ~1,500 | context_guide | Campaign→Mission→Objective hierarchy, phase design, mission execution protocol |
| 9 | OODA Cascade | `context_adna_core_ooda_cascade.md` | ~1,000 | context_guide | 3-level OODA loops, cascade dynamics, triggers, upward/downward flow |
| 10 | Ontology Workshop | `context_adna_core_ontology_workshop.md` | ~1,500 | context_guide | Multi-entity domain design, entity discovery, relationship mapping, validation |
| 11 | Type Vocabulary | `context_adna_core_type_vocabulary.md` | ~500 | context_guide | 19 canonical I/O types (4 tiers: primitives, structured, molecular, media) |
| 12 | FAIR Mapping | `context_adna_core_fair_mapping.md` | ~500 | context_guide | Flat↔nested FAIR envelope interconversion, field correspondence |
| 13 | Entity Definitions | `context_adna_core_entity_definitions.md` | ~1,600 | context_core | 14 base entity types (WHO 3, WHAT 4, HOW 7), triad classification, extension guidance |

## Total Token Budget

~13,100 tokens to load all subtopics. Typical session loads 2-4 subtopics (~1K-3K tokens).

## Usage by Task

| Task | Load These Subtopics |
|------|---------------------|
| Bootstrapping into aDNA (cold start) | paradigm_overview |
| Designing a new ontology or extending existing | ontology_design, convergence_model |
| Building a multi-entity domain from scratch | ontology_workshop, ontology_design |
| Creating a lattice YAML file | lattice_design |
| Writing context library files | context_engineering |
| Loading multi-topic context assemblies | context_engineering (Composition System section) + `context_recipes.md` |
| Auditing context quality | context_engineering (Quality Rubric section) + `skill_context_quality_audit` |
| Federating lattices across instances | federation, lattice_design |
| Merging ontologies from two instances | ontology_unification, ontology_design |
| Designing a campaign | campaign_dispatch, convergence_model |
| Reviewing structure for token efficiency | convergence_model, context_engineering |
| Understanding evaluation loops and cascade | ooda_cascade, campaign_dispatch |
| Running mission AARs | ooda_cascade (triggers section), campaign_dispatch |
| Understanding the full aDNA paradigm | paradigm_overview + convergence_model + ontology_design |
| Annotating module I/O types | type_vocabulary |
| Writing FAIR metadata for objects | fair_mapping |
| Looking up entity type definitions | entity_definitions |
| Onboarding or explaining vault structure | paradigm_overview + entity_definitions |
| Auditing object standards compliance | type_vocabulary + fair_mapping |
| Defining dataset YAML objects | type_vocabulary (for format field) |

## Dependency Notes

- **paradigm_overview** is the entry point — read first for any aDNA work
- **convergence_model** builds on paradigm_overview — the narrowing property in action
- **ontology_design** builds on paradigm_overview — extends the base types
- **lattice_design** is self-contained — YAML schema reference
- **context_engineering** is self-contained — writing guide
- **federation** depends on lattice_design (YAML schema) and references ontology_unification
- **ontology_unification** depends on ontology_design (base/extension partitioning)
- **campaign_dispatch** builds on convergence_model (execution hierarchy)
- **ooda_cascade** builds on campaign_dispatch (evaluation loops for the execution hierarchy)
- **ontology_workshop** depends on ontology_design (base/extension partitioning, question test)
- **type_vocabulary** is self-contained — 19 type definitions for I/O annotations
- **fair_mapping** references type_vocabulary (for `format` field values)
- **entity_definitions** is self-contained — reference for 14 base entity types

## Relationship to prompt_engineering Topic

Three subtopics overlap in domain with the `prompt_engineering` topic. The differentiation:

| adna_core File | prompt_engineering Counterpart | Differentiation |
|----------------|-------------------------------|-----------------|
| convergence_model | convergence_model | adna_core = operational quick-ref ("how to apply"); PE = full theoretical articulation |
| ontology_design | ontology_design | adna_core = aDNA-specific prescriptive guide; PE = general ontology-for-LLMs research |
| federation | federation_composability | adna_core = concrete aDNA protocol distillation; PE = external research patterns |

**Rule**: Load adna_core for aDNA-specific work. Load prompt_engineering for research/theory or cross-project design.

## Load/Skip Decision

**Load when**:
- Bootstrapping into the aDNA paradigm (agent cold-start beyond CLAUDE.md)
- Designing ontologies, lattices, or campaigns within aDNA
- Federating or merging across aDNA instances
- Writing or evaluating context library files

**Skip when**:
- Already oriented via CLAUDE.md + STATE.md for routine operational work
- Working on domain-specific tasks that don't touch aDNA structure
- Performing CRM, communications, or non-structural vault maintenance

**Token cost**: ~400 tokens (this AGENTS.md)
