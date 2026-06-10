---
type: context_core
topic: adna_core
subtopic: entity_definitions
created: 2026-03-01
updated: 2026-03-17
sources: ["aDNA Standard v2.1 (§5, §7)", "Per-entity AGENTS.md protocol files"]
context_version: "1.0"
token_estimate: ~1600
last_edited_by: agent_init
tags: [context, adna_core, ontology, entity_types, definitions]
quality_score: 3.8
signal_density: 4
actionability: 4
coverage_uniformity: 4
source_diversity: 3
cross_topic_coherence: 4
freshness_category: durable
last_evaluated: 2026-03-17
---

# aDNA Core: Entity Definitions — 14 Base Types

Complete definitions for the 14 base entity types in the aDNA ontology. Each entry covers: definition, purpose, location, key fields, and relationships. Use `ontology_design` to add domain-specific extensions (e.g., `lab_experiment`, `crm_customer`).

**Execution hierarchy**: Campaign → Mission → Session. Campaigns contain missions. Sessions execute mission objectives.

## WHO Leg (3 types)

### 1. Governance

**Definition**: Organizational charter, values, decision rights, and foundational documents.

**Purpose**: Establish organizational identity, mission, values, and decision-making authority. Every other entity type operates within governance constraints.

**Location**: `who/governance/`

**Key fields**: `type: charter|governance`, `status: skeleton|active|ratified`

**Relationships**: `team` operates under `governance` rules; `governance` frames naming conventions and agent protocols used by all other entities.

### 2. Team

**Definition**: Internal team member and group records documenting roles, responsibilities, and agent identities.

**Purpose**: Track who is working on what, with what agent identity (`agent_<username>`) and functional role. Enables attribution via `last_edited_by` across the vault.

**Location**: `who/team/`

**Key fields**: `type: team_member`, `role`, `agent_id`, `status: active|onboarding|alumni`

**Relationships**: `team` → `projects` (contributes to); `team` → `governance` (operates under); `team` members attributed via `last_edited_by` in all vault files.

### 3. Coordination

**Definition**: Ephemeral cross-agent synchronization notes for state, handoffs, and urgent flags between agents operating simultaneously.

**Purpose**: Prevent collision and enable continuity when multiple agents are active.

**Location**: `who/coordination/`

**Key fields**: `type: coordination_note`, date-stamped filename pattern `note_YYYYMMDD_<topic>.md`

**Relationships**: `sessions` may produce `coordination` notes; agents read `coordination/` during startup; notes are ephemeral.

---

## WHAT Leg (4 types)

### 4. Context

**Definition**: Pre-synthesized reference documents in the context library that give agents domain knowledge scoped to a topic.

**Purpose**: Provide token-efficient, pre-filtered knowledge payloads agents load before domain tasks, avoiding repeated re-research. Organized by topic with per-subtopic files.

**Location**: `what/context/<topic>/context_<topic>_<subtopic>.md`

**Key fields**: `type: context_research|context_guide|context_core`, `topic`, `subtopic`, `token_estimate`, `context_version`, `sources`

**Relationships**: `pipelines` (context_engine) → produces `context`; `campaigns` and `missions` consume `context` before execution; each topic has an `AGENTS.md` routing file.

### 5. Decisions

**Definition**: Architecture Decision Records (ADRs) capturing significant design choices with context, rationale, and consequences.

**Purpose**: Record the "why" behind major technical and organizational decisions so future agents and humans don't re-litigate settled questions.

**Location**: `what/decisions/adr_NNN_short_description.md`

**Key fields**: `type: decision`, `adr_number`, `status: proposed|accepted|deprecated|superseded`

**Relationships**: `missions` and `campaigns` produce decisions when significant choices arise; superseded ADRs reference their replacement.

### 6. Modules

**Definition**: Self-contained executable computation units — the atomic building blocks of lattices. Encompasses tools, ML models, model wrappers, preprocessors, postprocessors, and MCP servers.

**Purpose**: Document and catalog every reusable executable unit so lattices can compose them with defined I/O contracts.

**Location**: `what/modules/module_<name>.md`

**Key fields**: `type: module`, `module_type: tool|model|model_wrapper|preprocessor|postprocessor|mcp_server`, `runtime`, `gpu_required`, `category`

**Relationships**: `lattices` compose `modules` as nodes; `modules` run on `hardware`; `modules` consume `datasets`.

### 7. Lattices

**Definition**: Context graphs connecting datasets and modules into executable systems — the top-level composition primitive. Defined by `.lattice.yaml` files.

**Purpose**: Define how modules and datasets are wired together into runnable, federated, shareable workflows.

**Location**: `what/lattices/lattice_<name>.md`

**Key fields**: `type: lattice`, `lattice_type: pipeline|agent|context_graph|workflow|infrastructure|context_set|skill`, `execution.mode`, `execution.runtime`

**Relationships**: `lattices` compose `modules`; `lattices` consume `datasets`; `lattices` chain with other `lattices` via federation.

---

## HOW Leg (7 types)

### 8. Campaigns

**Definition**: Multi-mission strategic initiatives that coordinate large-scale work across phases, with mission containment and phase gates requiring user approval.

**Purpose**: Provide strategic framing, mission sequencing, and progress tracking for initiatives spanning many sessions.

**Location**: `how/campaigns/campaign_<name>/campaign_<name>.md` (with `missions/` subdirectory)

**Key fields**: `type: campaign`, `campaign_id`, `status: planning|active|completed|abandoned`, `phase_count`, `mission_count`

**Relationships**: `campaigns` contain `missions`; `campaigns` consume `context`; `campaigns` reference `decisions`; `backlog` ideas graduate into `campaigns`.

### 9. Missions

**Definition**: Multi-session task decompositions that break work too large for one session into session-sized objectives.

**Purpose**: Enable continuity and accountability across sessions. Each objective is claimed by one session at a time.

**Location**: `how/missions/` (standalone) or `how/campaigns/campaign_<name>/missions/` (campaign-linked)

**Key fields**: `type: plan`, `plan_id`, `status: active|completed|abandoned`; per-objective: `status: planned|in_progress|completed|skipped`

**Relationships**: `campaigns` contain `missions`; `missions` are tracked by `sessions`; `backlog` ideas graduate to `missions`.

### 10. Sessions

**Definition**: Per-agent-invocation tracking files created before any vault modification, providing audit trail and collision detection.

**Purpose**: Every agent session is an auditable unit — sessions record intent, files touched, and produce a SITREP on closure.

**Location**: `how/sessions/active/` (running) → `how/sessions/history/YYYY-MM/` (completed)

**Key fields**: `session_id`, `user`, `status: active|completed`, `intent`, `files_modified`, `files_created`

**Relationships**: `sessions` execute `mission` objectives; `sessions` may produce `coordination` notes.

### 11. Templates

**Definition**: Standardized file scaffolds for every entity type — ensuring consistent frontmatter, field coverage, and structure.

**Purpose**: Eliminate structural drift and reduce overhead when creating new records.

**Location**: `how/templates/` (HOW-leg templates) + per-directory template files

**Key fields**: Per-type template with required frontmatter fields

**Relationships**: `templates` used by `sessions`; templates exist for every entity type in the ontology.

### 12. Skills

**Definition**: Documented, reusable capabilities — either fully automated agent recipes (`skill_type: agent`) or human/hybrid procedures (`skill_type: process`).

**Purpose**: Encode institutional "how to do X" knowledge in a form agents can invoke reliably. Skills are formally interoperable with lattice objects (`lattice_type: skill`).

**Location**: `how/skills/skill_<name>.md`

**Key fields**: `type: skill`, `skill_type: agent|process`, `status: active|draft|deprecated`, `category`, `trigger`

**Relationships**: `skills` produce `context` (deep_research skill); `skills` may reference `lattices`; `skills` are invoked by `sessions` based on trigger conditions.

### 13. Pipelines

**Definition**: Folder-based content-as-code workflows where file location equals workflow state. Each stage directory contains an `AGENTS.md`; files advance by being moved.

**Purpose**: Provide stateless, observable, recoverable workflows without orchestrators or external state trackers.

**Location**: `how/pipelines/<pipeline_name>/` with numbered stage subdirectories

**Key fields** (on files in pipeline): `pipeline`, `stage`, `source_file`, `ingested`

**Relationships**: `pipelines` produce `context` (context_engine); `team` owns `pipelines`; `pipelines` support `campaigns`.

### 14. Backlog

**Definition**: Durable ideation intake — individual idea files capturing problems, proposals, and improvement opportunities that accumulate context before graduating into missions.

**Purpose**: Bridge between ephemeral coordination notes and committed missions. Structured funnel so good ideas aren't lost and premature missions aren't created.

**Location**: `how/backlog/idea_<short_name>.md`

**Key fields**: `type: backlog_idea`, `idea_id`, `title`, `category`, `status: proposed|discussed|planned|implemented|rejected`, `priority`, `effort`, `proposed_by`

**Relationships**: `backlog` → graduates to `missions` (via `plan_id` field on graduation); agents scan `backlog/` on session start.

---

## Summary Table

| # | Entity | Triad | Location |
|---|--------|-------|----------|
| 1 | governance | WHO | `who/governance/` |
| 2 | team | WHO | `who/team/` |
| 3 | coordination | WHO | `who/coordination/` |
| 4 | context | WHAT | `what/context/` |
| 5 | decisions | WHAT | `what/decisions/` |
| 6 | modules | WHAT | `what/modules/` |
| 7 | lattices | WHAT | `what/lattices/` |
| 8 | campaigns | HOW | `how/campaigns/` |
| 9 | missions | HOW | `how/missions/` + campaign dirs |
| 10 | sessions | HOW | `how/sessions/` |
| 11 | templates | HOW | `how/templates/` + per-dir |
| 12 | skills | HOW | `how/skills/` |
| 13 | pipelines | HOW | `how/pipelines/` |
| 14 | backlog | HOW | `how/backlog/` |

Domain-specific extensions follow the `{namespace}_{type}` pattern (e.g., `crm_customer`, `lab_experiment`). See `ontology_design` for the extension procedure and `ontology_workshop` for multi-entity domain design.

## Sources

1. aDNA Standard v2.1 — §5 (ontology), §7 (extensions)
2. Per-entity AGENTS.md protocol files
