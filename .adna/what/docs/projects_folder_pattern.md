---
type: context
title: "aDNA Projects Folder Pattern"
created: 2026-03-19
updated: 2026-04-03
status: active
last_edited_by: agent_init
tags: [adna, projects, scaffolding, workspace, pattern, lattice]
token_estimate: 2500
---

# aDNA Projects Folder Pattern

A workspace-level pattern for managing multiple aDNA-structured projects. Two approaches: the **Simplified Pattern** (recommended — uses the aDNA repo itself as the template) and the **Advanced Pattern** (uses a `.base/` directory with variable templates).

---

## Simplified Pattern (Recommended)

The repo root **is** `~/aDNA/`. Clone it once, and the root CLAUDE.md handles project creation and discovery. The base template lives in a hidden `.adna/` directory.

```
~/aDNA/                        # git clone target = user's lattice
├── CLAUDE.md                     # "The Front Door" — lattice intro, project creation
├── README.md                     # "What is a lattice?" — GitHub landing page
├── LICENSE
├── .gitignore                    # Ignores *.aDNA/ user projects
├── .adna/                        # Hidden: base template (all aDNA content)
│   ├── CLAUDE.md                 # Template-level governance (forked into projects)
│   ├── MANIFEST.md               # role: template marker (stripped on fork)
│   ├── setup.sh                  # Obsidian plugin bootstrap
│   └── how/skills/
│       ├── skill_project_fork.md    # Forks .adna/ into a new project
│       ├── skill_onboarding.md      # 5-question interview for new projects
│       └── skill_l1_upgrade.md      # L0→L1 phased compute upgrade
├── my_research_lab.aDNA/         # Project A (forked from .adna/, customized)
│   ├── CLAUDE.md                 # Project-specific governance
│   └── ...
├── client_acme.aDNA/             # Project B (forked from .adna/)
│   └── ...
├── latlab/                       # (appears after L1 upgrade — not initially present)
└── lattice-protocol/             # (appears after L1 upgrade — not initially present)
```

### How it works

1. **Clone directly**: `git clone https://github.com/LatticeProtocol/aDNA.git ~/aDNA`
2. **Run Claude Code** from `~/aDNA/` — the root CLAUDE.md detects `.adna/` and offers to create your first project
3. **Create projects** — the agent copies `.adna/`, strips `.obsidian/plugins/` and `.obsidian/themes/`, removes the `role: template` marker, runs `git init`, then triggers the 5-question onboarding interview inside the new project
4. **Work inside projects** — each project is self-contained. Open it directly in Claude Code or Obsidian.
5. **Upgrade to L1** — follow `.adna/how/skills/skill_l1_upgrade.md` to add JupyterHub compute

### Why this pattern

- **Two-command onboarding** — `git clone <url> ~/aDNA && cd ~/aDNA && claude`
- **Every project gets the complete toolkit** — templates, skills, context library, lattice tools
- **Upstream updates** — `git pull` inside `~/aDNA/` updates `.adna/` cleanly
- **Zero config** — the root CLAUDE.md ships pre-authored, no auto-generation needed

> **Workspace-root note**: `~/aDNA/` is the recommended workspace root; any path works — `<workspace_root>` is detected, never hardcoded. Operators on the legacy `~/lattice/` root migrate via `how/skills/skill_workspace_path_migration.md` (a turnkey agentic transition) plus a `~/lattice → ~/aDNA` symlink shim that keeps every existing reference valid mid-migration.

### Design principles

1. **The agent is the scaffolding engine** — the root CLAUDE.md instructs Claude how to fork, customize, and seed new projects
2. **Each project is self-contained** — own CLAUDE.md, own git, own triad structure. Can be moved out of the workspace and still works.
3. **Never modify `.adna/`** — it stays as a clean reference (`role: template` in MANIFEST.md). Only fork from it. `git pull` is always safe.
4. **The root CLAUDE.md is the front door** — it handles all workspace operations (project creation, discovery, L1 upgrade). Inside a project, that project's CLAUDE.md is authoritative.
5. **Lattice as concept** — `~/aDNA/` is the user's personal knowledge lattice. Each `.aDNA` project is a node. The lattice grows as users create more projects.

### Related files

- [Project Fork Skill](../../how/skills/skill_project_fork.md) — forks .adna/ into a new project
- [L1 Upgrade Skill](../../how/skills/skill_l1_upgrade.md) — phased compute upgrade

---

## Advanced Pattern (Custom Templates)

For organizations that want fine-grained control over project scaffolding, the `.base/` template pattern provides per-field customization.

```
~/aDNA/                        # Workspace root (or any folder)
├── CLAUDE.md                     # Meta-governance — interview + scaffold instructions
├── .base/                        # Base template (fork source, not a project)
│   ├── CLAUDE.md.template        # Governance template with {{variables}}
│   ├── MANIFEST.md.template
│   ├── STATE.md.template
│   ├── AGENTS.md.template
│   ├── README.md.template
│   ├── who_AGENTS.md.template
│   ├── what_AGENTS.md.template
│   └── how_AGENTS.md.template
├── my-research-vault/            # Project A (scaffolded)
│   └── ...
└── shared/                       # Optional cross-project context
    └── context/
```

### When to use the advanced pattern

- You need custom template fields beyond what the onboarding interview provides
- Your organization has specific governance requirements that every project must include
- You want a `shared/` directory for cross-project context reuse
- You're building a domain-specific scaffolding system (e.g., all projects in your org must have `what/compliance/`)

### Template variable syntax

`.base/` templates use `{{variable}}` placeholders that map to interview answers:

| Variable | Source | Used in |
|----------|--------|---------|
| `{{project_name}}` | Directory name | CLAUDE.md, MANIFEST.md, README.md |
| `{{project_description}}` | Q1 answer | MANIFEST.md, CLAUDE.md, README.md |
| `{{domain}}` | Q2 answer | CLAUDE.md domain section |
| `{{skeleton_tier}}` | Q3 → tier mapping | Directory structure (controls which subdirs are created, not template text) |
| `{{tooling}}` | Q4 answer | .obsidian/ inclusion |
| `{{persona_name}}` | Q5 answer | CLAUDE.md personality |
| `{{persona_style}}` | Q5 answer | CLAUDE.md operating style |
| `{{created_date}}` | Scaffold date | All frontmatter |

### 4. Shared context is optional

The `shared/` directory is for organizations that want cross-project context reuse — common domain knowledge, shared templates, organizational standards. Solo users can ignore it entirely.

---

## Interview → Scaffold Flow

The 5-question interview (from the [Start Kit PRD](start_kit_prd.md)) drives all scaffolding decisions:

| Q | Question | Maps to |
|---|----------|---------|
| Q1 | What are you building? | `{{project_description}}` → MANIFEST.md, CLAUDE.md identity |
| Q2 | What's your domain? | Ontology extension suggestions (9 presets) |
| Q3 | Team or solo? | Skeleton tier (starter/standard/full per §5.4) |
| Q4 | How will you browse? | .obsidian/ inclusion, .claude/ config |
| Q5 | Agent personality? | CLAUDE.md personality section |

### Domain → Extension Mapping (Q2)

| Domain | Suggested extensions |
|--------|---------------------|
| **research** | `what/papers/`, `what/datasets/`, `what/hypotheses/`, `what/experiments/` |
| **enterprise** | `who/customers/`, `who/partners/`, `who/contacts/`, `who/projects/` |
| **biotech** | `what/experiments/`, `what/compounds/`, `what/protocols/`, `what/targets/` |
| **software** | `how/incidents/`, `how/deployments/`, `what/services/`, `what/apis/` |
| **creative** | `who/clients/`, `what/creative_assets/`, `how/revision_cycles/` |
| **personal** | `what/courses/`, `what/books/`, `how/learning_goals/` |
| **healthcare** | `who/patients/`, `what/treatments/`, `what/protocols/` |
| **legal** | `what/cases/`, `what/contracts/`, `what/compliance/` |
| **content** | `what/publications/`, `how/editorial_pipeline/`, `what/assets/` |

### Team Size → Skeleton Mapping (Q3)

| Team size | Skeleton | Key additions |
|-----------|----------|---------------|
| **solo** | Starter | Minimal governance. No coordination. |
| **small-team** (2-5) | Standard | `who/coordination/`, AGENTS.md chain, STATE.md, session tracking, backlog |
| **organization** (5+) | Full | Standard + `who/governance/`, collision prevention Tier 3, domain extensions |

---

## Relationship to Start Kit

| Concern | Projects Folder Pattern | Start Kit CLI |
|---------|------------------------|---------------|
| **What it is** | A workspace pattern | A CLI tool |
| **Scaffolding engine** | The agent (via CLAUDE.md) | The `adna` shell script |
| **When it ships** | Now (this doc + examples) | Later (`campaign_lattice_start_kit`) |
| **Template format** | `{{variable}}` placeholders | Same templates, resolved by script |
| **Interview** | Agent-guided conversation | Interactive `read`/`select` prompts |

The Projects Folder Pattern is the manual version of what the Start Kit automates. Same templates, same interview, same output — different execution engine.

---

## Usage

### Creating a new project

1. Open Claude Code in `~/aDNA/` (the repo root)
2. Say "Create a new project" (or similar)
3. The root CLAUDE.md guides project creation, delegating to `skill_project_fork.md`
4. `.adna/` is copied to `project_name.aDNA/`, template markers stripped, `git init` run
5. Onboarding triggers automatically on first run inside the new project

### Updating the template

Run `git pull` inside `~/aDNA/` to update `.adna/` with the latest improvements. User projects are unaffected — they have their own git repos.

---

## Related

- [Project Fork Skill](../../how/skills/skill_project_fork.md) — Fork .adna/ into a new project
- [Start Kit PRD](start_kit_prd.md) — CLI tool design (interview, scaffolding, packaging)
- [Onboarding Skill](../../how/skills/skill_onboarding.md) — 10-step interactive flow (expanded version)
- [L1 Upgrade Skill](../../how/skills/skill_l1_upgrade.md) — Phased L0→L1 compute upgrade
- [aDNA Standard §5.4](adna_standard.md) — Skeleton tier definitions
- [Migration Guide](migration_guide.md) — Adding aDNA to existing projects
