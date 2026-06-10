---
type: context_research
topic: prompt_engineering
subtopic: federation_composability
created: 2026-02-19
updated: 2026-03-18
sources: ["aDNA Bridge Patterns v1.0", "W3C — SPARQL 1.1 Federation Extensions", "Keet (2021) — Conflict Resolution Framework for Ontologies", "MOMo — Modular Ontology Modeling", "SHACL — W3C Shapes Constraint Language", "FAIR Guiding Principles"]
context_version: "1.0"
token_estimate: ~2000
last_edited_by: agent_init
tags: [context, prompt_engineering]
quality_score: 4.4
signal_density: 4
actionability: 5
coverage_uniformity: 5
source_diversity: 5
cross_topic_coherence: 5
freshness_category: durable
last_evaluated: 2026-03-17
---

# Prompt Engineering: Federation & Composability Patterns

## Key Principles

1. **Federation is query-layer routing, not data duplication.** Separate knowledge graphs can interoperate by routing queries across boundaries — each graph remains authoritative over its own data. In file-based systems, this means agents traverse into child directories and follow cross-references rather than copying content between instances.

2. **Governance is designed not to cross instance boundaries.** Each aDNA instance is governed by its own CLAUDE.md. A child instance nested inside a parent does NOT inherit the parent's safety rules, naming conventions, session tracking, or persona. Governance isolation is a convention enforced by agent compliance with CLAUDE.md — the foundational design principle of multi-instance composition.

3. **Five federation capabilities form a complete lifecycle.** Any shareable knowledge unit needs: validate (against schema), export (as standalone artifact), share (via transfer mechanism), import (with compatibility check), compose (as sub-graph within a larger structure). Missing any capability creates a gap in the federation story.

4. **Base invariance enables additive extension.** When two instances merge, base entity types (universal to any instance) are invariant — they must match. Extensions are additive and namespaced. This means a CRM extension from one instance doesn't conflict with a science extension from another; both layer on top of the same base.

5. **Composition patterns are physical relationships.** Three patterns cover how instances relate: nesting (parent contains child), sibling (organizational peers), and monorepo (sub-projects under shared root). The choice depends on agent workflow, knowledge flow direction, and lifecycle coupling.

6. **Conflict resolution has a taxonomy.** Ontology merging conflicts fall into 10 types across 4 groups (foundational, domain, axiom, style). Each type has a known resolution strategy — this isn't ad-hoc; it's systematic.

## Recommendations

### Five Federation Capabilities

| Capability | What It Does | Schema Implications |
|------------|-------------|---------------------|
| **Validate** | Confirm artifact matches schema | JSON Schema or SHACL shapes; validation tooling required |
| **Export** | Package as standalone artifact with FAIR metadata | Self-contained `.lattice.yaml` with provenance, version, license |
| **Share** | Transfer via git, registry, or direct copy | Standard packaging format; no instance-specific paths in exported artifact |
| **Import** | Ingest into another instance with compatibility check | Ontology version check; base version must match; extension conflicts flagged |
| **Compose** | Reference as sub-graph within a larger structure | Parent lattice references child by URI; node IDs resolve across boundaries |

### Composition Patterns

| Pattern | Structure | Best When |
|---------|-----------|-----------|
| **Nesting** (parent contains child) | Parent vault physically contains child repo | Agent frequently works in both in the same session; parent reads child content |
| **Sibling** (organizational peers) | Separate directories, separate repos | Instances rarely reference each other; independent operations |
| **Monorepo** (sub-projects under shared root) | Single repo, multiple sub-project triads | Large project with distinct teams sharing a repository |

Decision factors:

| Factor | Nest | Separate |
|--------|------|----------|
| Agent works in both per session? | Yes → nest | Rarely → separate |
| Parent regularly reads child? | Yes → nest | No → separate |
| Same sync mechanism? | Yes → nest | Different → separate |
| Clear hierarchy? | Yes → nest | Peer relationship → separate |
| Lifecycle coupling? | Tight → nest | Independent → separate |

Default recommendation: **start as siblings**. Nesting adds scope-boundary management complexity. Nest only when cross-boundary workflow clearly demands it.

### Merge Semantics

When two aDNA instances need to combine (e.g., integrating a sub-lattice):

**Step 1: Validate base version compatibility**
```
Source base version == Target base version?
  → Yes: proceed
  → No: upgrade older base first (migration required)
```

**Step 2: Collect extensions**
```
Source extensions ∪ Target extensions
  → No overlap: merge directly (additive)
  → Overlap detected: go to conflict resolution
```

**Step 3: Detect conflicts**

| Conflict Type | Detection | Resolution |
|---------------|-----------|------------|
| Type name collision | Same `type:` value, different schema | Namespace one: `crm_customer` vs `bio_customer` |
| Discriminator conflict | Same discriminator field, different valid values | Union valid values if compatible; namespace if not |
| Relationship ambiguity | Same relation name, different semantics | Rename one; document mapping |
| Field semantics mismatch | Same field name, different meaning | Rename one field; add mapping annotation |
| Foundational theory conflict | Incompatible base ontologies | Cannot merge — resolve at base level first |

**Step 4: Produce merged artifact**
- Merged ontology document with all entity types
- Provenance annotations (which entities came from which source)
- Migration guide for instances that need to adopt the merged schema

### Sub-Graph Extraction

To extract a subset of a knowledge graph as a standalone shareable unit:

1. **Define boundary** — which entity types and relationships to include
2. **Resolve internal references** — all wikilinks within the subset must resolve within it (or be converted to external references)
3. **Package metadata** — FAIR fields: identifier, creator, description, version, license, creation date
4. **Validate standalone** — the extracted sub-graph must pass schema validation independently
5. **Document provenance** — source instance, extraction date, extraction criteria

### Cross-Instance Referencing

| Reference Type | Mechanism | Example |
|---------------|-----------|---------|
| Parent → child | Wikilinks (resolve within vault scope) | `[[child_repo/MANIFEST]]` |
| Child → parent | Explicit relative paths | `../../what/context/` |
| Sibling → sibling | External identifiers (URL, repo path) | `github.com/org/sibling-repo` |
| Lattice → lattice | URI scheme | `lattice://<instance_id>/path/to/node` |

Rules:
- Parent's CLAUDE.md Project Map SHOULD list child instances
- Child operates self-contained — need not know it's nested
- Cross-boundary sessions declare scope in session intent
- Follow each instance's rules within its boundary

### Interface Contracts

Use validation schemas as interface contracts between instances:

```yaml
# Schema shape defining what a shareable lattice must include
required_fields:
  - name
  - version
  - description
  - license
  - nodes (at least 1)
  - edges (at least 1)
  - federation:
      shareable: true
      source_instance: <instance_id>
      version_policy: <semver_range>
```

SHACL (W3C Shapes Constraint Language) provides formal shape definitions for RDF-based systems. For file-based systems, JSON Schema serves the same role — define the expected structure, validate at federation boundaries.

### FAIR Compliance for Shareable Artifacts

| Principle | Implementation |
|-----------|---------------|
| **Findable** | Unique identifier per artifact; registered in instance's lattice inventory |
| **Accessible** | Standard file format (`.lattice.yaml`); git-hosted or registry-published |
| **Interoperable** | Validates against published JSON Schema; uses standard entity types from base ontology |
| **Reusable** | Clear license in metadata; provenance (creator, source instance, creation method); version with semver |

## Anti-Patterns

- **Governance inheritance assumption.** Assuming child instances inherit parent rules leads to invisible inconsistencies. Each instance defines its own rules explicitly — no silent inheritance.
- **Full-graph replication.** Copying an entire knowledge graph to enable federation negates the point. Federation routes queries; it doesn't duplicate data.
- **Unnamespaced extensions.** Merging two instances that both define `type: task` with different schemas creates an irreconcilable collision. Namespace domain-specific types from the start.
- **Merge without base version check.** Combining instances at different base ontology versions produces an inconsistent merged schema. Always validate base compatibility first.
- **Implicit composition.** A child instance appearing inside a parent directory without documentation in the parent's Project Map creates discovery failures. Document all composition relationships explicitly.
- **Cross-boundary writes without scope declaration.** An agent modifying files in both parent and child instances without declaring cross-boundary scope in the session file creates audit gaps.

## Sources

- [aDNA Bridge Patterns](https://github.com/LatticeProtocol/adna) — Companion to aDNA Standard v2.0. Composition patterns (nesting, sibling, monorepo), discovery protocol, scope boundaries, cross-referencing conventions.
- [SPARQL 1.1 Federation Extensions](https://www.w3.org/TR/sparql11-federated-query/) — W3C (2013). SERVICE keyword for cross-endpoint queries.
- [Toward a Systematic Conflict Resolution Framework for Ontologies](https://pmc.ncbi.nlm.nih.gov/articles/PMC8352153/) — Keet (2021). 10 conflict types in 4 groups with fixed resolution strategies.
- [Modular Ontology Modeling (MOMo)](https://journals.sagepub.com/doi/10.3233/SW-222886) — Shimizu et al. Pattern-based modules, OPLa annotations, shared border concepts.
- [SHACL — Shapes Constraint Language](https://www.w3.org/TR/shacl/) — W3C (2017). Validation shapes as interface contracts between graphs.
- [The FAIR Guiding Principles](https://www.nature.com/articles/sdata201618) — Wilkinson et al. (2016). Findable, Accessible, Interoperable, Reusable data principles.
