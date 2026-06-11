> [!NOTE]
> **This directory is the aDNA standard tree, embedded in [`aDNA-Network/aDNA`](https://github.com/aDNA-Network/aDNA) — the clone-and-run workspace image.** It updates with the workspace (`git pull` at the workspace root); do not modify it directly (Standing Rule 1). The standard is developed in the private `aDNA.aDNA` vault and released here at gate cadence via `skill_template_release`.

<p align="center">
  <img src="what/assets/aDNABanner.png" alt="aDNA — retro pixel-art wordmark on a metal plate, set against glowing DNA helices rising from a workspace of laboratory instruments" width="100%">
</p>

# aDNA — Agentic DNA

[![Governance v7.2](https://img.shields.io/badge/governance-v7.2-663399.svg)](https://github.com/aDNA-Network/aDNA/releases/tag/v7.2) [![Standard v2.2](https://img.shields.io/badge/standard-v2.2-blue.svg)](https://github.com/aDNA-Network/aDNA/blob/main/.adna/what/docs/adna_standard.md) [![Docs](https://img.shields.io/badge/docs-adna--docs.vercel.app-44cc11.svg)](https://adna-docs.vercel.app/)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Obsidian](https://img.shields.io/badge/Obsidian-Compatible-7C3AED)](https://obsidian.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Ready-F97316)](https://docs.anthropic.com/en/docs/claude-code)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python&logoColor=white)](https://python.org)

**An open-source project template where AI agents and humans share the same map.**

Most knowledge systems weren't designed with AI agents in mind. aDNA is.

- **One structure, two audiences.** Three directories (`who/`, `what/`, `how/`) organize any project so both AI agents and humans can navigate it.
- **Context narrows automatically.** As your knowledge grows, agents load only what the current task needs — not everything you've ever written.
- **Plain Markdown, no lock-in.** Folders, Markdown files, and a handful of conventions. Works with any editor, any AI agent, any version control.
- **Conversational onboarding.** Clone the repo, run `claude`, and the AI builds a project structure tailored to your domain.

*A lattice is a graph of graphs — every project you create becomes a node in a growing graph of structured knowledge. This repo is the seed.*

---

## Getting Started

**Prerequisites:** [Git](https://git-scm.com) and [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed.

```bash
# Create the workspace + clone the template into .adna/ (hidden by convention)
mkdir -p ~/aDNA && cd ~/aDNA
git clone https://github.com/LatticeProtocol/aDNA.git .adna

# Bootstrap the workspace router from the template
cp .adna/how/templates/template_workspace_claude.md CLAUDE.md

# Start the AI — it handles the rest
claude
```

Claude reads the workspace router (`~/aDNA/CLAUDE.md`) and walks you through creating your first project. Tell it about your domain — it builds the right structure for you.

> For a faster clone, use `git clone --depth 1` — you'll get the latest template without full git history.
>
> **v7.0 flatten note**: post-aDNA-v7.0 (campaign_adna_v2_infrastructure 2026-05-18), the template clones directly into `.adna/` as a flat repo (no nested `adna/.adna/` layer). The workspace router (`~/aDNA/CLAUDE.md`) is bootstrapped from the template via the `cp` step above. See the v6→v7 upgrade guide at [`.adna/how/docs/upgrade_v6_to_v7.md`](how/docs/upgrade_v6_to_v7.md) for existing-operator migration.
>
> **Workspace-root note**: `~/aDNA/` is the recommended workspace root; any path works — `<workspace_root>` is detected, never hardcoded. Operators on the legacy `~/lattice/` root migrate via [`skill_workspace_path_migration`](how/skills/skill_workspace_path_migration.md) (a turnkey agentic transition) plus a `~/lattice → ~/aDNA` symlink shim that keeps every existing reference valid mid-migration.

---

## What Is aDNA?

**aDNA (Agentic DNA)** defines the structure inside each project. It organizes knowledge into three directories:

```
who/     →  Who is involved?                 (people, teams, organizations)
what/    →  What does this project know?     (knowledge, decisions, artifacts)
how/     →  How does this project work?      (processes, plans, operations)
```

Small config files (`AGENTS.md`) in each directory give AI agents instant orientation. Humans browse the same structure in [Obsidian](https://obsidian.md)'s graph view.

---

## How It Works

Your `~/aDNA/` directory looks like this:

```mermaid
graph LR
    A["~/aDNA/"] --> B[".adna/"]
    A --> C["my_project.aDNA/"]
    A --> D["another_project.aDNA/"]
    
    B --> B1["Base template — updates via git pull"]
    C --> C1["who/ what/ how/"]
    D --> D1["who/ what/ how/"]
```

The hidden `.adna/` directory is the base template — it holds the toolkit: templates, skills, context library, workflow tools, and Obsidian config.

When you create a project, Claude forks `.adna/` into a new `project_name.aDNA/` directory with its own git repo.

Run `git pull` in `~/aDNA/` anytime to update the template. Your projects are unaffected.

As you add projects, context narrows to what each task actually needs:

```mermaid
graph TD
    L["Full knowledge graph"] --> C["Active project — ~50K tokens"]
    C --> M["Current task — ~15K tokens"]
    M --> O["Immediate focus — ~5K tokens"]
```

---

## What's Inside .adna/?

| Component | What it is |
|-----------|-----------|
| **Context library** | Curated domain knowledge across multiple topics (~75K tokens) |
| **Templates** | Session, mission, campaign, context, ADR, and more |
| **Agent skills** | Onboarding, project fork, quality audit, lattice publishing |
| **Workflow toolkit** | YAML definitions, Python validators, YAML↔Canvas converters, JSON Schema |
| **Obsidian config** | Theme, plugins, CSS snippets — runs `setup.sh` to install |
| **Full documentation** | Detailed README, aDNA standard, design docs, migration guides |

---

## Who Is This For?

aDNA works for any project that manages knowledge:

- **Researchers** — papers, datasets, experiments, collaborations
- **Founders** — investors, customers, product roadmap, fundraising
- **Creative professionals** — clients, projects, assets, revision cycles
- **Teams** — shared context, coordinated operations, persistent memory
- **Personal knowledge managers** — learning goals, reading notes, skills

Every domain is different — the conversational onboarding adapts the structure to yours.

---

## How aDNA Compares

| | aDNA | Notion | PARA | Johnny Decimal | Zettelkasten |
|---|---|---|---|---|---|
| **AI-native** | Built for agents | — | — | — | — |
| **Human-friendly** | Obsidian graph | Web app | Folders | Numbered folders | Links + backlinks |
| **Portable** | Markdown + Git | Proprietary | Methodology | Methodology | Methodology |
| **Context scales** | Narrows automatically | — | — | — | — |
| **Execution system** | Project → task → objective | Project views | Projects + Areas | Categories | — |

aDNA isn't a replacement for these systems — it's what happens when you need your knowledge architecture to work for AI agents *and* humans simultaneously.

---

## Learn More

The full technical documentation lives inside `.adna/`:

- **[aDNA Standard](what/docs/adna_standard.md)** — formal specification
- **[Contributing](CONTRIBUTING.md)** — how to improve aDNA
- **[Changelog](CHANGELOG.md)** — version history

---

## License

[MIT](LICENSE) — use it for anything.

*Built by [Lattice Protocol](https://github.com/LatticeProtocol). aDNA is domain-neutral — any project benefits.*
