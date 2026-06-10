---
type: docs
title: "Agentic-DNA Overview"
status: active
created: 2026-04-05
updated: 2026-05-11
last_edited_by: agent_stanley
moved_from: README.md
moved_at: 2026-05-11
moved_by: M03_S2_B0
tags: [docs, overview, aDNA, introduction]
---

# Agentic-DNA Overview

> **Provenance**: This file was the inner template `README.md` (aDNA specification +
> tutorial hybrid; ~47K of canonical aDNA documentation) pre-aDNA-v7.0. The v7.0 repo
> flatten (campaign_adna_v2_infrastructure M03 Session 2 2026-05-11 commit `B0`)
> retained both READMEs by moving this content to the docs directory while the
> public-facing GitHub landing README at repo root took the entry-point slot. See
> [the repo root README](../../README.md) for the GitHub landing page; this file is
> the deep-dive content surface. M03 README collision resolution per Operator Decision
> 4 (preserve both — outer at root, inner moves) recorded in the M03 mission spec
> §Operator decisions table.

---

**Give your project a knowledge architecture that both humans and AI agents can navigate.**

Every project accumulates knowledge — decisions, contacts, research, processes, context. Without structure, that knowledge fragments across chat logs, scattered docs, and individual memory. AI agents start every session cold, re-discovering what the project is and how it works.

**aDNA (Agentic DNA)** is a knowledge architecture that solves this. It organizes any project's knowledge into three directories — `who/`, `what/`, `how/` — with lightweight governance files that give AI agents instant orientation and give humans a browsable knowledge graph in [Obsidian](https://obsidian.md).

Clone this repo to get a ready-to-use aDNA vault with templates, tools, and examples. Customize it for your domain in minutes.

> *aDNA is a standalone knowledge architecture standard. It is the foundational building block of the [Lattice Protocol](https://github.com/LatticeProtocol/lattice-protocol) for federated AI compute — but the architecture is domain-neutral. Any project that uses AI agents (or just wants structured knowledge) benefits.*

---

## aDNA in 60 Seconds

Your project has three kinds of knowledge: **people** (contacts, teams, partners), **things you know** (research, decisions, designs), and **how you work** (plans, processes, workflows). aDNA gives each one a folder — `who/`, `what/`, `how/`.

Inside each folder, a small config file (`AGENTS.md`) tells AI agents what's here and how to work with it. When an agent opens your project, it reads the top-level config, then only the folder-level configs relevant to its task. Instead of reading everything, it reads just what it needs.

This means every new folder you add automatically narrows the search space for agents. Your project gets bigger, but each task stays focused. The structure filters out the noise so both humans and AI can find what matters fast.

No special tooling required. It's folders, Markdown files, and a handful of conventions — works with any editor, any AI agent, any version control.

---

## The Problem

AI agents start every session cold. No memory of past work, no awareness of other agents, no understanding of the project they're operating in. This creates four compounding failures:

| Failure | What happens |
|---------|-------------|
| **Orientation overhead** | Every session begins with the agent re-discovering project structure, conventions, and current state. Context windows fill with exploration instead of execution. |
| **Coordination failure** | Multiple agents (or humans + agents) work on the same project without shared protocol. They overwrite each other's work, duplicate effort, and produce inconsistent outputs. |
| **Knowledge fragmentation** | Insights discovered in one session are lost by the next. There's no persistent medium that accumulates project understanding across sessions and agents. |
| **Audience divergence** | Humans browse knowledge visually (folders, links, graphs). Agents parse knowledge programmatically (frontmatter, structured files, protocol files). Most projects serve one audience poorly or both terribly. |

aDNA solves these by giving projects a **deliberate knowledge architecture** — structured knowledge that both humans and agents can read, navigate, and build on.

---

## Who Is This For?

aDNA works for any project that manages knowledge. Here are four common use cases:

**Startup founder** — You're tracking investors, customers, product roadmap, hiring, and fundraising. Your `who/` leg holds investor profiles, customer records, and team members. Your `what/` leg holds product decisions, market research, and competitive analysis. Your `how/` leg holds fundraising campaigns, sprint plans, and onboarding processes. One vault replaces scattered Notion pages, Google Docs, and Slack threads.

**Researcher** — You're managing papers, datasets, experiments, and collaborations. Your `what/` leg holds literature reviews, dataset documentation, and methodology decisions. Your `who/` leg holds collaborators, lab members, and funding contacts. Your `how/` leg holds research missions, publication pipelines, and grant application workflows.

**Creative professional** — You're juggling clients, projects, creative assets, and revision cycles. Your `who/` leg holds client profiles and collaborator contacts. Your `what/` leg holds project briefs, asset libraries, and style guides. Your `how/` leg holds project workflows, revision pipelines, and delivery checklists.

**Personal knowledge manager** — You're organizing learning goals, reading notes, skills development, and personal projects. Your `what/` leg holds course notes, book summaries, and topic deep-dives. Your `how/` leg holds learning paths, habit tracking, and project plans. Your `who/` leg holds mentors, communities, and professional contacts.

Each of these users starts with the same base structure and extends it with domain-specific directories. See [Extending the Ontology](#extending-the-ontology) for how.

---

## The aDNA Paradigm

### The Triad

Every piece of project knowledge answers exactly one of three questions:

```
who/     →  Who is involved?                 (people, teams, organizations)
what/    →  What does this project know?     (knowledge, decisions, artifacts)
how/     →  How does this project work?      (processes, plans, operations)
```

This is the **triad** — three directories, three questions, complete coverage.

**The Question Test** classifies any content:

| Content | Question | Triad leg |
|---------|----------|-----------|
| A research paper summary | What do we know about X? | `what/` |
| The deployment checklist | How do we deploy? | `how/` |
| The engineering team roster | Who works on this? | `who/` |
| An architecture decision record | What did we decide? | `what/decisions/` |
| A campaign plan for Q2 launch | How do we execute Q2? | `how/campaigns/` |

Why three? Two legs create sorting ambiguity — people get conflated into either knowledge or process. Four or more legs were found unnecessary in practice; candidates like TOOLS, WHERE, and WHEN all decompose cleanly into the existing three. Three is the minimum that separates knowledge, process, and people without overlap.

### Two Deployment Forms

| Form | Structure | Use case |
|------|-----------|----------|
| **Bare triad** | `what/` · `how/` · `who/` at project root | Knowledge bases, Obsidian vaults, standalone projects |
| **Embedded triad** | `.agentic/what/` · `.agentic/how/` · `.agentic/who/` | Git repos where aDNA lives alongside source code |

This repo is a **bare triad** — the full aDNA experience. When adding aDNA to an existing codebase, use the embedded form so it doesn't collide with your source tree.

### Governance Files

Five files provide the structural skeleton:

| File | Audience | Purpose |
|------|----------|---------|
| **CLAUDE.md** | Agents | Master context — auto-loaded on session start. Project structure, safety rules, domain knowledge, agent protocol. |
| **MANIFEST.md** | Both | Project identity — what this project is, its architecture, entry points, active builds. |
| **STATE.md** | Both | Operational state — what's happening now, blockers, next steps. The live pulse of the project. |
| **AGENTS.md** | Agents | Per-directory guide — one in every directory telling agents what lives here and how to work with it. |
| **README.md** | Humans | Standard README — GitHub rendering, onboarding, external audience. |

Agents read `CLAUDE.md` → `STATE.md` → directory-level `AGENTS.md` files. Humans read `README.md` → `MANIFEST.md` → browse the triad. Same knowledge, two entry paths.

### How It All Fits Together

```mermaid
graph TB
    subgraph governance ["Governance Layer"]
        CLAUDE["CLAUDE.md<br/><i>agents</i>"]
        STATE["STATE.md<br/><i>both</i>"]
        MANIFEST["MANIFEST.md<br/><i>both</i>"]
        README["README.md<br/><i>humans</i>"]
        AGENTS["AGENTS.md<br/><i>per-directory</i>"]
    end

    subgraph triad ["The Triad"]
        WHO["who/<br/>People & orgs"]
        WHAT["what/<br/>Knowledge & artifacts"]
        HOW["how/<br/>Operations & process"]
    end

    subgraph execution ["Execution Hierarchy — Context Narrows"]
        CAMP["Campaign<br/>~50K tokens"]
        MISS["Mission<br/>~15K tokens"]
        OBJ["Objective<br/>~5K tokens"]
    end

    CLAUDE --> STATE
    STATE --> AGENTS
    AGENTS --> WHO
    AGENTS --> WHAT
    AGENTS --> HOW
    HOW --> CAMP
    CAMP --> MISS
    MISS --> OBJ
```

Each layer narrows what an agent loads. By the time work reaches an objective, the agent has exactly the context it needs — no more, no less.

---

## Glossary

Key terms used throughout this documentation:

| Term | Definition |
|------|-----------|
| **aDNA** | Agentic DNA — a knowledge architecture standard that organizes project knowledge into three directories (who/what/how) with governance files for both human and AI agent navigation. |
| **Triad** | The three-directory structure (`who/`, `what/`, `how/`) at the heart of aDNA. Every piece of project knowledge belongs in exactly one leg. |
| **Ontology** | The set of entity types your project uses (e.g., customers, decisions, sessions). aDNA ships 14 base types; you extend with your own. |
| **Lattice** | A YAML-defined directed graph that models a workflow, pipeline, or reasoning process. Lattices are optional — the triad works without them. |
| **FAIR** | Findable, Accessible, Interoperable, Reusable — metadata principles applied to lattices so they can be shared and discovered. |
| **Convergence model** | The way aDNA's execution hierarchy (Campaign → Mission → Objective) progressively narrows context, reducing token count while increasing signal density. |
| **AGENTS.md** | A per-directory guide file that tells AI agents what lives in a directory and how to work with it. Every directory in an aDNA project has one. |

---

## An Ontology for Building Your Ontology

Base aDNA ships **14 entity types** across the triad — the minimal operational ontology any project needs:

| Triad leg | Entities | Purpose |
|-----------|----------|---------|
| **WHO** (3) | `governance`, `team`, `coordination` | Who decides, who works, how they sync |
| **WHAT** (4) | `context`, `decisions`, `modules`, `lattices` | What you know, what you've decided, what you build, how you compose |
| **HOW** (7) | `campaigns`, `missions`, `sessions`, `templates`, `skills`, `pipelines`, `backlog` | Plan → decompose → execute → track → automate → ideate |

**You extend by adding domain-specific entities under the appropriate triad leg.** The base gives you operational infrastructure — sessions, missions, coordination — that works from day one. Your extensions add the domain knowledge that makes the project yours.

Here are some examples of how different teams extend the base:

| Domain | Example extensions | Triad leg |
|--------|-------------------|-----------|
| **Startup / Business** | `investors`, `customers`, `partners`, `fundraising_pipeline` | `who/` |
| **Research / Science** | `experiments`, `datasets`, `hypotheses`, `protocols` | `what/` |
| **Software team** | `services`, `incidents`, `deployments` | `how/` |
| **Creative agency** | `clients`, `creative_assets`, `revision_cycles` | `who/` + `what/` |
| **Personal learning** | `courses`, `books`, `learning_goals` | `what/` |

The triad doesn't prescribe your domain — it gives you the scaffold to build your domain ontology on.

### The Discriminator Pattern

When related entities share a directory, use a frontmatter field to distinguish them:

```yaml
# what/modules/tool_lattice_validate.md
type: module
module_type: tool        # ← discriminator

# what/modules/model_protein_binder.md
type: module
module_type: model       # ← discriminator
```

This keeps the directory structure flat while preserving semantic precision. The base ontology uses three discriminators: `module_type` (tool, model, preprocessor, ...), `lattice_type` (pipeline, agent, context_graph, workflow), and `skill_type` (agent, process).

---

## What's Inside

```
Agentic-DNA/
├── CLAUDE.md                           # Agent master context
├── MANIFEST.md                         # Project identity (customize this)
├── STATE.md                            # Operational state (customize this)
├── what/                               # Knowledge
│   ├── context/                        #   Context library (5 topics, 27 subtopics)
│   ├── decisions/                      #   Architecture Decision Records
│   ├── docs/                           #   aDNA specification documents
│   │   ├── adna_standard.md            #     Full normative spec (v2.2)
│   │   ├── adna_design.md              #     Architecture rationale
│   │   └── adna_bridge_patterns.md     #     Multi-instance composition
│   └── lattices/                       #   Lattice definitions
│       ├── lattice_yaml_schema.json    #     JSON Schema
│       ├── canvas_yaml_interop.md      #     Canvas ↔ YAML spec
│       ├── examples/                   #     15 example lattices + 3 canvas templates
│       └── tools/                      #     validate, convert, interop
├── how/                                # Operations
│   ├── templates/                      #   22 templates (10 auto-triggering)
│   ├── pipelines/prd_rfc/              #   R&D → PRD → RFC pipeline
│   ├── sessions/                       #   Session tracking
│   ├── campaigns/                      #   Multi-mission initiatives
│   ├── missions/                       #   Task decomposition
│   ├── skills/                         #   13 agent recipes & procedures
│   └── backlog/                        #   Ideas & improvements
├── who/                                # Organization
│   ├── coordination/                   #   Cross-agent notes
│   └── governance/                     #   Project governance
└── .obsidian/                          # Visual config (theme, snippets, plugins)
# Community infrastructure lives inside the triad:
#   how/quests/          — Side-quest specs + results
#   what/lattices/tools/ — Aggregation & analysis scripts
```

| Component | Location | What it does |
|-----------|----------|-------------|
| **Lattice tools** | `what/lattices/tools/` | Validate `.lattice.yaml` files, convert to/from Obsidian canvas |
| **JSON Schema** | `what/lattices/lattice_yaml_schema.json` | Formal schema for lattice definitions |
| **15 example lattices** | `what/lattices/examples/` | Business, research, creative, and biotech examples (+ 3 canvas templates) |
| **22 templates** | `how/templates/` | Session, mission, campaign, campaign mission, ADR, context, coordination, backlog, skill, PRD, RFC, AAR, lightweight AAR, governance, data record, folder note, registry, strategic compass, campaign CLAUDE.md, migration, side quest, quest result |
| **PRD/RFC pipeline** | `how/pipelines/prd_rfc/` | 4-stage content-as-code planning workflow |
| **aDNA spec docs** | `what/docs/` | Normative standard, design rationale, bridge patterns |
| **Obsidian config** | `.obsidian/` | Tokyo Night theme, CSS snippets, 15 community plugins + curated core set, Notebook Navigator as default file browser |

---

## Quick Start

**Clone and open: ~5 minutes.** Agent-guided customization: 15-30 minutes. Manual customization: 30-45 minutes.

> **What you'll have after 5 minutes**: A fully configured knowledge vault with the triad structure (`who/`/`what/`/`how/`), 22 templates, 15 example lattices, 15 Obsidian plugins, and governance files — ready for customization to your domain.

> **Why this matters for AI agents**: aDNA's directory structure acts as a routing system. Each level narrows what an AI agent needs to read — from your entire project down to a single task. Agents work faster, use fewer tokens, and produce more focused results.

### Prerequisites

- [Obsidian](https://obsidian.md) 1.0+ (free, all platforms)
- Python 3.6+ (optional — only needed for lattice YAML validation/conversion tools)

### 1. Get the vault

**Option A — Clone into `~/aDNA/` (recommended)**
```bash
mkdir -p ~/aDNA
cd ~/aDNA
git clone https://github.com/LatticeProtocol/aDNA.git adna
cd adna
```

This creates the canonical workspace layout. The `adna/` directory is the base template — you'll fork it into project directories, keeping the template clean for updates.

**Option B — Use as GitHub template**
Click **[Use this template](https://github.com/LatticeProtocol/aDNA/generate)** on GitHub to create your own copy with clean history. Clone the result into `~/aDNA/`.

### 2. Run setup (recommended)

For the best first experience, run setup before opening in Obsidian:

```bash
./setup.sh
```

This downloads all 15 community plugins, the Tokyo Night theme, and ships a curated workspace layout with a clean sidebar (Notebook Navigator as the default file browser, minimal ribbon icons).

> **Windows users**: Run `setup.sh` in Git Bash or WSL. Or install plugins manually via Settings → Community plugins → Browse.

### 3. Open in Obsidian

Open `adna/` as a vault in [Obsidian](https://obsidian.md). Enable community plugins when prompted.
15 community plugins and the Tokyo Night theme ship pre-installed. The core plugin set is curated — Notebook Navigator replaces the default file explorer, and Templater replaces the built-in templates plugin. Both originals are disabled but can be re-enabled in Settings → Core plugins.

The accent color (Rebecca Purple `#663399`) and CSS snippets activate automatically. Triad colors (purple/blue/green) appear as Lucide icons in tabs, links, and the sidebar.

Optionally install [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk) font — the vault falls back to system fonts without it.

> **Optional**: Run `./setup.sh --force` to re-download all plugins to latest versions.

### 4. Choose your setup path

> **Visual learner?** Open `what/lattices/examples/hello_world.canvas` in Obsidian to see a lattice as an interactive node graph — no YAML knowledge needed. Drag nodes, follow edges, and explore how datasets, modules, and processes connect.

**Option A: Agent-guided setup (recommended, ~15-30 min)**

Open a terminal in the vault directory and start Claude Code:

```bash
claude
```

**Berthier** — the vault's built-in agent personality — will detect this is the base template and guide you through workspace setup:

- Creates a workspace CLAUDE.md at `~/aDNA/`
- Helps you fork into your first project (e.g., `~/aDNA/my_research_lab.aDNA/`)
- Runs the 5-question onboarding interview inside your new project
- Customizes governance files, suggests domain extensions, offers personality customization

The base `adna/` template stays clean — all customization happens in your forked project. Run `git pull` inside `adna/` anytime to get framework updates. Everything Berthier does is inspectable — see `how/skills/skill_project_fork.md` and `how/skills/skill_onboarding.md`.

> **No Obsidian?** This path works entirely from the terminal — no Obsidian installation required. See [`what/docs/agent_first_guide.md`](what/docs/agent_first_guide.md) for the full agent-first walkthrough, including feature parity details and Claude Code configuration.

**Option B: Manual setup (~30-45 min)**

See [Using Without AI Agents](#using-without-ai-agents) below.

---

## Adding aDNA to an Existing Project

Already have a project? Don't clone — add aDNA structure to it. This takes 10-15 minutes and works with any codebase.

**Choose your form:**

| Form | Structure | Use when |
|------|-----------|----------|
| **Embedded** | `.agentic/who/` · `.agentic/what/` · `.agentic/how/` | Adding to a code repo — aDNA lives alongside source code |
| **Bare** | `who/` · `what/` · `how/` at root | aDNA IS the project — knowledge bases, documentation vaults |

**Minimum viable aDNA** — 5 files + 3 directories:

1. `CLAUDE.md` at project root — agent master context (always at root, never inside `.agentic/`)
2. `MANIFEST.md` at project root — project identity
3. `STATE.md` at project root — operational state
4. Three `AGENTS.md` files — one per triad directory
5. Three triad directories — `who/`, `what/`, `how/` (bare) or `.agentic/who|what|how/` (embedded)

```bash
# Embedded form — one command to create the structure:
mkdir -p .agentic/who .agentic/what .agentic/how
```

Then write your governance files using the starter templates in the full guide. Everything else — templates, sessions, campaigns, context library — is enhancement you add when you need it.

**Full walkthrough**: [`what/docs/migration_guide.md`](what/docs/migration_guide.md) — step-by-step instructions, starter templates, common pitfalls, and progressive enhancement path.

---

## Multi-Project Workspaces

The `~/aDNA/` workspace naturally supports multiple projects. Each project is a fork of the Agentic-DNA template with its own governance, git history, and domain customization. Forked projects use the `.aDNA` suffix to indicate they follow the aDNA standard (see Standard §3.5).

```
~/aDNA/
├── CLAUDE.md              # Workspace governance (auto-created on first run)
├── Agentic-DNA/           # Base template (never modified — role: template, no .aDNA suffix)
├── my_research_lab.aDNA/  # Project A (forked, customized)
├── client_acme.aDNA/      # Project B (forked)
├── latlab/                # (appears after L0→L1 upgrade)
└── lattice-protocol/      # (appears after L0→L1 upgrade)
```

Open Claude Code in `adna/` or at the workspace root, say "create a new project," and the agent forks the template and runs a 5-question onboarding interview to scaffold a fully configured project — domain-specific directories, personalized CLAUDE.md, populated MANIFEST.md and STATE.md.

**Working example**: [`what/docs/examples/adna-projects/`](what/docs/examples/adna-projects/) — two pre-scaffolded projects (biotech lab, enterprise pipeline) showing distinct interview outputs.

**Full pattern doc**: [`what/docs/projects_folder_pattern.md`](what/docs/projects_folder_pattern.md)

---

## Using Without AI Agents

aDNA works perfectly well as a human-only knowledge management system. The triad structure, templates, and Obsidian integration don't require AI agents at all.

### Manual setup in 5 steps

**1. Clone and install** — Follow Quick Start steps 1-3 above.

**2. Edit `MANIFEST.md`** — Replace the project description with your project's name and purpose. This file is your project's identity card — update it to describe what you're building.

**3. Edit `STATE.md`** — Replace the current phase and next steps with your own. This is your operational dashboard — use it to track what's happening now and what's next.

**4. Edit `CLAUDE.md` (optional)** — If you plan to use AI agents later, update the project description in the `## Identity & Personality` section. If not, you can ignore this file.

**5. Create your first content file** — Pick the triad leg that matches your first piece of knowledge and create a file:
   - A decision? Create `what/decisions/adr_your_decision.md`
   - A team member? Create `who/governance/team_member_name.md`
   - A project plan? Create `how/missions/plan_your_project.md`

Use the templates in `how/templates/` as starting points — each one has the required frontmatter fields pre-filled.

### What you can skip for solo use

- **Session tracking** — designed for multi-agent coordination. For solo human use, it's optional.
- **Collision prevention** — the `updated` / `last_edited_by` fields prevent multi-agent conflicts. Solo users can still use them as an audit trail, but they're not critical.
- **AGENTS.md files** — these are per-directory guides for AI agents. As a human, browse directories directly in Obsidian — the AGENTS.md files won't get in the way.
- **Lattices** — YAML workflow definitions for executable pipelines. Useful for computational work, but the triad handles knowledge management without them.

---

## Working with AI Agents

aDNA is designed for **human-agent collaboration**. The architecture serves both audiences simultaneously.

### Agent Orientation

When an AI agent (Claude Code, Cursor, etc.) opens an aDNA vault, it reads `CLAUDE.md` and immediately understands:

- Project structure and where to find things
- Safety rules and what not to touch
- Active state — what's in progress, what's blocked
- Session protocol — how to track its work
- Domain knowledge — project-specific context

No prompt engineering required. The architecture *is* the prompt.

When an agent first opens a fresh vault, it runs an interactive onboarding flow to help customize the vault for your project.

### Session Tracking

Every agent session creates a file in `how/sessions/active/` before modifying vault files:

| Tier | When | What's tracked |
|------|------|---------------|
| **Tier 1** | Default for most work | Session ID, intent, files touched |
| **Tier 2** | Shared config edits | Adds scope declaration, conflict scan, heartbeat |

On completion, sessions close with a **SITREP** — a structured handoff:

- **Completed** — what got done
- **In progress** — what's started but unfinished
- **Next up** — recommended next actions
- **Blockers** — anything preventing progress
- **Files touched** — full audit trail

The next agent reads the last SITREP and picks up where the previous one left off. Knowledge compounds instead of evaporating.

### Team Use — Multi-User Vaults

For teams sharing a vault via git, install the [Obsidian Git](https://github.com/denolehov/obsidian-git) community plugin. Recommended settings:

- **Auto-commit interval**: 10 minutes (Settings → Obsidian Git → Automatic)
- **Auto-pull on open**: enabled (pulls latest changes when Obsidian starts)
- **Pull on open**: enabled

Per-device files (`workspace.json`, `graph.json`) should be excluded via `.gitignore` to prevent merge conflicts. The vault ships with these exclusions pre-configured.

For onboarding new team members, the vault includes a `workspace.default.json` — a curated layout with Notebook Navigator as the default sidebar, clean ribbon, and a pinned home page. New members run `cp .obsidian/workspace.default.json .obsidian/workspace.json` before opening in Obsidian.

### The Execution Hierarchy

For work larger than a single session:

```
Campaign  (strategic initiative — weeks to months)
├── Phase  (logical grouping with human gate between phases)
│   ├── Mission  (multi-session task — 1-5 sessions)
│   │   ├── Objective  (session-sized unit of work)
│   │   └── Objective
│   └── Mission
└── Phase
```

- **Campaigns** coordinate multiple missions toward a strategic goal
- **Missions** decompose complex tasks into claimable objectives
- **Objectives** are what actually get done in a session
- **Phases** group missions with human approval gates between them

Each level narrows the context an agent needs to load. A campaign might reference 50K tokens of project knowledge. A mission within it needs ~15K. A single objective within that mission needs ~5K. This progressive narrowing means agents spend tokens on *doing the work*, not re-reading the entire project. See [How It All Fits Together](#how-it-all-fits-together) for the visual version.

### Cross-Agent Coordination

When multiple agents work on the same project, they coordinate through `who/coordination/` — structured notes that flag dependencies, handoffs, and blockers. Each agent checks coordination on startup, before starting work.

---

## Frequently Asked Questions

### Do I need Obsidian to use aDNA?

No. aDNA is a directory convention — `who/`/`what/`/`how/` with Markdown files and YAML frontmatter. Any text editor or Markdown tool works. Obsidian adds visual browsing (graph view, wikilink navigation, canvas), but the structure is plain files on disk. AI agents like Claude Code work with the files directly regardless of editor. For a complete terminal-first walkthrough, see [`what/docs/agent_first_guide.md`](what/docs/agent_first_guide.md).

### What if I don't use AI agents?

aDNA works perfectly as a human-only knowledge management system. The triad structure, templates, and Obsidian plugins provide value without any AI. Skip `CLAUDE.md` and `AGENTS.md` files — they're inert governance files that don't affect human workflows. See [Using Without AI Agents](#using-without-ai-agents) for the manual setup path.

### Which plugins are essential vs. optional?

Plugins fall into three tiers (see `.obsidian/OBSIDIAN_CLAUDE.md` for full details):

- **Essential** (vault integrity): Templater (auto-applies templates, replaces core templates plugin), Dataview (frontmatter queries), Notebook Navigator (default file browser, replaces core file explorer)
- **Recommended** (major UX): Meta Bind, Style Settings, Icon Folder (triad colors in tabs/links/notes), Homepage, Advanced Canvas, BRAT
- **Optional** (nice-to-have): Tasks, Table Editor, Termy (terminal + Claude Code launcher), Pretty Properties, Fold Properties

The vault functions without optional plugins. Essential plugins are needed for the template auto-trigger and query systems. Two core plugins are disabled by default (file-explorer and templates) because their community replacements are strictly superior — re-enable them in Settings → Core plugins if you prefer the originals.

### How do I sync the vault across machines?

Use **git**. The vault is a standard git repository — commit, push, pull. For Obsidian-native sync, install the [Obsidian Git](https://github.com/denolehov/obsidian-git) community plugin, which auto-commits on a timer and auto-pulls on vault open. Per-device files (`workspace.json`, `graph.json`) are excluded via `.gitignore` so they don't conflict.

### Can I add my own entity types?

Yes — that's the extension model. Add a subdirectory under the appropriate triad leg, create an `AGENTS.md`, and optionally add a template with a Templater folder mapping. See [Extending the Ontology](#extending-the-ontology) for the 3-step process. Example extensions: `who/customers/`, `what/datasets/`, `how/runbooks/`.

### Can I run multiple vaults or connect them?

aDNA supports multi-vault composition through **bridge patterns** — nesting (child vault inside parent), sibling (peer vaults with cross-references), and monorepo (shared root). See [`what/docs/adna_bridge_patterns.md`](what/docs/adna_bridge_patterns.md) for the full spec. Federation across separate instances (different teams, different organizations) is an active development area.

### How do I customize CLAUDE.md for my project?

Edit three sections in `CLAUDE.md`: (1) **Identity & Mission** — replace the project name, agent persona, and mission description; (2) **Domain Knowledge** — add your domain-specific terminology, conventions, and architecture; (3) **Agent Protocol** — adjust the startup sequence and priority rules for your workflow. The rest (safety rules, sync protocol, standing orders) is framework-level and rarely needs changes.

### What's the difference between a skill and a lattice?

**Skills** (`how/skills/skill_<name>.md`) are documented agent recipes — step-by-step procedures in Markdown. **Lattices** (`what/lattices/<name>.lattice.yaml`) are executable directed graphs in YAML. A lattice with `lattice_type: skill` is the composable, publishable form of a skill. **Rule of thumb**: start with a skill file; promote to a lattice when you need registry publishing, runtime execution, or composition with other lattices. See [`what/docs/standard_reading_guide.md` §4](what/docs/standard_reading_guide.md#4-skill-vs-lattice-when-to-use-which) for the full comparison.

### How do templates work?

Templates live in `how/templates/` and auto-apply via the Templater plugin when you create files in mapped directories. For example, creating a file in `what/decisions/` auto-populates the ADR template. 10 of the 22 templates have auto-triggers; the other 12 are applied manually via `Templater: Insert template`. See `how/templates/AGENTS.md` for the full trigger table.

---

## Extending the Ontology

Adding a new entity type takes three steps:

### 1. Create the directory

Place it under the right triad leg:

```bash
mkdir -p who/customers    # People/orgs → who/
# or
mkdir -p what/datasets    # Knowledge objects → what/
# or
mkdir -p how/runbooks     # Operational processes → how/
```

### 2. Add an AGENTS.md

Every directory needs an `AGENTS.md` telling agents what lives here:

```markdown
# customers/ — Agent Guide

## What's Here
Customer records for active and prospective accounts.

## Working Rules
- One file per customer: `customer_<name>.md`
- Check `updated` field before modifying
- Set `last_edited_by` and `updated` on every edit
- Link to contacts via `[[contacts/contact_name]]`
```

### 3. Create a template

Add a template in `how/templates/` so new entities are consistent:

```markdown
---
type: customer
created: 2026-02-28
updated: 2026-02-28
status: prospect
last_edited_by:
tags: [customer]
---

# customer_<name>
```

Configure Templater to auto-trigger the template when files are created in the new directory.

**Using an AI agent?** The entity scaffolding skill (`how/skills/skill_new_entity_type.md`) automates all three steps — just tell the agent what entity type you need and where it belongs.

---

## Context Lattices

> **Lattices are optional.** The triad structure handles knowledge management without them. Lattices add value when you need to model executable workflows, computational pipelines, or multi-step reasoning processes. If your use case is purely knowledge organization, you can skip this section entirely.

A **lattice** is a directed graph connecting datasets, modules, reasoning nodes, and processes into an executable composition. Lattices bridge human knowledge graphs and machine-executable workflows.

### Four Lattice Types

| Type | What it does | Example |
|------|-------------|---------|
| **pipeline** | Deterministic DAG — modules process data through defined stages | Sales pipeline: lead → qualify → propose → close |
| **agent** | LLM-driven reasoning — nodes contain prompts, models make decisions | Code review agent: diff → analyze → critique → suggest |
| **context_graph** | Knowledge structure — connects datasets and context into navigable maps | Domain knowledge graph linking papers, models, and datasets |
| **workflow** | Operational process — defines human/agent procedures | Product launch: research → build → test → ship |

### Three Execution Modes

| Mode | Behavior |
|------|----------|
| **workflow** | Deterministic — every node executes in topological order |
| **reasoning** | LLM-driven — nodes contain prompts, model decides routing |
| **hybrid** | Mixed — some nodes are deterministic, others use LLM reasoning |

### FAIR Metadata — Start Simple, Add Later

Every lattice carries [FAIR](https://www.go-fair.org/fair-principles/) metadata — making it findable, accessible, interoperable, and reusable. You don't need all of it on day one:

| Tier | When | Fields |
|------|------|--------|
| **Start here** | Day 1 | `license`, `keywords` |
| **When sharing** | Publishing or collaborating | + `creators`, `description` |
| **Advanced** | Federation, registries | + `provenance`, `doi`, `access_conditions` |

A minimal lattice just needs two fields:

```yaml
fair:
  license: "MIT"
  keywords: [your, domain, tags]
```

<details>
<summary>Full FAIR example (all fields)</summary>

```yaml
fair:
  license: "MIT"
  creators: ["Your Name", "Your Team"]
  keywords: [research, context engineering, multi-agent]
  description: "What this lattice does and why"
  provenance: "Designed for deep research workflows"
  doi: "10.5281/zenodo.XXXXXXX"
  access_conditions: "Open access"
```

</details>

---

## Your First Lattice

### 1. Pick an example

Example lattices ship in `what/lattices/examples/` across multiple domains:

| Example | Type | What it models |
|---------|------|---------------|
| **General** | | |
| `hello_world.lattice.yaml` | pipeline (workflow) | Minimal 3-node pipeline — start here |
| **Business** | | |
| `sales_pipeline.lattice.yaml` | pipeline (workflow) | Lead → qualify → propose → negotiate → close |
| `product_launch.lattice.yaml` | pipeline (hybrid) | Market research → engineering → QA → launch |
| `brand_doctor.lattice.yaml` | pipeline (hybrid) | Brand audit → competitive analysis → positioning → content strategy |
| **Research & Creative** | | |
| `learning_path.lattice.yaml` | workflow | Course selection → study → practice → assessment |
| `creative_brief.lattice.yaml` | pipeline (hybrid) | Brief intake → design → revision → delivery |
| `deep_research.lattice.yaml` | pipeline (hybrid) | Research query → validated context object |
| `knowledge_base.lattice.yaml` | context_graph (reasoning) | Knowledge retrieval + LLM reasoning |
| `research_orchestrator.lattice.yaml` | agent (hybrid) | Multi-source research coordination |
| **Biotech** | | |
| `protein_binder_design.lattice.yaml` | pipeline (workflow) | Full binder design: target → generation → docking → ranking |
| `binder_generation.lattice.yaml` | pipeline (workflow) | Sub-lattice: generative binder design from target structure |
| `docking_assessment.lattice.yaml` | pipeline (workflow) | Sub-lattice: structure prediction + binding interface scoring |
| `composed_therapeutics.lattice.yaml` | pipeline (workflow) | Therapeutics discovery with federated `lattice://` composition |
| `full_therapeutics.lattice.yaml` | pipeline (workflow) | End-to-end therapeutics composing two federated sub-lattices |

Copy one to start customizing:

```bash
cp what/lattices/examples/hello_world.lattice.yaml what/lattices/my_first.lattice.yaml
```

### 2. Understand the anatomy

A `.lattice.yaml` has five sections:

```yaml
lattice:
  name: my_first                    # URL-safe identifier
  version: "1.0.0"                  # Semver
  lattice_type: pipeline            # pipeline | agent | context_graph | workflow
  description: "What this lattice does"
  execution:
    mode: hybrid                    # workflow | reasoning | hybrid
    runtime: local                  # local | ray | kubernetes
    tier: L1                        # L1 (edge) | L2 (regional) | L3 (cloud)
  nodes:
    - id: input_data
      type: dataset                 # dataset | module | process | reasoning
      description: "Input description"
    - id: analyze
      type: reasoning
      description: "What this node decides"
      prompt: "Instructions for the LLM"
      model_override: "claude-opus-4-6"  # or any LLM model ID
  edges:
    - from: input_data
      to: analyze
      label: "raw data"
      condition: "optional routing condition"
  fair:
    license: "MIT"
    keywords: [your, domain, tags]
```

**Nodes** are the units of work — datasets hold data, modules execute code, processes coordinate, reasoning nodes use LLMs. **Edges** define the flow between them, with optional conditions for branching and loops.

### 3. Validate

```bash
# From the repo root
cd what/lattices
pip install -r tools/requirements.txt
python -c "
from tools.lattice_validate import validate_lattice_file
result = validate_lattice_file('my_first.lattice.yaml')
print(f'Valid: {result.valid}')
for e in result.errors: print(f'  ERROR: {e}')
for w in result.warnings: print(f'  WARN:  {w}')
"
```

### 4. Visualize

Convert to an Obsidian canvas for visual editing:

```bash
python -c "
from tools.lattice2canvas import lattice_file_to_canvas
lattice_file_to_canvas('my_first.lattice.yaml', 'my_first.canvas')
print('Canvas created — open in Obsidian')
"
```

Edit the canvas visually in Obsidian (drag nodes, reroute edges), then convert back:

```bash
python -c "
from tools.canvas2lattice import canvas_file_to_lattice
canvas_file_to_lattice('my_first.canvas', 'my_first.lattice.yaml')
print('Lattice updated from canvas')
"
```

> **Note**: YAML is the source of truth. Canvas is a derived visualization. Round-tripping preserves node IDs, refs, and edge topology, but canvas-only properties (positions, dimensions, groups) don't survive the return trip. See [`canvas_yaml_interop.md`](what/lattices/canvas_yaml_interop.md) for the full mapping spec.

---

## Context Engineering

Token efficiency is the constraint that shapes everything. Every token in an agent's context window must earn its place.

| Principle | What it means |
|-----------|--------------|
| **Smallest high-signal token set** | Deliver maximum useful signal in the fewest tokens. Ruthlessly cut filler. |
| **Sub-agents as compression** | A sub-agent explores 10K+ tokens of source material and returns 1-2K of structured findings. 5-10x compression. |
| **Progressive disclosure** | Structure output in tiers: Tier 1 is self-contained and always loaded. Tier 2 adds depth on demand. Tier 3 provides source verification. |
| **Model-attention-aware formatting** | Tables compress information 40-60% vs. prose and are easier for models to parse. Use structured formats. |
| **Just-in-time retrieval** | Load only the context needed for the current operation. Don't front-load the entire knowledge base. |

The `what/context/` directory implements these principles as a **context library** — structured knowledge files with token estimates, tiered information, and progressive loading. Agents load only the subtopics they need for the current task.

---

## Architecture Reference

### Governance Files

| File | Loaded by | Scope | Update frequency |
|------|-----------|-------|-----------------|
| `CLAUDE.md` | Agents (auto) | Global — project structure, safety, protocol | Rarely (version-gated) |
| `MANIFEST.md` | Both | Global — project identity, architecture | On structural changes |
| `STATE.md` | Both | Global — current plans, blockers, next steps | Every session |
| `AGENTS.md` | Agents | Per-directory — what lives here, how to work with it | When directory contents change |
| `README.md` | Humans | Global — external onboarding, GitHub rendering | On major updates |

### Content-as-Code Pipelines

Files flow through stage directories. A file's location *is* its processing state:

```
how/pipelines/prd_rfc/
├── 01_research/        # Problem exploration
├── 02_requirements/    # PRD authoring (human gate)
├── 03_design/          # RFC authoring
└── 04_review/          # Final approval (human gate)
```

Each stage has an `AGENTS.md` with instructions. Drop a file into stage 1, and agents (or humans) advance it through the pipeline by moving it to the next stage directory.

### Compute Tiers

Lattices specify which compute tier they target:

| Tier | Scope | Example |
|------|-------|---------|
| **L1** (Edge) | Local/edge compute, lightweight inference | Laptop GPU, edge device |
| **L2** (Regional) | Institutional clusters, moderate training | University HPC, on-prem cluster |
| **L3** (Cloud/HPC) | Large-scale data centers, heavy training | Cloud GPU fleet |

### Collision Prevention

Three rules keep multi-agent work safe:

1. **Read before write** — always read current content immediately before writing
2. **Check `updated`** — if another agent edited today, confirm before overwriting
3. **Set `last_edited_by`** — every edit updates the frontmatter audit trail

---

## Contributing

We welcome contributions — bug reports, template improvements, documentation fixes, and design pattern proposals. aDNA is a knowledge architecture, so contributions are primarily Markdown, YAML, and shell scripts rather than application code.

AI agents working in aDNA vaults can also contribute: the [Agent Contribution Mode](CONTRIBUTING.md#agent-contribution-mode) describes how agents surface framework-level improvements organically during normal work.

**Side-quests**: Want to contribute without deep project knowledge? Browse [`how/quests/`](how/quests/) for structured validation experiments you can run with spare agent tokens. Each quest takes 10-30 minutes and produces data that helps improve aDNA. See the [Side-Quest Guide](what/docs/side_quest_guide.md) for details.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full guide.

---

## Ecosystem & Vision

aDNA is more than a file convention — it's a knowledge architecture standard designed to improve through community usage. Agents working in aDNA vaults organically surface framework-level improvements, side-quests collect structured validation data, and version migrations deliver improvements to every vault.

Read [`VISION.md`](who/governance/VISION.md) for the full picture: the decentralized frontier lab model, the opt-in participation ladder (use standalone → contribute improvements → run side-quests → shape the standard), and how the infrastructure built into this repo makes it work.

---

## Further Reading

| Document | What it covers |
|----------|---------------|
| [`what/docs/adna_standard.md`](what/docs/adna_standard.md) | Full normative specification (v2.2) — RFC 2119 keywords, all MUST/SHOULD/MAY rules |
| [`what/docs/standard_reading_guide.md`](what/docs/standard_reading_guide.md) | Reading guide — three persona-based paths through the standard, section map, skill/lattice disambiguation |
| [`what/docs/adna_design.md`](what/docs/adna_design.md) | Architecture rationale — why three legs, why these governance files, design tradeoffs |
| [`what/docs/adna_bridge_patterns.md`](what/docs/adna_bridge_patterns.md) | Multi-instance composition — nesting, sibling, monorepo patterns |
| [`what/docs/migration_guide.md`](what/docs/migration_guide.md) | Adding aDNA to an existing project — decision tree, walkthroughs, starter templates |
| [`what/docs/agent_first_guide.md`](what/docs/agent_first_guide.md) | Terminal-first aDNA setup — using aDNA with Claude Code without Obsidian |
| [`what/docs/projects_folder_pattern.md`](what/docs/projects_folder_pattern.md) | Multi-project workspace pattern — agent-guided scaffolding, shared templates, domain presets |
| [`what/docs/start_kit_prd.md`](what/docs/start_kit_prd.md) | Lattice Start Kit PRD — 1-click onboarding design (CLI interview, scaffolding, 4 personas) |
| [`what/docs/version_migration_guide.md`](what/docs/version_migration_guide.md) | Version migration system — upgrading vaults between CLAUDE.md versions with structured prompts |
| [`VISION.md`](who/governance/VISION.md) | Ecosystem vision — decentralized frontier lab model, participation ladder, community infrastructure |
| [`what/lattices/canvas_yaml_interop.md`](what/lattices/canvas_yaml_interop.md) | Canvas ↔ YAML bidirectional mapping specification |
| [`what/lattices/lattice_yaml_schema.json`](what/lattices/lattice_yaml_schema.json) | JSON Schema for `.lattice.yaml` validation |

---

## Versioning & Changelog

aDNA tracks two independent version numbers: **governance** (CLAUDE.md, vault structure and agent protocol) and **standard** (adna_standard.md, the normative specification). Both use Major.Minor versioning.

See [`CHANGELOG.md`](CHANGELOG.md) for the full version history, version policy, and links to migration prompts for upgrading between versions.

---

## License

[MIT](../LICENSE)
