---
type: context_guide
topic: context_library
subtopic: recipes
created: 2026-03-17
updated: 2026-03-28
sources: ["Context library AGENTS.md", "Context engineering guide", "Campaign dispatch guide"]
context_version: "2.0"
token_estimate: ~1000
last_edited_by: agent_aria
tags: [context, recipes, assembly, cross-topic, claude_code]
quality_score: 4.2
signal_density: 4
actionability: 5
coverage_uniformity: 4
source_diversity: 3
cross_topic_coherence: 5
freshness_category: stable
last_evaluated: 2026-04-03
---

# Context Library: Cross-Topic Assembly Recipes

Named, pre-defined cross-topic context assemblies for multi-disciplinary tasks. Each recipe specifies which subtopics to load, in what order, with token budgets at three tiers.

## Which Recipe Do I Need?

Answer these questions in order — stop at the first **yes**:

1. **Are you new to aDNA or bootstrapping an agent?** → `cold_start_orientation`
2. **Are you creating a lattice YAML, module, or workflow?** → `lattice_authoring`
3. **Are you extending the ontology or adding entity types?** → `ontology_extension`
4. **Are you designing a campaign, phases, or missions?** → `campaign_design`
5. **Are you writing or evaluating a context file?** → `context_authoring`
6. **Are you federating across nodes or merging ontologies?** → `federation_design`
7. **Are you setting up your first aDNA project?** → `first_project_setup`

No match? Fall back to manual subtopic selection from the relevant topic AGENTS.md.

## Key Principles

1. **Recipes are shortcuts, not requirements** — An agent can always load subtopics manually. Recipes encode known-good combinations.
2. **Three budget tiers** — Minimal (quick tasks), Standard (most work), Full (comprehensive production). Follow convergent narrowing: start narrow, expand only if needed.
3. **Order matters** — Subtopics listed in recommended load order. Foundational files first, detail files second.

## Recipes by Intent

### Build — Creating Objects

| Recipe | Topics Used | Subtopics (Standard Load) | ~Tokens | Use When |
|--------|------------|---------------------------|---------|----------|
| `lattice_authoring` | adna_core + lattice_basics | lattice_design, core_concepts | ~6K | Creating lattice YAML files, node/edge design |
| `ontology_extension` | adna_core + prompt_engineering | paradigm_overview, ontology_design, ontology_workshop, PE/ontology_design | ~12K | Extending the base ontology or designing multi-entity domains |
| `first_project_setup` | adna_core + prompt_engineering | paradigm_overview, entity_definitions, PE/agentic_scaffolding | ~8K | Setting up a new aDNA vault or project from scratch |

### Design — Architecture & Planning

| Recipe | Topics Used | Subtopics (Standard Load) | ~Tokens | Use When |
|--------|------------|---------------------------|---------|----------|
| `campaign_design` | adna_core | campaign_dispatch, convergence_model | ~5K | Designing a new campaign — phases, missions, scope |
| `federation_design` | adna_core | federation, lattice_design, ontology_unification | ~10K | Designing cross-instance federation, URI schemes, merge protocols |

### Learn — Onboarding & Skill Development

| Recipe | Topics Used | Subtopics (Standard Load) | ~Tokens | Use When |
|--------|------------|---------------------------|---------|----------|
| `cold_start_orientation` | adna_core | paradigm_overview, convergence_model | ~5.5K | Bootstrapping into aDNA — first session orientation |
| `context_authoring` | adna_core + prompt_engineering | context_engineering, PE/signal_to_token | ~6K | Writing new context files following quality standards |

### Federate — Multi-Node Operations

Cross-references `federation_design` from the Design section. For multi-node work, also consider loading the `ontology_unification` subtopic alongside your primary recipe — merge conflicts are the most common federation pain point.

### Operate — Day-to-Day Operations

| Recipe | Topics Used | Subtopics (Standard Load) | ~Tokens | Use When |
|--------|------------|---------------------------|---------|----------|
| `system_setup` | claude_code + who/governance | vault_architecture, config_cascade, `governance_agent_protocol.md` | ~6.4K | Setting up a new workspace, vault, or project from scratch |
| `agent_onboarding` | claude_code + who/governance | `governance_agent_protocol.md`, memory_integration, vault_architecture | ~7.4K | Onboarding a new agent to an existing vault |
| `orchestration_setup` | claude_code + how/skills | `skill_orchestration_tiers.md`, `skill_sqlite_persistence.md` | ~4.6K | Designing multi-agent workflows, model routing, or tier-based execution |
| `operational_debugging` | claude_code | config_cascade, hook_system, memory_integration | ~7.5K | Troubleshooting config inheritance, hook failures, or memory issues |

Candidates: `standard_compliance_audit` (type_vocabulary + fair_mapping + object_standards_overview, ~6.5K) for verifying objects meet aDNA standards.

## Token Budget Tiers

Each recipe supports three budget tiers. The Standard load is shown in the tables above.

| Tier | When to Use | Budget Rule |
|------|-------------|-------------|
| **Minimal** | Quick reference, single-task checks | Load only the first 1-2 subtopics from the recipe. Target <5K tokens |
| **Standard** | Most tasks — session work, mission objectives | Load the subtopics shown in the recipe tables. Target <12K tokens |
| **Full** | Comprehensive production, campaign-level work | Load all subtopics from all listed topics. Budget the full topic totals |

### Tier Examples (ontology_extension)

| Tier | Load | ~Tokens |
|------|------|---------|
| Minimal | paradigm_overview, ontology_design | ~6K |
| Standard | paradigm_overview, ontology_design, ontology_workshop, PE/ontology_design | ~12K |
| Full | All 13 adna_core + all 7 prompt_engineering | ~56K |

## Task Classification Heuristic

When no recipe is explicitly requested, match the task to a recipe using these keywords:

| Keywords in Task | Recipe Match |
|-----------------|--------------|
| cold start, bootstrap, first run, orientation | `cold_start_orientation` |
| lattice, YAML, node, edge, workflow, pipeline | `lattice_authoring` |
| ontology, entity, extend, domain type, namespace | `ontology_extension` |
| new vault, new project, scaffold, setup from scratch | `first_project_setup` |
| campaign, phase, mission, strategic initiative | `campaign_design` |
| context file, context topic, write context, quality rubric | `context_authoring` |
| federation, merge, cross-instance, URI, seam | `federation_design` |
| workspace, vault, configure, CLAUDE.md, settings, setup | `system_setup` |
| onboard agent, new agent, orient agent | `agent_onboarding` |
| orchestrate, tiers, model routing, multi-agent, parallel | `orchestration_setup` |
| hook failure, config debug, memory issue, inheritance | `operational_debugging` |

If no match: fall back to manual subtopic selection from the relevant topic AGENTS.md files.

## Recipe Creation Protocol

When adding a new recipe:

1. **Identify the recurring pattern** — the recipe must serve 2+ tasks or be used by a skill/pipeline
2. **List subtopics in load order** — foundational first, detail second
3. **Calculate token budgets** — sum `token_estimate` fields from each subtopic's frontmatter
4. **Define all three tiers** — Minimal, Standard, Full
5. **Add keyword triggers** to the Task Classification Heuristic table
6. **Place in the correct intent section** — Build, Design, Learn, Federate, or Operate
7. **Update this file** — add the recipe row to the appropriate intent table

## Sources

- Context library AGENTS.md — topic index and token estimates
- Context engineering guide (`context_adna_core_context_engineering.md`) — quality standards and budget principles
- Campaign dispatch guide (`context_adna_core_campaign_dispatch.md`) — execution hierarchy patterns
