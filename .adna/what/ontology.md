---
type: ontology
created: 2026-02-20
updated: 2026-03-01
status: active
last_edited_by: agent_init
tags:
  - ontology
  - architecture
  - adna
entity_count: 14
base_version: "v3.0"
quality_score: 4.2
signal_density: 5
actionability: 4
coverage_uniformity: 4
source_diversity: 3
cross_topic_coherence: 5
freshness_category: durable
last_evaluated: 2026-02-20
banner: "who/assets/banners/banner_what.jpg"
icon: share-2
---

# aDNA Base Ontology

Entity relationship map for an aDNA instance. Defines the **14 base entity types** universal to every aDNA lattice, organized by the `who/what/how` triad.

**Base ontology version**: v3.0 (14 entity types)

## Scope

The aDNA ontology has two layers:

| Layer | Entity Types | Rule |
|-------|-------------|------|
| **Base** (this document) | 14 types | Structurally invariant — every aDNA instance shares these. No renaming, removal, or triad reassignment. |
| **Extensions** (per instance) | Additive | Namespaced, domain-specific. Extensions plug into base types but never modify them. See [Extension Patterns](#extension-patterns). |

This artifact documents the base layer in full. Extensions are shown as illustrative examples only — each instance defines its own.

---

## Base Entity Types

### Summary Table

| # | Entity | Triad | Directory | Purpose | Merge Behavior |
|---|--------|-------|-----------|---------|----------------|
| 1 | governance | WHO | `who/governance/` | Rules, charter, naming conventions, policies | invariant |
| 2 | team | WHO | `who/team/` | People who work — profiles, roles, groups | invariant |
| 3 | coordination | WHO | `who/coordination/` | Cross-agent/cross-session sync notes | invariant |
| 4 | context | WHAT | `what/context/` | Knowledge library — domain topics, research | invariant |
| 5 | decisions | WHAT | `what/decisions/` | ADRs — architectural/design decisions | invariant |
| 6 | modules | WHAT | `what/modules/` | Executable units with I/O contracts | invariant |
| 7 | lattices | WHAT | `what/lattices/` | Composition graphs of modules + datasets | invariant |
| 8 | campaigns | HOW | `how/campaigns/` | Strategic multi-mission initiatives | invariant |
| 9 | missions | HOW | `how/missions/` | Decomposed multi-session tasks | invariant |
| 10 | sessions | HOW | `how/sessions/` | Execution tracking — one per work session | invariant |
| 11 | templates | HOW | `how/templates/` | File templates for consistent structure | invariant |
| 12 | skills | HOW | `how/skills/` | Reusable agent recipes + procedures | invariant |
| 13 | pipelines | HOW | `how/pipelines/` | Folder-based content-as-code workflows | invariant |
| 14 | backlog | HOW | `how/backlog/` | Ideas and improvement tracking | invariant |

**Merge behavior**: All 14 base types are `invariant` — during [ontology unification](docs/ontology_unification.md), base types are never renamed, removed, or reassigned. Only extension types use `extension/namespace` merge behavior.

### Triad Structure (Diagram 1)

```mermaid
erDiagram
    WHO ||--o{ governance : contains
    WHO ||--o{ team : contains
    WHO ||--o{ coordination : contains

    WHAT ||--o{ context : contains
    WHAT ||--o{ decisions : contains
    WHAT ||--o{ modules : contains
    WHAT ||--o{ lattices : contains

    HOW ||--o{ campaigns : contains
    HOW ||--o{ missions : contains
    HOW ||--o{ sessions : contains
    HOW ||--o{ templates : contains
    HOW ||--o{ skills : contains
    HOW ||--o{ pipelines : contains
    HOW ||--o{ backlog : contains
```

### Key Entity Attributes

```mermaid
erDiagram
    context {
        string subtype "context_research | context_guide | context_core"
        int token_estimate "approximate token count"
    }

    campaigns {
        string status "planning | active | completed | abandoned"
        int phase_count "number of phases"
        int mission_count "number of missions"
    }

    skills {
        string skill_type "agent | process"
        string category "setup | research | development | operations"
    }

    modules {
        string module_type "tool | model | model_wrapper | preprocessor | postprocessor"
        string runtime "python3.10 | python3.11 | python3.12 | container"
        bool gpu_required "requires GPU"
    }

    lattices {
        string lattice_type "pipeline | agent | context_graph | workflow"
        string execution_mode "workflow | reasoning | hybrid"
        string execution_tier "L1 | L2 | L3"
    }

    sessions {
        string session_id "timestamped unique ID"
        int tier "1 or 2"
        string status "active | completed"
    }

    team {
        string role "functional role category"
        string agent_id "agent identity for attribution"
        string status "active | onboarding | alumni"
    }
```

---

## Execution Hierarchy

The operational ontology encodes a strict execution hierarchy. Each level narrows scope — campaigns decompose into missions, missions into objectives, with sessions executing objectives.

### Hierarchy Diagram (Diagram 2)

```mermaid
flowchart TD
    C["Campaign\n~50K tokens"] --> P["Phase\n(logical grouping)"]
    P --> M["Mission\n~15K tokens"]
    M --> O["Objective\n~5K tokens"]
    O --> S["Session\n(executes objectives)"]

    style C fill:#8b5cf6,color:#fff
    style P fill:#a78bfa,color:#fff
    style M fill:#0d9488,color:#fff
    style O fill:#22c55e,color:#fff
    style S fill:#eab308,color:#000
```

**Hierarchy rules**:
- **Campaigns** contain missions (physically in `how/campaigns/campaign_<name>/missions/`)
- **Standalone missions** (no campaign) live in `how/missions/`
- **Objectives** are session-sized work units tracked within mission files and via task plugins
- **Sessions** claim and execute objectives, producing coordination notes as side effects

### Convergence Model

At each execution level, irrelevant knowledge is pruned — the working set decreases monotonically as specificity increases. This is the **convergent narrowing** property of aDNA.

**Token narrowing**:

| Level | Typical Scope | ~Tokens | Reduction |
|-------|--------------|---------|-----------|
| Instance (full vault) | All knowledge | ~500K | — |
| Campaign | Strategic initiative | ~50K | 90% |
| Mission | Decomposed task | ~15K | 70% |
| Objective | Single session work | ~5K | 67% |

**Entity-type narrowing** (worked example — an organization formation campaign):

| Level | Entity Types in Scope | Reduction |
|-------|----------------------|-----------|
| Full ontology | 32 types (14 base + 18 extension) | — |
| Campaign: org_formation | 22 types (CRM + Science pruned) | 32 → 22 (31%) |
| Mission: Role Architecture | 5 types (role, member, team, sessions, decisions) | 22 → 5 (77%) |
| Objective: Draft role charters | 2 types (role, member) | 5 → 2 (60%) |

At each level, the AGENTS.md routing mechanism selects the relevant subspace — load only what the current scope needs, skip everything else. For full detail see [context_adna_core_convergence_model](context/adna_core/context_adna_core_convergence_model.md).

---

## Base Entity Relationships (Diagram 3)

Cross-entity relationships among the 14 base types:

```mermaid
erDiagram
    %% === Execution Hierarchy ===
    campaigns ||--o{ missions : "contains"
    missions ||--o{ sessions : "tracked by"
    sessions ||--o{ coordination : "may produce"
    backlog }o--|| missions : "graduates to"

    %% === Knowledge Composition ===
    lattices }o--o{ modules : "composes"
    lattices }o--o{ lattices : "chains with"
    modules }o--o{ modules : "chains with"

    %% === Operational ===
    pipelines }o--o{ context : "produces"
    skills }o--o{ context : "produces"
    skills }o--o{ lattices : "may reference"

    %% === Structural ===
    templates }o--o{ sessions : "used by"
    templates }o--o{ missions : "used by"
    team }o--o{ governance : "operates under"
```

**Key relationship patterns**:

| Pattern | Entities | Relationship |
|---------|----------|-------------|
| **Execution** | campaigns → missions → sessions → coordination | Decompose → execute → sync |
| **Knowledge** | lattices ↔ modules, modules ↔ modules, lattices ↔ lattices | Compose → chain |
| **Operational** | pipelines/skills → context, skills → lattices | Produce knowledge, reference compositions |
| **Governance** | team ↔ governance | People operate under policies |
| **Lifecycle** | backlog → missions, templates ↔ sessions/missions | Ideas graduate, templates structure |

---

## Composition Concepts

The base ontology defines three related-but-distinct composition concepts:

| Concept | Location | Purpose | Implementation |
|---------|----------|---------|---------------|
| **Lattice** | `what/lattices/` | Technical object — DAG composition of modules for compute | YAML schema, protocol validation, federation |
| **Pipeline** | `how/pipelines/` | Operational workflow — folder-based content-as-code | File location = state, AGENTS.md per stage |
| **Skill** | `how/skills/` | Agent/human procedure — reusable capability recipe | Single-file or directory-based |

All three share the "graph of steps" concept but serve different layers: technical (lattice), operational (pipeline), and agent-native (skill).

---

## Extension Patterns

### How Extensions Work

Extensions are **additive and namespaced**. They plug into the base ontology without modifying it. The question test classifies new entity types: "Is this about WHAT we know, HOW we work, or WHO is involved?"

| Rule | Description |
|------|-------------|
| **Additive only** | Extensions add entity types — they never modify or remove base types |
| **Namespaced** | Extension types use `{domain}_{entity_type}` syntax to prevent cross-instance collisions |
| **Question test** | Determines triad assignment — one answer, one leg, one home |
| **Directory convention** | New entity types get their own subdirectory under the appropriate triad leg |

**Namespace syntax**: `{domain}_{entity_type}` — domain is 2-20 lowercase alphanumeric + underscore characters.

### Example: CRM Extension

A customer relationship management extension adds entity types to the WHO leg:

| Entity | Namespace | Triad | Directory | Purpose |
|--------|-----------|-------|-----------|---------|
| customers | `crm_` | WHO | `who/customers/` | External organizations and deals |
| contacts | `crm_` | WHO | `who/contacts/` | People at customer/partner orgs |
| projects | `crm_` | WHO | `who/projects/` | Deployment initiatives per customer |

### Example: Science Extension

A biotech/science extension adds entity types to the WHAT leg:

| Entity | Namespace | Triad | Directory | Purpose |
|--------|-----------|-------|-----------|---------|
| hardware | `bio_` | WHAT | `what/hardware/` | Compute infrastructure (L1/L2/L3) |
| datasets | `bio_` | WHAT | `what/datasets/` | FAIR-compliant data packages |

### Extension Diagram (Diagram 4)

```mermaid
erDiagram
    %% Base types (invariant)
    WHO ||--o{ governance : contains
    WHO ||--o{ team : contains
    WHO ||--o{ coordination : contains
    WHAT ||--o{ context : contains
    WHAT ||--o{ modules : contains
    WHAT ||--o{ lattices : contains

    %% CRM extension plugging into WHO
    WHO ||--o{ crm_customers : "extension"
    WHO ||--o{ crm_contacts : "extension"
    WHO ||--o{ crm_projects : "extension"
    crm_customers ||--o{ crm_contacts : "has"
    crm_customers ||--o{ crm_projects : "owns"

    %% Science extension plugging into WHAT
    WHAT ||--o{ bio_hardware : "extension"
    WHAT ||--o{ bio_datasets : "extension"
    lattices }o--o{ bio_datasets : "consumes"
    modules }o--o{ bio_hardware : "runs on"
```

---

## Ontology Unification

When aDNA instances integrate (e.g., importing a sub-lattice), their ontologies must be **unified** — base entities aligned, extensions reconciled, conflicts resolved.

### Base Invariance Rule

Base entity types are **structurally invariant** across all aDNA instances at the same base version:

| Property | Invariant? |
|----------|-----------|
| Entity type name | YES — no renaming |
| Triad assignment | YES — no reassignment |
| Directory location | YES — canonical paths |
| Base frontmatter fields | YES — always present |
| Execution hierarchy | YES — Campaign → Mission → Objective |
| Type-specific fields | NO — instances may add fields (additive only) |
| Extension relationships | NO — extensions may define new relationships |

### Merge Algorithm (4-Step Summary)

```mermaid
flowchart TD
    Start([Start Merge]) --> S1

    S1["Step 1: Validate\nBase version compatible?"]
    S1 -->|Yes| S2
    S1 -->|No| Halt([HALT: Upgrade required])

    S2["Step 2: Collect\nClassify extensions from both instances"]
    S2 --> S3

    S3["Step 3: Detect\nFind conflicts between extensions"]
    S3 --> S4

    S4["Step 4: Resolve\nNamespace + produce merged artifact"]
    S4 --> Done([Merged ontology\n+ provenance record])

    style S1 fill:#ef4444,color:#fff
    style S2 fill:#eab308,color:#000
    style S3 fill:#3b82f6,color:#fff
    style S4 fill:#22c55e,color:#fff
```

**Step details**:

1. **Validate** — Confirm both instances share the same base major version (e.g., v3.x). Incompatible versions require upgrade before merge.
2. **Collect** — Enumerate extensions from both instances. Classify each as source-only, target-only, or present in both.
3. **Detect** — For shared extensions, check for type name collisions, discriminator conflicts, relationship ambiguity, and field semantic mismatches.
4. **Resolve** — Apply namespace prefixes to conflicting extensions. Produce merged ontology with provenance record documenting every resolution.

### Namespace Quick Reference

| Namespace | Domain | Status |
|-----------|--------|--------|
| `crm_` | Customer relationship management | Active |
| `bio_` | Biotech / life science | Active |
| `formation_` | Organization formation | Active |
| `compute_` | Compute infrastructure | Available |
| `custom_` | User-defined | Available |
| `base_` | Reserved (base types are unprefixed) | Reserved |

For the full merge algorithm, conflict taxonomy, and worked examples, see [Ontology Unification Protocol](docs/ontology_unification.md).

---

## Cross-References

- [CLAUDE.md](../CLAUDE.md) — Vault structure map and agent protocol
- [aDNA Standard v2.1](docs/adna_standard.md) — Normative specification (§5.1 ontology artifact, §3 triad architecture)
- [Ontology Unification Protocol](docs/ontology_unification.md) — Formal merge algorithm, conflict taxonomy, namespace specification
- [Lattice Federation & Sharing Protocol](docs/lattice_federation.md) — Federation lifecycle, import triggers merge
- [aDNA Design Rationale](docs/adna_design.md) — Design decisions and deployment forms
- [Ontology Design Guide](context/adna_core/context_adna_core_ontology_design.md) — Prescriptive guide for extending the ontology
- [Convergence Model](context/adna_core/context_adna_core_convergence_model.md) — Token narrowing operational reference
- [what/AGENTS.md](AGENTS.md) — Knowledge layer directory index
- [how/AGENTS.md](../how/AGENTS.md) — Operations layer
- [who/AGENTS.md](../who/AGENTS.md) — Organization layer
