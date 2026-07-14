<p align="center">
  <img src=".adna/what/assets/aDNABanner.png" alt="aDNA — retro pixel-art wordmark on a metal plate, set against glowing DNA helices rising from a workspace of laboratory instruments" width="100%">
</p>

# aDNA — Agentic DNA

[![Governance v8.7](https://img.shields.io/badge/governance-v8.7-663399.svg)](https://github.com/aDNA-Network/aDNA/releases/tag/v8.7) [![Standard v2.5](https://img.shields.io/badge/standard-v2.5-blue.svg)](https://github.com/aDNA-Network/aDNA/blob/main/.adna/what/docs/adna_standard.md) [![Docs](https://img.shields.io/badge/docs-adna.network-44cc11.svg)](https://adna.network)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Obsidian](https://img.shields.io/badge/Obsidian-Compatible-7C3AED)](https://obsidian.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Ready-F97316)](https://docs.anthropic.com/en/docs/claude-code)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python&logoColor=white)](https://python.org)

**An open-source workspace where AI agents and humans share the same map.**

Most knowledge systems weren't designed with AI agents in mind. aDNA is.

- **One structure, two audiences.** Three directories (`who/`, `what/`, `how/`) organize any project so both AI agents and humans can navigate it.
- **Context narrows automatically.** As your knowledge grows, agents load only what the current task needs — not everything you've ever written.
- **Plain Markdown, no lock-in.** Folders, Markdown files, and a handful of conventions. Works with any editor, any AI agent, any version control.
- **Clone and run.** This repo *is* a ready workspace — clone it to `~/aDNA/`, run your agent in it, and it builds your first project with you.

*A lattice is a graph of graphs — every project you create becomes a node in a growing graph of structured knowledge. This repo is the seed.*

**New to aDNA?** Start with the guided learning path at [adna.network/learn](https://adna.network/learn) — concepts, tutorials, and a first-hour walkthrough.

---

## Getting Started

**Prerequisites:** [Git](https://git-scm.com) and [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed.

```bash
git clone https://github.com/aDNA-Network/aDNA.git ~/aDNA && cd ~/aDNA && claude
```

That's it. The agent reads the workspace router (`CLAUDE.md`), welcomes you, and walks you through creating your first project — tell it about your domain and it builds the right structure for you.

> Faster clone: add `--depth 1` for the latest release without full history.
>
> **Any path works** — `~/aDNA/` is the recommended root, but the workspace is detected, never hardcoded.

### What you just cloned

```
~/aDNA/                  ← your workspace (this repo)
├── CLAUDE.md            ← the workspace router — your agent's map
├── .adna/               ← the aDNA standard: skills, templates, docs, context library
└── <YourProject>.aDNA/  ← your projects appear here (untracked — each its own repo)
```

The tracked base (`CLAUDE.md`, `.adna/`) updates with `git pull` run at the workspace root. Your projects are **never touched by updates** — they're untracked here and live as their own self-contained git repos.

### Working with Obsidian (optional)

For visual browsing and graph view, open `~/aDNA/.adna/` as an Obsidian vault and run `.adna/setup.sh` to install the curated plugin set.

---

## What Is aDNA?

**aDNA (Agentic DNA)** defines the structure inside each project. It organizes knowledge into three directories:

```
who/     →  Who is involved?                 (people, teams, organizations)
what/    →  What does this project know?     (knowledge, decisions, artifacts)
how/     →  How does this project work?      (processes, plans, operations)
```

Small config files (`AGENTS.md`) in each directory give AI agents instant orientation. Humans browse the same structure in [Obsidian](https://obsidian.md)'s graph view.

Full documentation: **[adna.network](https://adna.network)** · the canonical spec lives at [`.adna/what/docs/adna_standard.md`](.adna/what/docs/adna_standard.md).

---

## Existing installs (pre-2026-06 layout)

If you installed aDNA before June 2026, your workspace uses the two-step layout (a standalone `.adna/` clone + a copied router). **Nothing breaks** — your `.adna/` keeps resolving through GitHub's redirect to the archived [`adna-legacy`](https://github.com/aDNA-Network/adna-legacy) repo, frozen at its final commit. To move to this layout at your own pace, run `.adna/how/skills/skill_workspace_upgrade.md` from an agent session — or clone this repo fresh and copy your `*.aDNA/` projects in.

---

## Development & Releases

The standard is developed in the private `aDNA.aDNA` vault and **released to this repo at gate cadence** — every release is a reviewed, tagged snapshot. Issues and PRs are welcome here; framework-level proposals flow into the development graph via the upstream-contribution skill (`.adna/how/skills/skill_upstream_contribution.md`).

## License

[MIT](LICENSE) — take the structure, grow your own lattice.
