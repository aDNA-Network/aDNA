---
type: prd
project_slug: start_kit
project_title: "Lattice Start Kit"
version: "1.0"
owner: <project_owner>
reviewers: []
approved_by: FA
approved_date: 2026-03-19
created: 2026-03-19
updated: 2026-03-19
last_edited_by: agent_init
tags: [prd, start-kit, onboarding, adoption, cli]
---

# PRD: Lattice Start Kit

## Problem Statement

Onboarding a new aDNA project currently requires 6 synchronous steps: clone the repo, run `setup.sh`, open Obsidian, launch Claude Code, complete an interactive interview, then customize governance files. This takes 15-30 minutes and demands that the user understand aDNA architecture upfront — a 309-line CLAUDE.md, a 1,433-line standard document, and a multi-plugin Obsidian setup.

This friction kills adoption. Researchers want to add structured knowledge management to an existing project in minutes, not hours. Developers working terminal-only must manually fill Templater placeholders designed for Obsidian. Team leads have no guidance for multi-user vault setup. New users exploring aDNA for the first time face a cliff of complexity before writing their first context file.

The Lattice Start Kit reduces this to: install → answer 5 questions → start working. The interview front-loads project customization *before* scaffolding, producing a fully configured vault in under 2 minutes with zero manual file editing.

**Why now**: The migration guide (M04), agent-first guide (M05), standard reading guide (M07), and existing `skill_onboarding.md` define what a start kit needs to scaffold. This PRD synthesizes them into a buildable product spec.

## Users & Stakeholders

### Persona 1: Researcher (existing project)

| Attribute | Detail |
|-----------|--------|
| **Entry point** | Has an existing repo (Python, R, or mixed), wants aDNA added |
| **Pain today** | Migration guide is 540+ lines. Bare-vs-embedded decision is unclear without reading the full walkthrough. Manual directory creation + governance file authoring takes 10-15 minutes. |
| **What the kit gives them** | `adna init` detects existing project context (package.json, pyproject.toml, Cargo.toml), auto-selects embedded triad, asks 5 questions, scaffolds `.agentic/` structure with generated governance files. Under 2 minutes. |

**User story**: *As a researcher with an existing project, I want to add aDNA to my repo by running a single command that detects my project structure and generates the right files, so I can start using AI agents productively without reading the full migration guide.*

`REQ-SK-001` — `adna init` command for existing projects.

### Persona 2: New User (starting fresh)

| Attribute | Detail |
|-----------|--------|
| **Entry point** | No project yet. Exploring aDNA for the first time. |
| **Pain today** | Clone → `setup.sh` → 6-step process → 15-30 min before productive. Must understand triad structure, governance files, and agent protocol before writing a single file. |
| **What the kit gives them** | `adna new my-project` → 5 questions → fully configured vault with personalized CLAUDE.md, populated MANIFEST.md, initial STATE.md, domain-specific ontology extensions. Ready in <2 min. |

**User story**: *As a new user exploring aDNA, I want to create a customized vault by answering a few questions, so I can start working immediately without understanding the full aDNA architecture upfront.*

`REQ-SK-002` — `adna new` command for fresh projects.

### Persona 3: Developer (terminal-only)

| Attribute | Detail |
|-----------|--------|
| **Entry point** | VS Code or terminal workflow. No Obsidian. |
| **Pain today** | Agent-first guide still requires cloning, skipping `setup.sh`, then manually editing governance files. Templater placeholders in templates don't resolve without Obsidian. |
| **What the kit gives them** | `adna new --no-obsidian` skips `.obsidian/` config and plugin download, generates `.claude/settings.json` instead, produces templates with resolved values (no `<% tp.date.now() %>` remnants). |

**User story**: *As a developer who uses the terminal and VS Code, I want to set up an aDNA vault without Obsidian-specific files, so my workspace stays clean and agent-ready without plugins I won't use.*

`REQ-SK-003` — `--no-obsidian` flag for terminal-first setup.

### Persona 4: Team Lead (multi-user)

| Attribute | Detail |
|-----------|--------|
| **Entry point** | Needs a shared vault for 2-10 collaborators. |
| **Pain today** | No guidance on multi-user setup. Collision prevention (read-before-write, `last_edited_by` tracking) is documented but not scaffolded. No `coordination/` directory, no per-user AGENTS.md, no git remote setup. |
| **What the kit gives them** | `adna new --team` scaffolds `who/coordination/`, generates per-user AGENTS.md stubs, inits git repo with `.gitignore`, adds collision prevention section to CLAUDE.md. |

**User story**: *As a team lead setting up a shared vault, I want the scaffolding tool to create multi-user coordination infrastructure, so my team can start collaborating without manually configuring collision prevention.*

`REQ-SK-004` — `--team` flag for multi-user scaffolding.

## Requirements

### Must Have

| ID | Requirement | Acceptance Criteria | Notes |
|----|------------|-------------------|-------|
| REQ-SK-001 | `adna init` command for existing projects | Detects project markers (package.json, pyproject.toml, Cargo.toml, go.mod). Auto-selects embedded triad (`.agentic/`). Generates CLAUDE.md, MANIFEST.md, STATE.md at repo root. Creates `.agentic/who/`, `.agentic/what/`, `.agentic/how/` with AGENTS.md per directory. Does not overwrite existing files (appends aDNA nav section to existing README). | Flow B in mockups |
| REQ-SK-002 | `adna new` command for fresh projects | Creates named project directory. Generates full governance file set. Applies skeleton tier from Q3 (starter/standard/full). Populates all files with interview answers — no manual editing required. | Flow A in mockups |
| REQ-SK-003 | Pre-flight interview (5 questions, ≤60 seconds) | Q1: project description (free text). Q2: domain (7 presets + other). Q3: team size (solo/small-team/organization). Q4: tooling (obsidian/terminal-only/vs-code/other). Q5: agent personality (berthier/custom/none). Each answer maps to a template variable. | See Interview Design section |
| REQ-SK-004 | Three skeleton tiers | Starter (solo): CLAUDE.md + MANIFEST.md + README + triad + 7 subdirs. Standard (small-team): adds STATE.md + AGENTS.md chain + active/history session dirs + backlog. Full (organization): adds domain extensions + coordination + governance tiers. Must match `adna_standard.md` §5.4. | Per-tier file counts verified against standard |
| REQ-SK-005 | Governance file generation | Generated CLAUDE.md includes: project identity (from Q1), agent protocol, safety rules, domain section (from Q2). Generated MANIFEST.md includes: project description, architecture stub. Generated STATE.md includes: "Phase 1 — Setup Complete" initial state. All files pass frontmatter validation (type, created, updated, last_edited_by, tags). | Zero Templater placeholders in output |
| REQ-SK-006 | Obsidian/terminal toggle | Q4=obsidian: include `.obsidian/` config, CSS snippets, run plugin download. Q4=terminal-only: skip `.obsidian/`, generate `.claude/settings.json` with project-appropriate permissions. Q4=vs-code: skip `.obsidian/`, generate `.vscode/settings.json` stub. | No Obsidian-only syntax in terminal output |

### Should Have

| ID | Requirement | Acceptance Criteria | Notes |
|----|------------|-------------------|-------|
| REQ-SK-010 | Domain-specific ontology suggestions | Q2 answer maps to domain extension table (from `skill_onboarding.md` Step 6): research → `what/papers/`, `what/datasets/`; biotech → `what/experiments/`, `what/targets/`; enterprise → `who/customers/`, `who/contacts/`; etc. User confirms before creation. | 9 domain presets from onboarding skill |
| REQ-SK-011 | Agent personality customization | Q5=berthier: keep default personality in CLAUDE.md. Q5=custom: prompt for name + 3 operating principles, generate personality section. Q5=none: strip personality, keep functional CLAUDE.md only. | Mirrors `skill_onboarding.md` Step 8 |
| REQ-SK-012 | First-session auto-creation | Generate an onboarding session file in `how/sessions/active/` recording what the kit configured. Session file includes: interview answers, files created, suggested next steps. | Provides continuity for the first agent session |
| REQ-SK-013 | Git initialization | `adna new`: init git repo, generate `.gitignore` (exclude `.claude/`, `.mcp.json`, `workspace.json`, `graph.json`). `adna init`: verify existing git repo, update `.gitignore` if needed. Team mode: prompt for remote URL. | Does not auto-push — user controls when to push |

### Could Have

| ID | Requirement | Acceptance Criteria | Notes |
|----|------------|-------------------|-------|
| REQ-SK-020 | Web configurator | Browser-based interview → generates zip download with complete vault. Same 5-question flow, visual preview of directory structure before download. | Phase 3 aspiration — overengineered for v1 |
| REQ-SK-021 | `latlab scaffold` integration | Same scaffolding as `adna new` but invoked via `latlab scaffold vault`. Shares templates. Adds Lattice Protocol-specific extensions (federation, registry). | Phase 2 — ties to `idea_build_kit_scaffold_cli.md` |
| REQ-SK-022 | Plugin auto-install | Obsidian plugin download and configuration as part of setup. Currently handled by `setup.sh`. | Medium effort — Obsidian plugin API changes frequently |
| REQ-SK-023 | VS Code extension | "New aDNA Vault" command in VS Code command palette. Same interview flow. | Narrow audience — defer |

### Won't Have (this version)

| ID | Requirement | Rationale |
|----|------------|-----------|
| REQ-SK-090 | Electron/desktop app | Heavy packaging overhead for a CLI that runs in <2 min. No user demand signal. |
| REQ-SK-091 | Migration from non-aDNA vaults | Importing from Notion, Confluence, Roam etc. requires format-specific parsers. Out of scope for v1 — file under separate campaign. |
| REQ-SK-092 | Remote vault creation | Cloud-hosted vault provisioning. Requires server infrastructure. Deferred to federation roadmap. |
| REQ-SK-093 | Team invite system | User management, permissions, access control. Requires identity layer (`campaign_iam_identity_layer`). |
| REQ-SK-094 | Auto-updating vaults | "Check for aDNA standard updates" mechanism. Deferred to `campaign_adna_ecosystem_evolution` Phase 2 (M10 — Version Migration Prompt System). |

## Packaging Evaluation

Five packaging options scored on four axes (1-5 scale):

| Option | Effort | Reach | Maintenance | UX | Total | Verdict |
|--------|--------|-------|-------------|-----|-------|---------|
| **Shell script** (`adna` CLI) | 5 (Low) | 5 (Any terminal) | 5 (Low) | 4 (Interactive prompts) | **19** | **MVP — recommended** |
| **`latlab scaffold` subcommand** | 3 (Python, click) | 3 (Requires latlab install) | 3 (Medium) | 4 (Good) | **13** | **Phase 2 integration** |
| **Obsidian plugin** | 3 (TypeScript) | 3 (Obsidian only) | 2 (API changes) | 5 (Native UX) | **13** | Defer — locks to Obsidian |
| **VS Code extension** | 2 (Medium-High) | 3 (VS Code users) | 2 (API changes) | 4 (Good) | **11** | Defer — narrow audience |
| **Web configurator** | 1 (Frontend + backend) | 5 (Browser) | 2 (High) | 5 (Best for non-devs) | **13** | Defer — overengineered for v1 |

**Recommendation**: Shell script as MVP. Cross-platform (bash/zsh), zero dependencies, interactive prompts via `read`/`select`, runs anywhere a terminal exists. The `adna` script ships in the repo root and can be `curl | sh` installed or aliased.

**Phase 2**: Integrate into `latlab scaffold` (Python + click). Shares the same templates but adds Lattice Protocol-specific extensions (federation config, registry setup). Relates to `idea_build_kit_scaffold_cli.md`.

**Phase 3 aspiration**: Web configurator. Browser-based interview with live directory preview, generates downloadable zip. Highest reach (works without any local tooling) but requires hosted infrastructure.

## Pre-Flight Interview Design

Five questions, ~60 seconds total. Each answer maps to template variables that drive file generation.

### Interview Flow

```
╔═══════════════════════════════════════════════════════════════════╗
║                    LATTICE START KIT                             ║
║                    Pre-Flight Interview                         ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  Q1: What are you building?                                       ║
║      → Free text                                                  ║
║      → Maps to: MANIFEST.md description, CLAUDE.md identity      ║
║                                                                   ║
║  Q2: What's your domain?                                          ║
║      → [research / enterprise / biotech / software /              ║
║         creative / personal / other]                              ║
║      → Maps to: ontology extension suggestions                    ║
║                                                                   ║
║  Q3: Team or solo?                                                ║
║      → [solo / small-team (2-5) / organization (5+)]             ║
║      → Maps to: skeleton tier, coordination scaffold              ║
║                                                                   ║
║  Q4: How will you browse the vault?                               ║
║      → [obsidian / terminal-only / vs-code / other]              ║
║      → Maps to: .obsidian/ inclusion, .claude/ config             ║
║                                                                   ║
║  Q5: Agent personality?                                           ║
║      → [berthier (default) / custom / none]                      ║
║      → Maps to: CLAUDE.md personality section                     ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

### Output Mapping

| Question | Variable | Feeds into |
|----------|----------|-----------|
| Q1 (project description) | `{project_description}` | MANIFEST.md `## What This Is`, CLAUDE.md `## Identity`, README.md heading |
| Q2 (domain) | `{domain}` | Ontology extension suggestions (9 domain presets from `skill_onboarding.md` Step 6), CLAUDE.md `## Domain` section |
| Q3 (team size) | `{skeleton_tier}` + `{team_size}` | Skeleton selection (starter/standard/full per §5.4), `who/coordination/` scaffold, collision prevention tier in CLAUDE.md |
| Q4 (tooling) | `{tooling}` | `.obsidian/` inclusion/exclusion, `.claude/settings.json` or `.vscode/settings.json` generation, template format (resolved vs. Templater syntax) |
| Q5 (personality) | `{persona}` | CLAUDE.md personality section: Berthier default, custom (name + 3 principles), or stripped functional-only |

### Domain → Extension Mapping (Q2)

| Domain | Suggested extensions (user confirms) |
|--------|--------------------------------------|
| **research** | `what/papers/`, `what/datasets/`, `what/hypotheses/`, `what/experiments/` |
| **enterprise** | `who/customers/`, `who/partners/`, `who/contacts/`, `who/projects/` |
| **biotech** | `what/experiments/`, `what/compounds/`, `what/protocols/`, `what/targets/` |
| **software** | `how/incidents/`, `how/deployments/`, `what/services/`, `what/apis/` |
| **creative** | `who/clients/`, `what/creative_assets/`, `how/revision_cycles/`, `what/portfolio/` |
| **personal** | `what/courses/`, `what/books/`, `how/learning_goals/`, `what/skills/` |
| **other** | No auto-suggestions — ask user for 2-3 entity types they expect to manage |

### Team Size → Skeleton Mapping (Q3)

| Team size | Skeleton | Additions |
|-----------|----------|-----------|
| **solo** | Starter | Minimal governance. No coordination directory. |
| **small-team (2-5)** | Standard | `who/coordination/`, `AGENTS.md` chain, `STATE.md`, session tracking with `active/`+`history/`, backlog |
| **organization (5+)** | Standard + governance extensions | Standard + `who/governance/`, collision prevention Tier 3 (read-before-write + `updated` check + `last_edited_by`), per-user AGENTS.md stubs |

## "Start New Project" Flow

### Flow A: `adna new` (fresh project)

```
$ adna new my-research-vault

  ╭──────────────────────────────────────╮
  │   Lattice Start Kit v1.0             │
  │   Creating: my-research-vault        │
  ╰──────────────────────────────────────╯

  Q1: What are you building?
  > A platform for tracking rare disease genomics research

  Q2: What's your domain?
  > [1] research  [2] enterprise  [3] biotech  [4] software
    [5] creative  [6] personal    [7] other
  > 3

  Suggested extensions for biotech:
    what/experiments/  what/compounds/  what/protocols/  what/targets/
  Include these? [Y/n] y

  Q3: Team or solo?
  > [1] solo  [2] small-team (2-5)  [3] organization (5+)
  > 2

  Q4: How will you browse the vault?
  > [1] obsidian  [2] terminal-only  [3] vs-code  [4] other
  > 2

  Q5: Agent personality?
  > [1] berthier (structured chief of staff) [default]
    [2] custom (you choose name + style)
    [3] none (functional only)
  > 1

  Creating my-research-vault/
    ├── CLAUDE.md ............... ✓  (berthier, biotech domain)
    ├── MANIFEST.md ............. ✓  (rare disease genomics)
    ├── STATE.md ................ ✓  (Phase 1 — Setup Complete)
    ├── AGENTS.md ............... ✓  (root index)
    ├── README.md ............... ✓  (project overview)
    ├── what/
    │   ├── AGENTS.md ........... ✓
    │   ├── context/ ............ ✓
    │   ├── decisions/ .......... ✓
    │   ├── experiments/ ........ ✓  (biotech extension)
    │   ├── compounds/ .......... ✓  (biotech extension)
    │   ├── protocols/ .......... ✓  (biotech extension)
    │   └── targets/ ............ ✓  (biotech extension)
    ├── how/
    │   ├── AGENTS.md ........... ✓
    │   ├── missions/ ........... ✓
    │   ├── sessions/
    │   │   ├── active/ ......... ✓
    │   │   └── history/ ........ ✓
    │   ├── templates/ .......... ✓  (starter set)
    │   └── backlog/ ............ ✓
    └── who/
        ├── AGENTS.md ........... ✓
        ├── coordination/ ....... ✓  (team mode)
        └── governance/ ......... ✓

  Git initialized. .gitignore created.
  Session file: how/sessions/active/session_onboarding.md

  ╭──────────────────────────────────────╮
  │   Ready! Run `claude` to start.      │
  │   Total time: 47 seconds             │
  ╰──────────────────────────────────────╯
```

### Flow B: `adna init` (existing project)

```
$ cd my-existing-repo && adna init

  ╭──────────────────────────────────────╮
  │   Lattice Start Kit v1.0             │
  │   Adding aDNA to: my-existing-repo   │
  ╰──────────────────────────────────────╯

  Detected: pyproject.toml, src/, tests/
  Recommended form: embedded triad (.agentic/)
  Use embedded form? [Y/n] y

  Q1: What are you building?
  > A protein structure prediction pipeline

  Q2: What's your domain?
  > [1] research  [2] enterprise  [3] biotech  [4] software
    [5] creative  [6] personal    [7] other
  > 3

  Q3: Team or solo?
  > [1] solo  [2] small-team (2-5)  [3] organization (5+)
  > 1

  Q4: How will you browse the vault?
  > [1] obsidian  [2] terminal-only  [3] vs-code  [4] other
  > 2

  Q5: Agent personality?
  > [1] berthier  [2] custom  [3] none
  > 1

  Creating aDNA layer:
    ├── CLAUDE.md ............... ✓  (at repo root)
    ├── MANIFEST.md ............. ✓  (at repo root)
    ├── STATE.md ................ ✓  (at repo root)
    ├── .agentic/
    │   ├── AGENTS.md ........... ✓  (bridge to root governance)
    │   ├── who/
    │   │   └── AGENTS.md ....... ✓
    │   ├── what/
    │   │   ├── AGENTS.md ....... ✓
    │   │   ├── context/ ........ ✓
    │   │   └── experiments/ .... ✓  (biotech extension)
    │   └── how/
    │       ├── AGENTS.md ....... ✓
    │       ├── sessions/
    │       │   └── active/ ..... ✓
    │       └── templates/ ...... ✓
    ├── README.md ............... ✓  (aDNA nav section appended)
    └── .gitignore .............. ✓  (updated — .claude/, .mcp.json)

  Session file: .agentic/how/sessions/active/session_onboarding.md

  ╭──────────────────────────────────────╮
  │   aDNA layer added!                  │
  │   Run `claude` to start.             │
  │   Total time: 38 seconds             │
  ╰──────────────────────────────────────╯
```

### Key Flow Differences

| Aspect | `adna new` | `adna init` |
|--------|-----------|-------------|
| **Directory** | Creates new directory | Works in existing directory |
| **Form** | Bare triad (default) | Embedded triad (auto-detected) |
| **README** | Generates new README | Appends aDNA section to existing |
| **Git** | Initializes new repo | Verifies existing repo, updates .gitignore |
| **Skeleton** | All three tiers available | Starter or Standard only (Full is overkill for embedded) |
| **Existing files** | N/A | Never overwrites — detects and appends |

## Scope

### In Scope

- CLI tool design (shell script MVP)
- Pre-flight interview specification (5 questions with output mapping)
- Scaffolding logic for both `adna new` and `adna init` flows
- Governance file generation templates (CLAUDE.md, MANIFEST.md, STATE.md, AGENTS.md)
- Three skeleton tiers (starter, standard, full per `adna_standard.md` §5.4)
- Obsidian/terminal/VS Code tooling toggle
- Domain-specific ontology extension suggestions (9 presets)
- Agent personality customization (3 options)

### Out of Scope

| Item | Rationale | Destination |
|------|-----------|-------------|
| Building the CLI | This PRD is design only. Building is a separate engineering campaign. | New campaign: `campaign_lattice_start_kit` |
| Web configurator implementation | Overengineered for v1. Design noted as Phase 3 aspiration. | Phase 3 of build campaign |
| IDE plugins (Obsidian/VS Code) | Narrow audience, high maintenance. | Deferred indefinitely |
| Migration from non-aDNA systems | Requires format-specific parsers (Notion, Confluence, Roam). | Separate campaign if demand emerges |
| Team invite/permissions system | Requires identity layer infrastructure. | `campaign_iam_identity_layer` |
| Version migration/update system | Version migration is a separate concern. | `campaign_adna_ecosystem_evolution` Phase 2 (M10) |

## Dependencies

| Dependency | Type | Status | Risk |
|-----------|------|--------|------|
| `adna_standard.md` §5.4 (skeleton definitions) | Internal | Available (v2.1) | Low — stable specification |
| `skill_onboarding.md` (interview flow, domain extensions) | Internal | Available | Low — established patterns |
| `migration_guide.md` (init flow, embedded triad patterns) | Internal | Available (v1.0) | Low — just published |
| `agent_first_guide.md` (terminal-only patterns, substitution table) | Internal | Available (v1.0) | Low — just published |
| `how/templates/` (starter template set) | Internal | Available | Low — 17 templates exist |
| `idea_build_kit_scaffold_cli.md` (latlab scaffold proposal) | Internal | Proposed | Medium — Phase 2 dependency, not blocking MVP |
| Bash/Zsh availability on target platforms | Technical | Available | Low — standard on macOS/Linux. Windows: WSL or Git Bash |

## Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Time from install to productive vault | **<2 minutes** (from current 15-30 min) | Timed walkthrough with each persona |
| Interview questions | **≤5** (from current 10+ in skill_onboarding) | Count |
| Generated files pass aDNA standard validation | **100%** | Run frontmatter validator against output |
| Manual file editing required before first agent session | **Zero** | Verify agent starts cleanly on generated vault |
| User can describe their vault's purpose after setup | **100%** | Ask user "what does this vault do?" — answer matches Q1 input |
| Interview completion rate | **>90%** | Track Q1-Q5 completion (no dropoffs) |
| Correct skeleton tier selection | **>95%** | Q3 maps to appropriate skeleton per §5.4 |

## Timeline

| Milestone | Effort Estimate | Dependencies |
|-----------|----------------|--------------|
| MVP CLI (`adna new` + `adna init` + interview) | 2-3 sessions | PRD approval (this document) |
| Template library (governance file generators) | 1 session | MVP CLI structure |
| Test suite (all 4 personas, both flows) | 1 session | MVP CLI + templates |
| Documentation (README section, install instructions) | 0.5 session | All above |
| **Total MVP** | **~5 sessions** | — |
| Phase 2: `latlab scaffold` integration | 2-3 sessions | MVP CLI + latlab codebase |
| Phase 3: Web configurator | 5-8 sessions | MVP CLI + hosting infrastructure |

## Resolved Questions (DG1 — 2026-03-19)

- [x] **Where does the CLI live?** — **Both** (option c). Standalone `adna` shell script as MVP, `latlab scaffold` wraps it later. *FA approved 2026-03-19.*
- [x] **Generated CLAUDE.md size** — **~100 lines**. Functional core + personality + domain section. Omit advanced features (campaigns, pipelines, skills) that users discover organically. *FA approved 2026-03-19.*
- [x] **Template inclusion** — **Tier-dependent**. 4 templates for solo, 7 for small-team, 17 for organization. *FA approved 2026-03-19.*
- [x] **Distribution method** — **Repo-bundled + curl**. `curl` install for frictionless onboarding, repo-bundled as fallback. *FA approved 2026-03-19.*
- [x] **Windows support** — **WSL-only** for MVP. PowerShell port if user demand signal emerges. *FA approved 2026-03-19.*

> **Note**: PRD approved as reference artifact. Building deferred to separate campaign (`campaign_lattice_start_kit`) when aDNA standard stabilizes.

## Related

- **Existing onboarding skill**: [`how/skills/skill_onboarding.md`](../../how/skills/skill_onboarding.md) — 10-step interactive interview (258 lines). The Start Kit front-loads and compresses this into 5 pre-scaffold questions.
- **Migration guide**: [`what/docs/migration_guide.md`](migration_guide.md) — step-by-step `adna init` patterns for bare and embedded triads.
- **Agent-first guide**: [`what/docs/agent_first_guide.md`](agent_first_guide.md) — terminal-only setup, feature parity audit, Claude Code configuration.
- **Standard reading guide**: [`what/docs/standard_reading_guide.md`](standard_reading_guide.md) — persona-based paths through the standard.
- **Skeleton definitions**: [`what/docs/adna_standard.md`](adna_standard.md) §5.4 — starter, standard, full skeleton specifications.
- **Build Kit scaffold proposal**: `idea_build_kit_scaffold_cli.md` — proposed `latlab scaffold` command (Phase 2 integration path).
- **Architecture diagram**: [`what/docs/adna_design.md`](adna_design.md) — triad structure and deployment forms the kit scaffolds.

---

*Start Kit PRD v1.0 | Design document — building deferred to `campaign_lattice_start_kit` | 2026-03-19*
