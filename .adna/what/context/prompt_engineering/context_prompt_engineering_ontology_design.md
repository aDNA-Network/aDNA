---
type: context_research
topic: prompt_engineering
subtopic: ontology_design
created: 2026-02-19
updated: 2026-03-18
sources: ["Anthropic — Effective Context Engineering for AI Agents", "Anthropic — Knowledge Graph Memory MCP Server", "Microsoft — GraphRAG: From Local to Global", "ODKE+ — Ontology-Guided Open-Domain Knowledge Extraction (2025)", "MODL — Modular Ontology Design Library", "A-MEM — Agentic Memory for LLM Agents (NeurIPS 2025)"]
context_version: "1.0"
token_estimate: ~2000
last_edited_by: agent_init
tags: [context, prompt_engineering]
quality_score: 4.4
signal_density: 5
actionability: 5
coverage_uniformity: 4
source_diversity: 5
cross_topic_coherence: 4
freshness_category: durable
last_evaluated: 2026-03-17
---

# Prompt Engineering: Ontology Design for LLM Agents

## Key Principles

1. **Design for the context window, not for the database.** An agent-facing ontology exists to serve the context window. Every schema decision — granularity, nesting depth, field count — should be evaluated by how effectively it lets agents retrieve the *minimum viable context* for each task. The ontology is a routing structure, not a storage structure.

2. **Flat schemas outperform deep hierarchies.** LLMs handle flat entity structures with type discriminators far better than deep inheritance trees. Anthropic's MCP Memory Server uses a deliberately flat three-concept schema (Entity, Relation, Observation). Deep hierarchies create ambiguity — a flat base with a `type` field is preferred.

3. **The question test is the classification primitive.** Any piece of knowledge belongs in exactly one ontology category when you apply a classification question. The aDNA triad uses: "Is this about WHAT we know, HOW we work, or WHO is involved?" Minimal categories (3 is sufficient) eliminate sorting ambiguity. Additional categories create decision overhead that wastes agent reasoning tokens.

4. **Ontology snippets beat full schema loading.** Production systems (ODKE+, GraphRAG, Claude Code's AGENTS.md chain) select subsets of available schema relevant to the current task rather than loading everything. Each directory's AGENTS.md is effectively an ontology snippet — it tells the agent what this dimension contains and whether to load or skip it.

5. **Discriminator patterns unify without losing type information.** When entity types share most fields but differ on a few, merge them into a single base type with a discriminator field plus type-specific optional fields. This is Single Table Inheritance for knowledge files — every entity is a markdown file, the `type` field discriminates, and type-specific fields coexist in the same frontmatter format.

6. **Base/extension partitioning enables composition.** Partition the ontology into a universal base (entities any instance needs) and domain extensions (entities specific to a domain). Base entities are invariant across instances; extensions are additive and namespaced. This enables sub-lattices to compose without base conflicts.

## Recommendations

### Entity-Relationship Design

| Pattern | When to Use | Tradeoffs |
|---------|-------------|-----------|
| Flat entity + type discriminator | Entity types share >60% of fields | Simplest; can't enforce type-specific NOT NULL |
| Observation arrays | Facts vary widely per entity | Schema-less extensibility; no structural validation |
| Typed relations (active voice) | Relationships need directionality | Clear semantics; verbose for many relations |
| Community hierarchies (GraphRAG) | Large graphs need multi-level summarization | Excellent for retrieval; expensive to precompute |
| Entity-with-provenance | Agent-generated content needs attribution | Full audit trail; additional storage overhead |

### Discriminator Field Patterns

Discriminators should be enumerated, documented, and stable:

```yaml
# Base entity (all types share this)
type: module          # discriminator at entity level
created: 2026-01-15
updated: 2026-03-18
status: active
tags: [module]

# Type-specific extension
module_type: tool     # second-level discriminator within 'module'
runtime: python3.12
gpu_required: false
```

Design rules for discriminators:
- One discriminator per entity level (avoid nested discriminator chains > 2 deep)
- Enumerate valid values in the type standard document
- Discriminator changes are major version bumps
- New discriminator values are minor version bumps (additive)

### Graph-Based Context Serving

The agent's context retrieval path should follow a convergent graph traversal:

```
Root governance (CLAUDE.md)
  → Relevant triad leg (what/how/who AGENTS.md)
    → Relevant directory (topic/entity AGENTS.md)
      → Specific file(s) needed for current task
```

Each node in this traversal answers: "Should the agent go deeper?" This is selective loading (analogous to projection) — at every level, irrelevant branches are pruned and the token budget decreases monotonically.

Implementation patterns:
- **AGENTS.md as routing nodes** — each tells the agent what it contains, estimated token cost, and when to load
- **Token budget in topic indices** — explicit ~tokens per subtopic enables budget-aware loading
- **Frontmatter as metadata index** — agents read YAML headers without loading full file bodies
- **Named subgraphs** — directories are implicit named graphs; AGENTS.md is the graph descriptor

### Base/Extension Partitioning

**Base schema** (universal to any aDNA instance):

| Layer | Base Entities | Purpose |
|-------|--------------|---------|
| WHO | governance, team, coordination | Decide, work, sync |
| WHAT | context, decisions, modules, lattices | Know, decide, build, compose |
| HOW | campaigns, missions, sessions, templates, skills, pipelines, backlog | Plan, decompose, execute, track, automate, ideate |

**Extension schema** (domain-specific, additive):

| Extension | Entities | Purpose |
|-----------|----------|---------|
| CRM | customers, partners, contacts, projects | External relationships |
| Science | hardware, datasets, targets | Domain objects |
| *Custom* | *any domain-specific types* | *User-defined* |

Rules for extensions:
- Extensions MUST NOT modify base entity types
- Extensions MAY reference base entities via relations
- Extension entity types use the same frontmatter base fields plus type-specific additions
- Extensions are namespaced by domain (e.g., `crm_`, `science_`)

### Ontology Evolution

| Change Type | Version Impact | Migration |
|-------------|---------------|-----------|
| Add entity type | Minor (Y) | No migration — additive |
| Add field to existing type | Minor (Y) | Existing files get default or remain without |
| Rename entity type | Major (X) | Update all instances + cross-references |
| Remove entity type | Major (X) | Deprecate first, remove next major version |
| Change discriminator values | Major (X) | Full instance migration required |
| Merge two entity types | Major (X) | Create unified type with discriminator, migrate both |

Evolution discipline:
- **Additive-first** — prefer adding new types over modifying existing ones
- **Deprecate before delete** — mark deprecated with `deprecated_since` version and `replaced_by` pointer
- **Consolidation map** — document merges explicitly (from → to, discriminator, status)
- **Version in the ontology** — store version within `ontology.md`, not in external references
- **Mermaid ER diagrams** — maintain visual relationship map that updates with each version

## Anti-Patterns

- **Deep inheritance hierarchies.** A 4-level class hierarchy (`Entity → TechnicalEntity → ComputeEntity → GPU`) creates classification ambiguity for agents. Flatten to `type: hardware` with `hardware_layer: L1|L2|L3`.
- **Implicit type semantics.** If an agent must infer entity type from file location rather than frontmatter, you have an implicit schema. Make all type information explicit in frontmatter.
- **Monolithic schema loading.** Loading the full 22-entity ontology when the agent only needs 3 entities for its task wastes context budget. Design for selective loading via AGENTS.md routing.
- **Extension-base coupling.** If removing a CRM extension breaks base session tracking, the boundary is wrong. Extensions depend on base; base MUST NOT depend on extensions.
- **Undocumented discriminators.** A `module_type` field with no enumerated valid values forces agents to infer from existing data. Document all discriminator values in the type standard.
- **Breaking changes without migration.** Renaming `type: topology` to `type: lattice` without a consolidation map leaves orphaned files. Always document the migration path.

## Worked Example: Merge-via-Discriminator

A production aDNA instance evolved its ontology from 27 to 22 entities by merging related types:

| Before | After | Discriminator |
|--------|-------|---------------|
| `tools/` (7 files) + `models/` (6 files) | `modules/` (13 files) | `module_type: tool\|model\|model_wrapper\|preprocessor\|postprocessor` |
| `topologies/` (6 files) + `agents/` (4 files) | `lattices/` (10 files) | `lattice_type: pipeline\|agent\|context_graph\|workflow` |
| `protocols/` (2 files) | `context/` | Reclassified as `context_research` |
| `processes/` | `skills/` | `skill_type: agent\|process` |

Result: fewer entity types, clearer classification, same information preserved via discriminators. Cross-references updated in ~43 files. Breaking change managed via consolidation map with explicit forward/backward mappings.

## Sources

- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic (2025). Context as scarce resource, just-in-time loading, metadata signaling.
- [Knowledge Graph Memory MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) — Anthropic. Flat three-concept schema: Entity, Relation, Observation.
- [From Local to Global: A Graph RAG Approach](https://arxiv.org/html/2404.16130v1) — Microsoft (2024). Community hierarchies, multi-level summarization, token-efficient retrieval.
- [ODKE+: Ontology-Guided Knowledge Extraction](https://arxiv.org/html/2509.04696v1) — Khorshidi et al. (2025). Ontology snippets for dynamic schema subsetting, >95% factual accuracy.
- [MODL: A Modular Ontology Design Library](https://arxiv.org/pdf/1904.05405) — Shimizu et al. (2019). Reusable ontology design patterns: AgentRole, Explicit Typing, EntityWithProvenance.
- [A-MEM: Agentic Memory for LLM Agents](https://arxiv.org/abs/2502.12110) — NeurIPS 2025. Zettelkasten-inspired atomic notes with bidirectional linking; evolving memory graphs.
