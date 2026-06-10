---
type: context
title: "aDNA Design Document — Architecture Rationale"
created: 2026-02-13
updated: 2026-02-19
status: approved
last_edited_by: agent_init
tags: [adna, design, rationale, architecture, spec]
---

# aDNA Design Document

<!-- Companion to the aDNA Universal Standard v2.1 -->

## 1. Preamble

This document explains **why** aDNA is designed the way it is. It is the companion to the [aDNA Universal Standard](01_adna_standard.md), which defines **what** to do. A third piece — the [base templates](template_bare/) — provides the **how**: ready-to-use skeletons for bootstrapping new projects.

Together these form a three-document ecosystem:

| Document | Role | Audience |
|----------|------|----------|
| **aDNA Standard** (01_adna_standard.md) | Normative — MUST/SHOULD/MAY rules | Implementers building or maintaining an aDNA instance |
| **This design document** | Explanatory — rationale, trade-offs, worked examples | Evaluators deciding whether to adopt aDNA; adopters understanding intent |
| **Base templates** (template_bare/, template_embedded/) | Operational — empty shells with placeholders | Anyone bootstrapping a new aDNA project |

This document is self-contained. You do not need to read the five planning deliverables (00a–00d) that produced the 40 design decisions — though they are available in this directory for those who want the full deliberation record.

---

## 2. The Problem

AI agents start every session cold. They have no memory of previous sessions, no awareness of what other agents are doing, and no inherent understanding of the project they are operating in. This is a fundamental constraint, not a temporary limitation — even as models improve, the session boundary persists.

This creates four problems that compound in practice:

**Orientation overhead.** Every session begins with the agent asking: "What is this project? Where are things? What am I allowed to do?" Without deliberate architecture, agents spend significant context window budget simply figuring out where they are — or worse, they guess wrong and take actions based on incorrect assumptions.

**Coordination failure.** When multiple agents (or the same agent across sessions) modify the same project, they need to know what others have done and what is currently in progress. Without coordination infrastructure, agents silently overwrite each other's work or duplicate effort.

**Knowledge fragmentation.** Projects accumulate knowledge across sessions — domain context, decisions made, conventions established, lessons learned. Without a persistent knowledge layer, this knowledge lives only in session transcripts that no future agent will read. Each session re-derives what previous sessions already discovered.

**Audience divergence.** Humans and agents consume the same project knowledge but in fundamentally different ways. Humans browse, skim, and follow visual navigation cues. Agents parse, search, and follow structured metadata. A single set of documents optimized for one audience underserves the other.

aDNA addresses these problems through deliberate project knowledge architecture: a standard way to organize what a project knows, how it works, and who is involved — designed from the start for both human and AI consumption.

---

## 3. The Triad — Why Three

The core architectural decision in aDNA is the **what/how/who triad**: every piece of project knowledge belongs in exactly one of three categories.

| Leg | Question | Contains |
|-----|----------|----------|
| **what/** | WHAT does this project know? | Knowledge, context, decisions, reference, domain objects |
| **how/** | HOW does this project work? | Missions, sessions, templates, pipelines, processes |
| **who/** | WHO is involved? | People, teams, coordination, governance |

### Why three legs?

The triad emerges from a simple generative principle: **the question test**. Any piece of project content can be classified by asking which question it answers — WHAT, HOW, or WHO. Three questions, three categories, one clear home for every file. (Edge cases exist — some content could plausibly live in two legs. The question test resolves these by asking which question is PRIMARY, not whether other questions also apply.)

We considered and rejected other cardinalities:

**Two legs** (knowledge vs. operations, or content vs. process) creates sorting ambiguity. Where does a team roster go — is it "content" or "process"? Where do governance policies live — in "knowledge" or "operations"? Two-way splits force uncomfortable compromises because they conflate the people dimension into one of the other two.

**Four or more legs** were found unnecessary in design exploration. We tested candidate fourth legs — TOOLS (what we build with), WHERE (locations, deployments), WHEN (timelines, schedules) — and found that each decomposes cleanly into the existing three. Tools are knowledge about capabilities (what/). Deployment locations are either infrastructure knowledge (what/) or operational processes (how/). Timelines are operational planning (how/) or organizational milestones (who/). Adding legs past three created sorting ambiguity rather than resolving it.

We found three to be the minimum number that cleanly separates knowledge, process, and people. The "exactly one home" principle — every file belongs in exactly one leg — is what makes the system navigable. When an agent or human encounters a new piece of content, the question test produces one answer, not a debate.

### Worked example: classifying real content

Consider a project that manages machine learning models. Here is how different content sorts through the question test:

| Content | Question asked | Answer | Location |
|---------|---------------|--------|----------|
| "Our fine-tuned LLaMA model achieves 92% accuracy on the benchmark" | What do we know about our models? | WHAT | `what/models/` |
| "To deploy a model, follow these 5 steps..." | How do we deploy models? | HOW | `how/processes/` or `how/skills/` |
| "Alice is the ML lead; Bob reviews all model cards" | Who is responsible for what? | WHO | `who/team/` or `who/governance/` |
| "We decided to use LoRA instead of full fine-tuning because..." | What did we decide and why? | WHAT | `what/decisions/` |
| "Sprint plan: fine-tune 3 models this quarter" | How are we organizing the work? | HOW | `how/missions/` |
| "Meeting notes from the model review with the partner team" | Who met and what was communicated? | WHO | `who/communications/` |
| "Agent context: how ancient DNA extraction works" | What does the agent need to know about the domain? | WHAT | `what/context/` |

In every case, the question test yields one answer. The triad is not a filing system imposed on content — it is a design choice reflecting common dimensions of project knowledge (see spec S3.1).

---

## 4. Two Deployment Forms

aDNA has two first-class physical layouts: **bare** and **embedded**. This was the keystone design decision (C1) — everything structural flows from it.

### The insight: triad is ontology, not directory layout

The what/how/who triad is an intellectual framework for classifying project knowledge. How that framework manifests physically should respect the conventions of the environment it inhabits. A directory structure that makes sense at the root of an Obsidian vault would be foreign at the root of a Python package. Conversely, wrapping aDNA in a dot-prefixed directory makes no sense when aDNA IS the project.

This led to the **pattern-appropriate deployment** principle: one ontology, two physical forms.

### Bare triad

When aDNA IS the primary content — Obsidian vaults, knowledge bases, standalone agent workspaces — the triad directories sit at the project root alongside governance files:

```
my_vault/
├── CLAUDE.md
├── MANIFEST.md
├── STATE.md
├── what/          <- knowledge
├── how/          <- operations
├── who/          <- organization
└── {content}/    <- project-specific
```

This is natural for knowledge-first projects. The triad is visible, browsable, and immediately meaningful to both humans exploring in a file browser and agents parsing the directory tree.

### Embedded triad

When aDNA SERVES a codebase — git repositories, application projects, libraries — the triad is wrapped inside `.agentic/`, following the convention of dot-prefixed meta directories (`.github/`, `.vscode/`, `.docker/`):

```
my_repo/
├── CLAUDE.md     <- governance stays at root
├── MANIFEST.md
├── .agentic/
│   ├── what/      <- knowledge
│   ├── how/      <- operations
│   └── who/      <- organization
└── src/          <- codebase
```

Governance files remain at the root in both forms — this is the invariant. CLAUDE.md must be at root because Claude Code auto-loads it from there. The other governance files sit beside it for consistency and discoverability.

### Why not one form?

We considered mandating bare triad everywhere (simpler standard) and mandating embedded everywhere (uniform convention). Both failed:

- **Bare everywhere** means a Python repository has `what/`, `how/`, `who/` alongside `src/`, `tests/`, `pyproject.toml`. This pollutes the project namespace with directories that have nothing to do with the code. Developers rightly object — the aDNA infrastructure should not compete for attention with the actual project content.

- **Embedded everywhere** means a vault whose entire purpose is knowledge management wraps its content inside `.agentic/`. This hides the primary content behind a directory that signals "meta/configuration" rather than "this is the point." It also breaks Obsidian conventions — vault root should contain navigable content, not just a dot-directory.

Pattern-appropriate deployment accepts this reality: different project types have different norms, and the standard should respect them rather than fighting them. The triad ontology is identical in both forms — only the nesting differs. CLAUDE.md in each environment documents the paths, bridging the difference transparently (see spec S3).

The following diagram shows both deployment forms side by side. The triad ontology is identical — only the physical nesting differs:

```mermaid
flowchart TB
    subgraph BARE["Bare Triad (Knowledge Base)"]
        BR["project_root/"]
        BR --> BC["CLAUDE.md"]
        BR --> BW["what/"]
        BR --> BH["how/"]
        BR --> BO["who/"]
    end

    subgraph EMBED["Embedded Triad (Git Repo)"]
        ER["repo_root/"]
        ER --> EC["CLAUDE.md"]
        ER --> EA[".agentic/"]
        ER --> ES["src/"]
        EA --> EW["what/"]
        EA --> EH["how/"]
        EA --> EO["who/"]
    end

    BARE ---|"Same ontology<br/>Different packaging"| EMBED

    style BW fill:#0d9488,color:#fff
    style BH fill:#22c55e,color:#fff
    style BO fill:#8b5cf6,color:#fff
    style EW fill:#0d9488,color:#fff
    style EH fill:#22c55e,color:#fff
    style EO fill:#8b5cf6,color:#fff
```

### Worked example: same project, both layouts

A research lab documentation project could use either form:

**As a vault** (bare — the knowledge management is the point):
```
lab_docs/
├── CLAUDE.md
├── what/context/experimental_methods/  <- domain knowledge
├── what/decisions/adr_data_format.md   <- architecture decisions
├── how/missions/mission_v2_launch.md   <- release mission
├── who/team/member_dana.md             <- team roster
└── guides/                             <- project content
```

**As a repo** (embedded — the code is the point):
```
lab-platform/
├── CLAUDE.md
├── .agentic/
│   ├── what/context/             <- domain knowledge
│   ├── how/missions/             <- missions
│   └── who/governance/           <- governance
├── src/                          <- the actual application code
├── tests/
└── package.json
```

Same ontology, same governance files, same agent protocols — different packaging.

---

## 5. Five Governance Files

Every aDNA instance has up to five ALLCAPS files at root. These are the agent's orientation documents — the first things read on every session.

| File | What it answers | Update cadence |
|------|----------------|----------------|
| **CLAUDE.md** | "Who am I, where are things, what are the rules?" | When structure or protocols change |
| **MANIFEST.md** | "What is this project and how is it built?" | When scope or architecture changes |
| **STATE.md** | "Where are we right now?" | Every session close |
| **AGENTS.md** | "What does each directory contain?" | When structure changes |
| **README.md** | "How do I navigate this as a human?" | When onboarding changes |

### The cold-start problem

The primary design driver for governance files is cold-start orientation. An agent begins every session knowing nothing about the project. The governance files must take it from zero to productive within minutes. The critical path is:

1. **CLAUDE.md** (auto-loaded by Claude Code): The agent learns the project structure, its role, the safety rules, and how to begin a session.
2. **STATE.md**: The agent learns what phase the project is in, what happened recently, and what needs to happen next.

These two files — read in sequence — are sufficient for an agent to begin useful work. This is the Cold Start success criterion (see spec S18.1), and it was validated against both base template variants during Task 19.

```mermaid
sequenceDiagram
    participant A as Agent
    participant C as CLAUDE.md
    participant S as STATE.md
    participant Ses as sessions/active/
    participant Co as coordination/

    A->>C: 1. Auto-loaded on start
    Note over A,C: Learn structure, rules, persona
    A->>S: 2. Read current state
    Note over A,S: Learn phase, blockers, next steps
    A->>Ses: 3. Check active sessions
    Note over A,Ses: Detect conflicts
    A->>Co: 4. Read coordination notes
    Note over A,Co: Urgent cross-agent messages
    A->>Ses: 5. Create session file
    Note over A: Ready to work
```

### Why CLAUDE.md?

The name "CLAUDE.md" is a pragmatic choice, not a universal one. Claude Code auto-loads any file named CLAUDE.md from the project root. This auto-loading behavior is the single most valuable integration point — it means the agent's orientation document is always available without the agent needing to know to look for it.

We acknowledge this is model-specific (see spec Appendix C, deferred topic G2). A future revision may define a model-neutral convention — perhaps `.agentrc.md` or `AGENT.md` — that multiple AI tools auto-load. For now, the pragmatic value of auto-loading outweighs the purity of model-neutral naming. Projects using non-Claude agents can use the same structure with whatever filename their tooling auto-loads.

### Why MANIFEST.md and STATE.md are separate (D2)

Early designs combined project overview and current state into a single file. We separated them because they have fundamentally different update cadences:

- **MANIFEST.md** describes what the project IS — its architecture, entry points, major workstreams. This changes when you add a new subsystem or restructure the project. Weeks or months between updates.

- **STATE.md** describes where the project IS RIGHT NOW — current phase, recent decisions, active blockers, next steps. This changes every session close. Daily or more frequent updates.

Combining them means either the project overview gets cluttered with transient state, or the state section gets buried in stable architecture description. Separating them lets agents read STATE.md for "what changed recently?" without re-parsing the full project overview, and lets humans read MANIFEST.md for "what is this project?" without wading through operational status.

### The AGENTS.md / README.md split (C2)

Every directory in an aDNA instance can have two guide files:

- **AGENTS.md**: Optimized for machine consumption. Structured, scannable, focused on what an agent needs to know to operate in this directory — purpose, key files, patterns, conventions.

- **README.md**: Optimized for human browsing. Navigation-oriented, providing context for someone exploring in Obsidian, GitHub, or an IDE.

We chose dual files over a single combined document because the audiences genuinely need different things. An agent needs to know "what naming convention do files in this directory follow?" — structured and precise. A human needs to know "what will I find here and how does it connect to other parts of the project?" — contextual and navigational. A single document serving both audiences serves neither well.

The dual-file pattern adds maintenance cost — two files to update instead of one. We accept this trade-off because the alternative (one file, two audiences, constant compromise) proved worse in practice across 40+ sessions of operational experience (see spec S4.5, S4.6).

---

## 6. The Session Model

Sessions are aDNA's unit of accountability. Every modification to the project happens within a session, and every session leaves a record.

### Why sessions are structured

An agent operating without session structure modifies files, then the session ends. The next agent (or the same agent returning) has no record of what happened, what was in progress, or what should happen next. Session structure solves this by requiring three things:

1. **A session file exists before work begins** — this is the audit trail. If something goes wrong, the session file tells you who was working, what they intended, and what they touched.

2. **SITREP at close** — Completed, In Progress, Next Up, Blockers, Files Touched. This structured format ensures nothing falls through the cracks during handoff. It is deliberately concise — five fields, each with a clear purpose.

3. **Next-session prompt** — A self-contained paragraph that a fresh agent can read to continue the work. This is the single most valuable handoff mechanism: it compresses the full session context into what the next agent actually needs to know.

### Timestamped IDs over sequences

Session IDs use the format `session_{user}_{YYYYMMDD}_{HHMMSS}_{descriptor}`. We chose this over sequential numbering (S001, S002...) for three reasons:

- **Collision-free**: Two agents creating sessions simultaneously will never generate the same ID, because their usernames and timestamps differ.
- **Machine-sortable**: Alphabetical sort = chronological sort. No need for a registry to know which session came first.
- **Self-documenting**: The ID itself tells you who, when, and what — before you even open the file.

Sequential IDs require a shared counter, which introduces a coordination problem in distributed environments. Timestamps avoid this entirely (see spec S8.2).

### The 75% rule (D5)

The only universal sizing prescription is: scope each session to use approximately 75% of the context window, reserving 25% for thinking, debugging, and course correction.

We deliberately avoided other sizing guidance — time limits, task counts, line-count ranges — because these are paradigm-specific. A two-hour code generation session looks nothing like a two-hour knowledge synthesis session. The 75% rule applies regardless of paradigm because it addresses the universal constraint: context windows are finite, and agents that exhaust them cannot recover gracefully.

If a task requires more than 75% of the context window, the agent splits the work across sessions, checkpointing progress in the SITREP close-out. This is not a failure mode — it is the expected behavior for complex work (see spec S8.7).

---

## 7. Collision Prevention

Collision prevention is the system that keeps agents from silently destroying each other's work. It is tiered because different environments face different risks.

### The fundamental tension

AI agents cannot lock files. There is no mutex, no transaction, no compare-and-swap. When an agent reads a file, another agent (or human) might modify it before the first agent writes back. In sync environments like Google Drive, there is not even a notification that a conflict occurred — last write wins, silently.

This means collision prevention must be cooperative, not enforced. Agents follow conventions because the standard tells them to, not because a system prevents violations. This is an honor system — and we designed it to work as one, with multiple layers of defense rather than a single point of enforcement.

```mermaid
flowchart TB
    Start["Agent wants to<br/>modify a file"] --> Read["Read current content"]
    Read --> Check{"updated = today<br/>AND different author?"}
    Check -->|No| Safe["Write with<br/>frontmatter attribution"]
    Check -->|Yes| Ask["Confirm with user<br/>before overwriting"]
    Ask -->|Approved| Safe
    Ask -->|Denied| New["Create new file instead<br/>(zero collision risk)"]
    Safe --> Done["Update last_edited_by<br/>+ updated fields"]

    style Safe fill:#22c55e,color:#fff
    style Ask fill:#eab308,color:#000
    style New fill:#3b82f6,color:#fff
```

### Tier 1 — Universal (every aDNA instance)

Three rules that work everywhere:

1. **Frontmatter attribution**: Every file modification updates `last_edited_by` and `updated` in YAML frontmatter. This creates a visible "who touched this last?" signal that any tool can read.

2. **Read-before-write**: Always read the current file content immediately before writing. Never rely on a cached read from earlier in the session. This minimizes the window during which a conflict can occur.

3. **New-file safety**: Creating a new file has zero collision risk. When in doubt about modifying an existing file, consider creating a new one instead.

These three rules cost almost nothing — a frontmatter field update and a file read — and catch the most common collision scenario: an agent overwriting changes it did not know about. Even in git repositories where version control provides a safety net, Tier 1 attribution is valuable because it provides at-a-glance "who and when" without needing `git log` (see spec S13.2).

### Tier 2 — Sync environments

Google Drive, Dropbox, and similar sync systems add a specific risk: renames and moves can cause file duplication or loss during sync. Tier 2 adds:

- **Safety tiers for files**: Content files are Safe (low collision risk — different users work on different records). Governance files are Shared Config (medium risk — everyone might need to edit CLAUDE.md). Auto-generated files like `workspace.json` are Volatile (do not attempt to maintain them).

- **Archive-don't-rename**: Move deprecated files to `archive/` rather than renaming them. Sync systems handle renames poorly — a rename on one machine can appear as a delete-and-create on another, potentially duplicating or losing the file.

- **One config at a time**: When editing shared configuration files, complete one edit and verify it synced before starting the next. This prevents race conditions on files that multiple users/agents might touch.

### Tier 3 — Multi-agent

When multiple agents operate simultaneously on the same project, Tier 3 adds strategic coordination:

- **Coordination notes** in `who/coordination/` — explicit messages between agents about intentions, urgency, and scope.
- **Session scope declarations** — a Tier 2 session declares which files or directories it will modify, so other agents know to avoid those areas.
- **Update-field check** — before modifying a file where `updated` is today and `last_edited_by` is someone else, confirm with the user before overwriting.

### Why we rejected enforcement

We considered implementing file-locking mechanisms, mandatory check-out protocols, or database-backed coordination. All were rejected because:

- They add infrastructure dependencies that conflict with aDNA's design goal of working with plain files and directories.
- They create failure modes (stale locks, abandoned checkouts) that are worse than the collisions they prevent.
- They do not work across all environments — Google Drive has no locking API accessible to agents.

The tiered honor system works because it matches real usage patterns: most projects are single-agent most of the time (Tier 1 suffices), some projects sync across machines (Tier 2 helps), and a few projects have concurrent agents (Tier 3 provides the additional coordination). Projects adopt only the tiers they need (see spec S13).

### Worked example: two agents, one vault

**Setup**: Agent A (on Machine 1) and Agent B (on Machine 2) both start sessions on the same infrastructure knowledge base, synced via file sync.

**Tier 1 in action**: Both agents create their own session files (new files — zero collision risk). Agent A modifies `what/context/networking/vpc_design.md` — updates `last_edited_by: agent_alpha` and `updated: 2026-03-15`. Agent B reads that file and sees it was just modified today by someone else. The update-field check (Tier 3) fires: Agent B asks its user before overwriting.

**Tier 2 in action**: Agent A needs to update CLAUDE.md. It is classified as Shared Config. Agent A edits it, verifies the write, then moves on. Agent B, following the "one config at a time" rule, waits until its next session to propose CLAUDE.md changes, or notes the desired change in `who/coordination/` for Agent A to see.

**Tier 3 in action**: Agent A creates a coordination note: "Working on what/context/networking/ this session — please avoid." Agent B reads this during startup, routes its work to `how/missions/` instead, and leaves a reply note: "Updated the Q2 deployment plan, FYI."

No file locks. No central server. Just conventions, frontmatter, and coordination notes — and the vault stays consistent.

---

## 8. Content-as-Code and Extensions

aDNA includes several optional systems beyond the core triad and governance files. The design philosophy behind these extensions is consistent: **document the paradigm, not the instance**.

### Folder-equals-state (D14)

The content-as-code paradigm is simple: a file's directory location IS its processing state. Moving a file from `inbox/` to `processing/` to `review/` to `done/` advances it through a workflow. No separate status database. No state machine. The filesystem is the state machine.

This paradigm is universal — it works for research ingestion, document review, approval workflows, publishing pipelines, or any process where content flows through stages. The standard documents the paradigm and the directory structure convention (`how/pipelines/{name}/` with stage subdirectories, each containing an AGENTS.md with processing instructions). Specific pipelines are project-specific instances of the pattern.

We made pipelines optional rather than required because not every project has staged workflows. A simple knowledge base may never need a pipeline. But when you do need one, the pattern is defined and consistent (see spec S14).

```mermaid
stateDiagram-v2
    direction LR
    [*] --> inbox
    inbox --> processing: Agent picks up
    processing --> review: Work complete
    review --> done: Approved
    review --> processing: Needs revision

    note left of inbox: File location<br/>= processing state
    note right of done: No separate<br/>status database
```

### Graduated skeletons (D11)

Templates and directory structure grow with the project:

- **Starter**: 3 templates (session, mission, context), minimal directories. Enough for a single-agent project getting started.
- **Standard**: Adds coordination, backlog, and ADR templates. For active multi-agent projects.
- **Full**: Project-specific additions — experiment registries, model catalogs, pipeline stages. For mature operations.

We rejected a flat "include everything" approach because it overwhelms new projects with structure they do not yet need, and a minimal "include nothing" approach because it provides no guidance on how to grow. The graduated model lets projects start light and add structure as complexity demands (see spec S12).

### Machine registry in what/, not how/

The machine registry — tracking which machines sync the project and their path patterns — lives in `what/hardware/machines/`, not `how/`. This is the triad question test in action: "What machines does this project run on?" is a WHAT question (knowledge), not a HOW question (process). The machine registry is a catalog of facts about infrastructure, not an operational procedure (see spec S19.1).

---

## 9. Frontmatter as Integration Layer

aDNA requires YAML frontmatter on all triad content files and governance files, but NOT on project source code. This boundary (C4) is deliberate.

### The boundary principle

Files inside the triad (`what/`, `how/`, `who/`) and governance files benefit from frontmatter because they are queried, filtered, and aggregated. An agent needs to find "all missions with status active" or "all context files updated this week." Frontmatter makes these queries trivial — any tool that reads YAML can answer them.

Project source code does not benefit from frontmatter. A Python file does not need `type: source` and `updated: 2026-02-13` in a YAML block — git handles attribution, and source files are organized by code structure, not by knowledge taxonomy. Requiring frontmatter on source code would create friction without value.

The boundary is the triad perimeter. Inside the triad: frontmatter mandatory. Outside: frontmatter exempt. This keeps the requirement focused where it adds value (see spec S7.1).

### Frontmatter as universal API

The five required base fields (`type`, `created`, `updated`, `last_edited_by`, `tags`) form a universal API that any tool can consume:

- **Obsidian Dataview** queries frontmatter to build dashboards and aggregation views.
- **Shell scripts** parse YAML to generate reports or validate compliance.
- **CI/CD pipelines** can read frontmatter to check session status or mission progress.
- **Agents** use frontmatter to understand file purpose, recency, and authorship without reading full content.

This is the three-tier tool integration model (C13): Tier 1 (files and directories) works universally. Tier 2 (frontmatter queries) works with any YAML-reading tool. Tier 3 (Obsidian plugins, IDE extensions) is environment-specific. Everything in aDNA is Tier 1 unless noted otherwise — the standard does not require any particular tooling beyond a filesystem and a text editor (see spec S16).

---

## 10. Persona as Optional Architecture

aDNA provides a persona framework — a structured way to define an agent's identity, operating style, and communication norms. It does not require any specific persona.

### The consistency argument

A persona provides session-to-session consistency. Without one, each agent session establishes its own tone, greeting style, and behavioral norms. With a persona, the agent behaves predictably — it greets the same way, structures reports the same way, and follows the same behavioral principles every session. For long-running projects with dozens or hundreds of sessions, this consistency is valuable. It reduces cognitive load for the humans working with the agent.

### The universality problem

Not every project wants the same persona. A project persona — for example, a military-operational chief-of-staff, a scholarly research assistant, or a fast-moving startup co-builder — should match the project's character. A research lab might want a meticulous librarian. A documentation project might want a patient educator. Mandating any single persona would be inappropriate outside the specific context where it was designed.

### The framework solution

The standard defines the SHAPE of a persona, not its CONTENT:

- **Identity**: Name, role metaphor, mission statement.
- **Operating style**: 3-5 behavioral principles.
- **Communication norms**: Tone, formatting, greeting and closure patterns.
- **Domain awareness**: What the persona should know about the project.

A reference implementation — a fully worked example — demonstrates how to fill the framework. Projects adopt it directly, modify it, or create their own. The framework survives regardless of the specific persona chosen (see spec S4.2 and Appendix A).

```mermaid
flowchart TB
    P["Persona Framework"]
    P --> ID["Identity<br/>Name, role, mission"]
    P --> OS["Operating Style<br/>3-5 behavioral principles"]
    P --> CN["Communication Norms<br/>Tone, format, greetings"]
    P --> DA["Domain Awareness<br/>Project-specific context"]

    ID --> EX1["e.g. Chief of Staff<br/>to the operation"]
    OS --> EX2["e.g. Orient first,<br/>think in lines of effort"]
    CN --> EX3["e.g. Direct, SITREP format,<br/>no filler"]

    style P fill:#8b5cf6,color:#fff
```

---

## 11. Evolution and Deferred Design

aDNA v1.0 is deliberately scoped. Several topics were identified during the planning arc, evaluated, and intentionally deferred — not forgotten, but set aside until operational experience provides better design input.

### What was left out and why

Five topics were deferred to future revisions:

| Topic | Why deferred | Unlock condition |
|-------|-------------|-----------------|
| **Multi-model naming** (G2) | "CLAUDE.md" works today via auto-loading. Model-neutral naming requires ecosystem convergence that has not happened yet. | Multiple AI tools adopting a shared convention for auto-loaded project files. |
| **Documentation generation** (G3) | Generating external docs from aDNA is project-specific. No universal pattern has emerged. | Two or more projects developing similar patterns, suggesting standardization value. |
| **Context staleness detection** (G7) | The `updated` field + session cycling naturally refresh context. Formal detection is tooling, not architecture. | Operational evidence that natural refresh is insufficient for a common use case. |
| **Cross-instance awareness** (G8) | Addressed by bridge patterns — informational companion with SHOULD-level guidance for nesting, sibling composition, and monorepo patterns. | At least two aDNA instances needing to interoperate. |
| **Agent capability declaration** (G10) | Most aDNA instances target specific agent capabilities. Formal schemas are premature. | Broader agent ecosystem maturity and standardization of capability descriptions. |

### Why v1.0, not v0.1

This standard was validated through implementation. Tasks 12-19 applied every major design decision to two real systems — a knowledge base vault with 300+ files and 45+ sessions, and a git repository with 600+ files and 40+ sessions. The base templates (Tasks 18-19) passed Cold Start, Handoff, and Spec Compliance validation. This is not a theoretical design — it is an operational one.

The aspirational success criteria (spec S18.3) — network awareness, collision safety under heavy contention, dual-audience excellence — represent where we want aDNA to go, not what it must achieve today. They are guideposts for future revisions.

### The CLAUDE.md naming question

The decision to name the primary governance file "CLAUDE.md" is the clearest example of aDNA's design philosophy: **pragmatism over purity**. The pure choice would be a model-neutral name like `AGENT.md`. The pragmatic choice is the name that auto-loads in the tool most aDNA instances will use today. We chose pragmatism, documented the trade-off, and deferred the purity question to a future revision when the ecosystem may have converged on a model-neutral convention. This is the kind of trade-off aDNA makes throughout: optimize for today's operational reality while designing for tomorrow's evolution.

---

## 12. Acknowledgments

aDNA v1.0 emerged from the convergence of three systems: a knowledge base vault shaped by 45+ operational sessions, a git repository with 600+ spec-generated files, and an original genesis prompt encoding 30 aspirational architectural concepts. The standard preserves what worked from each, resolves where they diverged, and fills what was missing.

The planning arc spanned five sessions, producing 40 design decisions (15 structural, 25 process/pattern), a 40-row divergence map, and a 12-item gap registry. Execution spanned eight phases across 12+ sessions, validated against both deployment forms. The full deliberation record — reconnaissance, gap analysis, and design session deliverables — is available in this directory for those who want the complete rationale chain.

---

*End of aDNA Design Document*
