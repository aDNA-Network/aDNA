---
type: context
title: "Agent-First Guide — Using aDNA Without Obsidian"
created: 2026-03-19
updated: 2026-03-19
status: approved
last_edited_by: agent_init
tags: [adna, agent-first, claude-code, terminal, guide]
token_estimate: ~3500
---

# Agent-First Guide

<!-- Using aDNA with Claude Code and a terminal — no Obsidian required -->

## 1. Introduction

This guide is for developers who want to use aDNA with Claude Code (or another AI coding agent) from the terminal, without installing Obsidian. If you already use Obsidian, you don't need this — the [Quick Start](../../README.md#quick-start) covers everything.

**What you'll have at the end**: A working aDNA vault that Claude Code can navigate, with session tracking, templates, and the full execution hierarchy — all from your terminal and text editor.

**Time estimate**: 10-15 minutes.

**Prerequisites**:
- Git
- A text editor (VS Code, Vim, Emacs, whatever you use)
- The `claude` CLI ([Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview))

---

## 2. What Works Without Obsidian

aDNA is a directory convention — Markdown files with YAML frontmatter organized in a `who/`/`what/`/`how/` triad. Obsidian adds a visual layer on top, but the operational core is plain files on disk.

### Feature parity at a glance

| Bucket | Count | % | What's in it |
|--------|-------|---|-------------|
| **Works everywhere** | 22 | 55% | Governance, sessions, templates, context library, execution hierarchy, git workflow, FAIR metadata, lattice YAML, naming conventions, skills, campaigns, missions, onboarding |
| **Degraded** | 6 | 15% | Wikilinks (no click-nav), graph view (unavailable), Dataview queries (won't render), search (editor-dependent), Meta Bind inputs (won't render), Tasks queries (won't render) |
| **Requires Obsidian** | 12 | 30% | Templater auto-trigger, Canvas, Obsidian Git, Notebook Navigator, Homepage, Icon Folder, Style Settings + CSS, BRAT, Termy, Pretty Properties, Fold Properties, Banners |

**The important number**: The operational core — governance (`CLAUDE.md`, `AGENTS.md`), session tracking, templates-as-files, context library, execution hierarchy, git workflow — is **100% functional** without Obsidian. The 30% you lose is visual polish and automation shortcuts. The value split is closer to **80/20**.

### Detailed breakdown

**Works everywhere** — these features are plain Markdown and YAML:

| Feature | How it works without Obsidian |
|---------|-------------------------------|
| `CLAUDE.md` governance | Auto-loaded by Claude Code on startup. No change. |
| `AGENTS.md` per-directory guides | Read by agents before working in a directory. No change. |
| `MANIFEST.md` + `STATE.md` | Plain Markdown. No change. |
| Triad structure (`who/`/`what/`/`how/`) | Directory convention. Works in any filesystem. |
| YAML frontmatter | Standard YAML. Parsed by agents, readable in any editor. |
| 14 base entity types | Naming conventions + frontmatter schemas. No Obsidian dependency. |
| Session tracking | Create files in `how/sessions/active/`, move to `history/` on close. |
| Execution hierarchy | Campaign → Mission → Objective. Plain Markdown with status tracking. |
| Context library | `what/context/` files loaded by agents on demand. |
| Context recipes | Cross-topic assembly instructions. Agent-parsed. |
| Skills | Reusable agent recipes in `how/skills/`. Agent-executed. |
| Templates | Files in `how/templates/`. Copy manually instead of auto-trigger. |
| Git workflow | Standard git. `commit`, `push`, `pull` from terminal. |
| Lattice YAML | `.lattice.yaml` definitions. Schema-validated. |
| FAIR metadata | `fair:` blocks in lattice YAML. No rendering dependency. |
| Naming conventions | Underscores, `type_descriptive_name.md`. Convention, not tooling. |
| Wikilinks as identifiers | `[[filename]]` syntax serves as machine-parseable cross-references even without Obsidian's click-navigation. Agents use them for relationship discovery. |
| First-run detection + onboarding | Claude Code reads `CLAUDE.md`, detects uncustomized vault, runs `skill_onboarding.md` interactively. Fully terminal-compatible. |
| Bridge patterns | Multi-vault composition. Directory conventions, no Obsidian dependency. |
| OODA cascade | Observe-Orient-Decide-Act at each execution level. Methodology, not tooling. |
| Convergence model | Progressive context narrowing. Agent behavior, not Obsidian feature. |
| Escalation / priority rules | Governance protocols. Agent-enforced. |

**Degraded** — present in files but won't render interactively:

| Feature | What happens | Workaround |
|---------|-------------|------------|
| Wikilinks | `[[filename]]` appears as literal text. No click-navigation, no auto-rename on file move. | Use `grep` or `rg` to find references. Agents parse wikilinks natively. |
| Graph view | Not available. No visual map of entity relationships. | Use `grep '[[' *.md` to trace links. Or `rg '\[\[' --type md` for recursive search. |
| Dataview queries | ` ```dataview ``` ` blocks appear as code fences. No rendered tables. | Claude Code can query frontmatter directly — ask it to find files by type, status, etc. |
| Search | No unified Obsidian search. | `rg` (ripgrep) or your editor's search. Claude Code's `Grep` tool works across the vault. |
| Meta Bind inputs | ` ```meta-bind ``` ` blocks appear as code fences. No interactive controls. | Edit frontmatter directly in your editor. |
| Tasks queries | ` ```tasks ``` ` blocks appear as code fences. No rendered task lists. | Track tasks in frontmatter (`status` field) or use Claude Code's task system. |

**Requires Obsidian** — completely absent without it:

| Feature | What you lose | Impact |
|---------|--------------|--------|
| Templater auto-trigger | No automatic template application when creating files in mapped directories. | Low — copy from `how/templates/` manually or let Claude Code do it. |
| Canvas / Advanced Canvas | No visual node graphs, no canvas presentations. | Medium — use Mermaid diagrams in Markdown or skip visual workflows. |
| Obsidian Git | No auto-commit timer, no auto-pull on open. | None — use standard `git` commands. |
| Notebook Navigator | No folder-based navigation with triad colors and icons. | Low — use `ls`, `tree`, or your editor's file explorer. |
| Homepage | No configured start page on vault open. | None — `STATE.md` serves the same purpose for agents. |
| Icon Folder | No custom folder/file icons. | None — cosmetic only. |
| Style Settings + CSS | No theme customization GUI, no visual styling. | None — cosmetic only. |
| BRAT | No beta plugin management. | None — only relevant for Obsidian plugins. |
| Termy | No terminal presets inside Obsidian. | None — you're already in a terminal. |
| Pretty Properties | No polished frontmatter display. | None — read YAML directly. |
| Fold Properties | No auto-folding of frontmatter blocks. | None — editor setting. |
| Banners | No header images on notes. | None — cosmetic only. |

---

## 3. Setup Walkthrough

### Step 1: Clone the repo

```bash
git clone https://github.com/LatticeProtocol/adna.git adna
cd adna
```

Skip `./setup.sh` — that script downloads Obsidian plugins and themes. The `.obsidian/` directory will exist in the repo but is inert without Obsidian installed. You can ignore it.

### Step 2: Launch Claude Code

```bash
claude
```

Claude Code auto-loads `CLAUDE.md` from the project root. **Berthier** — the built-in agent personality — orients on the vault structure and is ready to work.

**If onboarding triggers**: On a truly fresh vault (empty session history, uncustomized `MANIFEST.md`), Berthier automatically runs the interactive onboarding skill — explaining the architecture, asking about your project, and customizing governance files. The entire flow runs in the terminal.

**On the reference repo** (the default): The aDNA repo ships with reference content already in place (sample sessions, populated manifests, documentation). Onboarding won't auto-trigger. Instead, tell Claude Code what you want to do:

- *"Customize this vault for my project"* — Berthier will walk you through editing `MANIFEST.md`, `STATE.md`, and the identity section of `CLAUDE.md`
- *"Run the onboarding skill"* — explicitly invokes `how/skills/skill_onboarding.md` for the full guided experience

### Step 3: Verify the setup

After customization, confirm three things:

1. **`MANIFEST.md`** — should have your project name and description
2. **`STATE.md`** — should reflect your current phase and next steps
3. **`how/sessions/active/`** — should contain a session file

```bash
head -20 MANIFEST.md
head -20 STATE.md
ls how/sessions/active/
```

If all three check out, your vault is operational.

### Alternative: Manual setup (no agent)

If you prefer to skip the agent entirely:

1. Edit `MANIFEST.md` — replace the project description with your own
2. Edit `STATE.md` — set your current phase and next steps
3. Optionally edit `CLAUDE.md` — customize the `## Identity & Personality` section

Use the starter templates in the [Migration Guide](migration_guide.md) § 6 for copy-paste-ready governance files.

---

## 4. Session Workflow

### Creating sessions

In Obsidian, Templater auto-applies `template_session.md` when you create a file in `how/sessions/active/`. Without Obsidian, you have two options:

**Option A: Let Claude Code handle it** (recommended)

Claude Code's agent protocol creates a session file automatically on startup. Just launch `claude` and start working — the session file will be created for you.

**Option B: Copy the template manually**

```bash
cp how/templates/template_session.md \
   how/sessions/active/session_$(whoami)_$(date +%Y%m%d)_descriptor.md
```

Then open the file and replace the Templater placeholders with actual values:

| Placeholder | Replace with |
|-------------|-------------|
| `YYYY-MM-DD` | Today's date (e.g., `2026-03-19`) |
| `{username}` | Your username |
| `{ISO_TIMESTAMP}` | Current timestamp (e.g., `2026-03-19T10:00:00-05:00`) |
| `<% tp.date.now() %>` | Today's date — this is Templater syntax that won't auto-resolve |
| `<% tp.file.title %>` | The filename you just created |

> **Templater syntax note**: Templates contain `<% tp.date.now("YYYY-MM-DD") %>` and similar expressions. These are Templater plugin functions that auto-resolve in Obsidian. In a terminal, they appear as literal text. Replace them with the actual values.

### Closing sessions

When you're done working:

1. Update your session file's SITREP section (completed, in progress, next up, blockers)
2. Write the **Next Session Prompt** — a self-contained paragraph so the next agent can continue
3. Set `status: completed` in frontmatter
4. Move the file to the history directory:

```bash
# Create the month directory if it doesn't exist
mkdir -p how/sessions/history/$(date +%Y-%m)

# Move the session file
mv how/sessions/active/session_*.md \
   how/sessions/history/$(date +%Y-%m)/
```

### Git workflow

Without Obsidian Git's auto-commit, use standard git:

```bash
# Start of session
git pull

# After making changes
git add -A
git commit -m "session: brief description of what changed"
git push
```

If you're the only user, commit frequency is up to you. If multiple people sync the vault, commit and push at the end of each session to avoid conflicts.

---

## 5. Claude Code Configuration

### CLAUDE.md placement

`CLAUDE.md` must be at the **project root** — Claude Code auto-loads it from the working directory. This is the single most important file for agent orientation. If it's missing or misplaced, agents start blind.

### Memory vs. sessions

Claude Code has two persistence mechanisms. They serve different purposes:

| Mechanism | Location | Scope | Use for |
|-----------|----------|-------|---------|
| **Claude Code memory** | `~/.claude/projects/` | Personal, per-machine | Your preferences, feedback, credentials, tool notes |
| **Vault sessions** | `how/sessions/` | Shared, in git | Work continuity across agents and collaborators |

Memory is private — it stays on your machine and isn't committed to git. Sessions are shared — they go into the vault repo so any collaborator (human or agent) can pick up where you left off.

### The `.claude/` directory

Claude Code creates a `.claude/` directory in your project for local settings:

```
.claude/
├── settings.json     # Project-specific permissions and hooks
└── ...               # Other machine-local state
```

This directory is **gitignored** — it's machine-local configuration that shouldn't be shared. Each collaborator has their own `.claude/` directory.

### `.mcp.json`

If you use MCP (Model Context Protocol) servers with Claude Code, the `.mcp.json` config file is also **gitignored**. Claude Code has native filesystem access, so you don't need a filesystem MCP server. Add MCP servers only for external integrations (databases, APIs, specialized tools).

### Useful patterns

| Pattern | When to use |
|---------|-------------|
| **Plan mode** | Before starting a multi-step mission. Claude Code explores the codebase, designs an approach, and gets your approval before writing code. |
| **Explore agents** | For codebase research. Claude Code spawns a sub-agent to search files, trace references, and report back without consuming your main conversation context. |
| **Hooks** | For automation. Configure in `.claude/settings.json` to run scripts on events (e.g., auto-format on file save, run tests after edits). |
| **`/clear` then re-orient** | When context gets stale mid-session. Clear the conversation, Claude Code reloads `CLAUDE.md`, and you get a fresh start with the vault's current state. |

---

## 6. Substitution Table

Quick reference for replacing Obsidian-specific features:

| Obsidian feature | Terminal substitute |
|-----------------|-------------------|
| Templater auto-trigger | Copy from `how/templates/` manually, or let Claude Code create files |
| Graph view | `rg '\[\[' --type md` to trace wikilink relationships |
| Canvas | Mermaid diagrams in Markdown, or skip visual workflows |
| Obsidian Git | Standard `git pull` / `git commit` / `git push` |
| Obsidian search | `rg` (ripgrep) or your editor's search |
| Dataview queries | Ask Claude Code to query frontmatter (e.g., "find all files with status: active") |
| Meta Bind inputs | Edit frontmatter YAML directly |
| Tasks plugin | Track status in frontmatter fields or use Claude Code's task tracking |
| Notebook Navigator | `ls`, `tree`, or editor file explorer |
| Homepage | Read `STATE.md` for operational context on startup |

---

## 7. Growing Into Obsidian

If you later decide to add Obsidian, install it, open the vault directory, enable community plugins when prompted, and run `./setup.sh`. Everything lights up — graph view, wikilink navigation, canvas visualizations, auto-templates, the Tokyo Night theme. It's a one-way door that adds capability without changing anything you've already built. Your governance files, sessions, context library, and git history all carry over unchanged.

---

*Agent-first guide v1.0 | Companion to the [Migration Guide](migration_guide.md), [aDNA Standard](adna_standard.md), and [Architecture Overview](adna_design.md)*
