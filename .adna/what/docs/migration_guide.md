---
type: context
title: "aDNA Migration Guide — Adding aDNA to an Existing Project"
created: 2026-03-18
updated: 2026-03-18
status: approved
last_edited_by: agent_init
tags: [adna, migration, adoption, guide, getting-started]
---

# aDNA Migration Guide

<!-- Adding aDNA to an existing project — step-by-step -->

## 1. Introduction

This guide is for developers who already have a project and want to add aDNA to it. If you're starting fresh, use the [Quick Start](../../README.md#quick-start) instead — clone the repo, open in Obsidian, done.

**What you'll have at the end**: Your existing project with a working aDNA knowledge architecture — governance files that orient AI agents on first contact, a triad structure for organizing project knowledge, and session tracking for continuous context across agent conversations.

**Time estimate**: 10-15 minutes for the core structure. Under 5 minutes if you copy-paste the starter templates without customization.

**Prerequisites**: A text editor. Optionally, [Obsidian](https://obsidian.md) for visual browsing. No special tooling required.

---

## 2. Which Form Is Right for You?

aDNA deploys in two forms. Pick the one that matches your project:

| Factor | Bare triad | Embedded triad |
|--------|-----------|----------------|
| **Structure** | `who/` `what/` `how/` at project root | `.agentic/who/` `.agentic/what/` `.agentic/how/` |
| **Best for** | Knowledge bases, documentation projects, Obsidian vaults, repos where aDNA IS the project | Code repos, existing apps, repos where aDNA lives ALONGSIDE source code |
| **Root clutter** | Adds 3 directories + 3 files to root | Adds 1 directory + 1 file to root |
| **Agent discovery** | Direct — agents see triad immediately | Indirect — agents read CLAUDE.md, which points to `.agentic/` |
| **Collision risk** | Higher — `who/`, `what/`, `how/` may conflict with existing dirs | Minimal — `.agentic/` is unlikely to exist |
| **.gitignore** | No changes needed | Add `.agentic/` exception if dotfiles are ignored |

**Decision rule**: If you're adding aDNA to a codebase with `src/`, `lib/`, `tests/`, etc. — use **embedded**. If aDNA *is* the project (a knowledge base, documentation vault, or wiki) — use **bare**.

> **Not sure?** Start with embedded. You can always promote to bare later by moving `.agentic/who|what|how/` to the root.

---

## 3. Minimum Viable aDNA

The smallest aDNA installation that delivers Day 1 value:

### Essential files (5)

| File | Location | Purpose |
|------|----------|---------|
| `CLAUDE.md` | Project root (always) | Agent master context — project identity, structure, safety rules |
| `MANIFEST.md` | Project root | Project identity card — what this is, architecture, entry points |
| `STATE.md` | Project root | Operational state — current phase, next steps, blockers |
| `AGENTS.md` | One per triad directory (3 total) | Per-directory guide — what's here, how to work with it |

### Triad directories (3)

| Directory | Bare form | Embedded form |
|-----------|-----------|---------------|
| People & orgs | `who/` | `.agentic/who/` |
| Knowledge & artifacts | `what/` | `.agentic/what/` |
| Operations & process | `how/` | `.agentic/how/` |

That's it — **5 files + 3 directories**. Everything else (templates, sessions, campaigns, lattices, context library, Obsidian config) is enhancement you add when you need it.

### What you can add later

| Enhancement | When to add | What it gives you |
|-------------|-------------|-------------------|
| `how/sessions/` | When you want cross-session continuity | Agents pick up where the last one left off |
| `how/templates/` | When you create the same file type repeatedly | Consistent frontmatter, less boilerplate |
| `how/campaigns/` + `how/missions/` | When work spans multiple sessions | Structured decomposition of complex initiatives |
| `what/context/` | When agents need domain knowledge | Pre-loaded expertise files for specific topics |
| `what/decisions/` | When you want to track ADRs | Architecture Decision Records with linked rationale |
| `.obsidian/` | When you want visual browsing | Graph view, wikilinks, canvas, themes |

---

## 4. Walkthrough: Embedded Form

For code repos where aDNA lives alongside source code. Each step includes a timing checkpoint — total should be under 15 minutes.

### Step 1: Create the structure (~30 seconds)

```bash
# From your project root
mkdir -p .agentic/who .agentic/what .agentic/how
```

Your project now looks like:

```
my-project/
├── src/                    # Your existing code
├── tests/                  # Your existing tests
├── .agentic/               # aDNA knowledge architecture
│   ├── who/                # People & organizations
│   ├── what/               # Knowledge & artifacts
│   └── how/                # Operations & process
├── CLAUDE.md               # (next step)
└── ...                     # Your existing files
```

**Checkpoint**: ~30 seconds elapsed.

### Step 2: Write CLAUDE.md (~3 minutes)

Create `CLAUDE.md` **at your project root** (not inside `.agentic/`). This is the file AI agents auto-load on startup.

```markdown
# CLAUDE.md — [Your Project Name]

## Identity

This is [one-sentence description of your project].

## Structure

Project knowledge lives in `.agentic/` using the aDNA triad:

- `.agentic/who/` — people, teams, contacts, stakeholders
- `.agentic/what/` — research, decisions, domain knowledge, artifacts
- `.agentic/how/` — plans, processes, sessions, workflows

Source code lives in the standard project structure ([describe briefly: src/, lib/, etc.]).

## Agent Protocol

1. Read this file (auto-loaded)
2. Read `STATE.md` for current operational context
3. Read the `AGENTS.md` in the directory you're working in

## Safety Rules

- Read before write — always check current content before modifying
- Set `last_edited_by` and `updated` in frontmatter when editing `.agentic/` files
- Do not modify files outside `.agentic/` without explicit instruction

## Domain

[Add 3-5 bullet points about your domain — what this project does,
key terminology, important conventions. This is where agents learn
what makes YOUR project different.]
```

**Customize**: Replace the bracketed sections. The `## Domain` section is where you teach agents about your project — spend a minute here writing a few bullet points. Everything else is structural.

**Checkpoint**: ~3.5 minutes elapsed.

### Step 3: Write MANIFEST.md and STATE.md (~2 minutes)

**MANIFEST.md** — project identity card:

```markdown
---
type: manifest
created: 2026-03-18
updated: 2026-03-18
---

# [Your Project Name]

## What This Is

[2-3 sentences: what the project does, who it's for, why it exists.]

## Architecture

[Brief description of the codebase structure — languages, frameworks, key directories.]

## Active Builds

- [Current focus area or sprint goal]
```

**STATE.md** — operational state:

```markdown
---
type: state
created: 2026-03-18
updated: 2026-03-18
---

# Operational State

## Current Phase

[What's happening right now — the active sprint, milestone, or focus area.]

## Next Steps

- [Immediate next action]
- [Following action]

## Blockers

- [None, or list current blockers]
```

**Checkpoint**: ~5.5 minutes elapsed.

### Step 4: Write AGENTS.md for each triad directory (~3 minutes)

Each triad directory gets an `AGENTS.md` telling agents what belongs here. These are short — 5-10 lines each.

**.agentic/who/AGENTS.md**:

```markdown
# who/ — Agent Guide

## What's Here

People, teams, and organizations related to [your project].

## Working Rules

- One file per person or organization
- Use frontmatter: `type`, `created`, `updated`, `tags`
- Link to related entries with `[[wikilinks]]`
```

**.agentic/what/AGENTS.md**:

```markdown
# what/ — Agent Guide

## What's Here

Knowledge, research, decisions, and artifacts for [your project].

## Working Rules

- Decisions go in `what/decisions/` as ADRs
- Domain knowledge goes in `what/context/`
- Use frontmatter: `type`, `created`, `updated`, `tags`
```

**.agentic/how/AGENTS.md**:

```markdown
# how/ — Agent Guide

## What's Here

Operational processes, plans, and session tracking for [your project].

## Working Rules

- Session files go in `how/sessions/`
- Multi-session plans go in `how/missions/`
- Use frontmatter: `type`, `created`, `updated`, `status`, `tags`
```

**Checkpoint**: ~8.5 minutes elapsed.

### Step 5: Classify existing knowledge (~3-5 minutes)

Look at your existing project files. Do any of them contain knowledge that belongs in the triad? Use the **Question Test**:

| If the content answers... | It belongs in... |
|---------------------------|------------------|
| "Who is involved?" — team members, stakeholders, contacts | `.agentic/who/` |
| "What do we know?" — research, decisions, specs, designs | `.agentic/what/` |
| "How do we work?" — processes, runbooks, checklists, plans | `.agentic/how/` |

Common candidates:

- **CONTRIBUTING.md** → copy key points into `.agentic/how/` (keep the original for GitHub)
- **Architecture docs** → move or link into `.agentic/what/decisions/`
- **Team/contacts info** → move to `.agentic/who/`
- **Runbooks/playbooks** → move to `.agentic/how/`

> **Don't over-migrate.** Move 2-3 files on Day 1. The triad grows organically — you'll naturally file new knowledge into the right directory as you create it.

**Checkpoint**: ~12 minutes elapsed.

### Step 6: Test (~1 minute)

Open a terminal in your project directory and start your AI agent:

```bash
claude    # or your preferred agent
```

The agent should:
1. Read `CLAUDE.md` automatically
2. Understand your project structure
3. Know where to find and file knowledge
4. Follow the safety rules you defined

Try asking: *"What is this project and how is the knowledge organized?"*

If the agent can answer correctly, your aDNA installation is working.

**Checkpoint**: ~13 minutes. Done.

---

## 5. Walkthrough: Bare Form

For knowledge bases, documentation projects, and repos where aDNA IS the project. The steps are identical to the embedded form with these differences:

### Structure differences

```bash
# Instead of .agentic/ subdirectories:
mkdir -p who what how
```

```
my-knowledge-base/
├── who/                    # People & organizations
├── what/                   # Knowledge & artifacts
├── how/                    # Operations & process
├── CLAUDE.md               # Agent master context
├── MANIFEST.md             # Project identity
├── STATE.md                # Operational state
└── ...                     # Any existing files
```

### CLAUDE.md differences

Update the `## Structure` section to reference root-level directories:

```markdown
## Structure

Project knowledge uses the aDNA triad at the project root:

- `who/` — people, teams, contacts, stakeholders
- `what/` — research, decisions, domain knowledge, artifacts
- `how/` — plans, processes, sessions, workflows
```

### Extra considerations

- **Existing directories**: If you already have a `how/` or `what/` directory, you have two options: (a) adopt the aDNA naming and add `AGENTS.md` files to your existing directories, or (b) switch to the embedded form to avoid collisions.
- **Root file count**: The bare form adds `CLAUDE.md`, `MANIFEST.md`, `STATE.md`, and `README.md` to your root. If your root is already crowded, embedded form keeps it cleaner.
- **Mixed content**: In bare form, the triad directories contain only aDNA-managed knowledge. Keep source code, build artifacts, and tooling configs at the root or in their own directories — don't put code inside `what/` or `how/`.

---

## 6. Starter Templates

Copy-paste-ready minimal versions. Customize the bracketed sections.

### CLAUDE.md (~25 lines)

```markdown
# CLAUDE.md — [Your Project Name]

## Identity

This is [one-sentence project description].

## Structure

[Bare: `who/`, `what/`, `how/` at root]
[Embedded: `.agentic/who/`, `.agentic/what/`, `.agentic/how/`]

## Agent Protocol

1. Read this file (auto-loaded)
2. Read `STATE.md` for current context
3. Read the `AGENTS.md` in the directory you're working in

## Safety Rules

- Read before write
- Set `last_edited_by` and `updated` on every edit
- Do not modify files outside the triad without explicit instruction

## Domain

- [Key fact about your project]
- [Important convention or pattern]
- [Domain terminology to know]
```

### MANIFEST.md (~15 lines)

```markdown
---
type: manifest
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# [Your Project Name]

## What This Is

[2-3 sentences describing the project.]

## Architecture

[Languages, frameworks, key directories.]

## Active Builds

- [Current focus]
```

### STATE.md (~10 lines)

```markdown
---
type: state
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Operational State

## Current Phase

[What's happening now.]

## Next Steps

- [Next action]
```

### AGENTS.md (~8 lines)

```markdown
# [directory_name]/ — Agent Guide

## What's Here

[One sentence: what this directory contains.]

## Working Rules

- [Naming convention for files]
- Use frontmatter: `type`, `created`, `updated`, `tags`
```

---

## 7. Common Pitfalls

Things that trip people up when adding aDNA to an existing project:

### Putting CLAUDE.md inside `.agentic/` instead of the project root

AI agents auto-load `CLAUDE.md` from the project root. If it's inside `.agentic/`, agents won't find it on startup and lose all orientation. **Always place CLAUDE.md at the project root**, regardless of which triad form you use.

### Over-engineering Day 1

You don't need 14 entity types, custom templates, campaign hierarchies, and a context library on your first day. Start with the minimum viable set (5 files + 3 directories). Add structure as you discover you need it — the triad grows organically.

### Frontmatter perfectionism

Start with three fields: `type`, `created`, `tags`. Add `updated`, `status`, `last_edited_by` when you have multiple agents or collaborators. Add domain-specific fields when you find yourself repeatedly including the same information. Don't design the perfect schema upfront.

### Forgetting AGENTS.md files

Every triad directory needs an `AGENTS.md`. Without it, agents have no routing information for that directory and will either skip it or read everything in it (wasting tokens). Even a 3-line AGENTS.md is better than none.

### Migrating everything at once

Don't dump all your existing docs into the triad in one session. Move 2-3 files to prove the pattern works. Let the structure grow as new knowledge is created. Forced migrations create filing confusion and don't stick.

### Treating aDNA as a replacement for your existing structure

aDNA doesn't replace your codebase structure (`src/`, `lib/`, `tests/`). In the embedded form, `.agentic/` sits alongside your code — it manages *project knowledge*, not source code. Your code organization stays exactly as it is.

---

## 8. What to Do Next

Once the core structure is working, enhance it progressively:

### Week 1: Session tracking

Add `how/sessions/` (bare) or `.agentic/how/sessions/` (embedded). Each agent session creates a file here before modifying the vault. Sessions create continuity — the next agent reads the last session's handoff notes and picks up where it left off.

### Week 2: Templates

Create templates in `how/templates/` for file types you create repeatedly. A template is just a Markdown file with pre-filled frontmatter that gets copied when you create a new file of that type.

### Week 3: Your first campaign

When you have a multi-session initiative (a feature build, a research project, a migration), create a campaign file in `how/campaigns/`. Campaigns decompose into missions (multi-session tasks) which decompose into objectives (single-session units). This gives agents structured context about what you're working toward.

### When needed: Context library

As your project accumulates domain knowledge that agents need repeatedly, organize it into `what/context/` with topic-based files. Each file covers one domain topic with structured information that agents can load on demand instead of re-discovering it each session.

### When collaborating: Obsidian config

If your team uses Obsidian for visual browsing, add `.obsidian/` with theme and plugin configuration. See the [Agentic-DNA repo](https://github.com/LatticeProtocol/adna) for a pre-configured setup with 15 plugins and the Tokyo Night theme.

### When connecting: Bridge patterns

When your project needs to reference or compose with other aDNA instances, see [`adna_bridge_patterns.md`](adna_bridge_patterns.md) for nesting, sibling, and monorepo composition patterns.

---

## 9. Quick Reference

### The Question Test

| Question | Triad leg |
|----------|-----------|
| Who is involved? | `who/` |
| What does this project know? | `what/` |
| How does this project work? | `how/` |

### File placement checklist

```
Project root:
  ✓ CLAUDE.md          (agent master context — ALWAYS at root)
  ✓ MANIFEST.md        (project identity)
  ✓ STATE.md           (operational state)

Triad directories (bare: root / embedded: .agentic/):
  ✓ who/AGENTS.md      (people directory guide)
  ✓ what/AGENTS.md     (knowledge directory guide)
  ✓ how/AGENTS.md      (operations directory guide)
```

### Minimum frontmatter

```yaml
---
type: [entity_type]
created: YYYY-MM-DD
tags: [relevant, tags]
---
```

---

*Migration guide v1.0 | Companion to the [aDNA Standard](adna_standard.md), [Design Document](adna_design.md), and [Bridge Patterns](adna_bridge_patterns.md)*
