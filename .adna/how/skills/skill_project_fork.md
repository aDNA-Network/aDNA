---
type: skill
skill_type: agent
created: 2026-03-23
updated: 2026-06-19
status: active
category: onboarding
trigger: "Root CLAUDE.md project creation flow — user wants to create a new project"
last_edited_by: agent_rosetta
tags: [skill, project, fork, onboarding, lattice, exemplar_home, hearthstone_p4]

requirements:
  tools: []
  context: ["CLAUDE.md", "MANIFEST.md"]
  permissions: ["copy directories", "write files in workspace directory", "remove .git and .obsidian from fork"]
---

# Skill: Project Fork

## Overview

Creates a new aDNA project by forking the `.adna/` base template. The fork receives the full aDNA structure (triad, templates, skills, context library, lattice tools) as a new project with its own git repository. The forked project's `MANIFEST.md` is prepared for first-run onboarding.

This skill is called from the **root CLAUDE.md** at `~/aDNA/CLAUDE.md` when a user wants to create a new project.

## Trigger

Invoked by the root CLAUDE.md project creation flow. Not triggered automatically — always called from the root governance.

## Parameters

| Parameter | Source | Required |
|-----------|--------|----------|
| `carry_forward_answers` | Any project name/description already collected from the calling flow | No |
| `--exemplar-home` | Flag — overlay the premium exemplar HOME bundle (`template_node_adna_exemplar/`) after the base fork (auto-implied when the fork is a `Home.aDNA`-class node vault). See Step 4.5. | No |

The workspace root is always the directory containing this `.adna/` template (detected automatically). The template source is always `.adna/`.

> **Exemplar overlay (Hearthstone P4).** The themed HOME is normally materialized by `skill_node_bootstrap_interview.md` Step 9 during the Step-0.3 bootstrap chain; the `--exemplar-home` flag (Step 4.5) lets the fork trigger the same overlay directly, in one pass, without waiting for the interview. Both are opt-in and idempotent — a fork that declines keeps the plain base `.adna/HOME.md`.

## Requirements

### Tools/APIs
- File copy (`cp -r`)
- File deletion (`rm -rf .obsidian/plugins/ .obsidian/themes/`)
- Git init (`git init`)
- File read/write (MANIFEST.md frontmatter editing)

### Context Files
- `.adna/MANIFEST.md` — to verify `role: template` in the source and strip it in the fork

### Permissions
- Write to the workspace root directory (same level as `.adna/`)
- Copy the `.adna/` directory structure

## Implementation

### Step 1: Collect Project Identity

If `carry_forward_answers` are provided (from the calling flow), use them. Otherwise ask:

1. **Project name** — base folder name (the `.aDNA` suffix is appended automatically). Must be lowercase with underscores. Example: `my_research_lab`, `acme_crm`, `sleep_study` → creates `my_research_lab.aDNA/`
2. **Brief description** — 1-2 sentences describing the project's purpose

Validate the project name (per [ADR-009](../../what/decisions/adr_009_aDNA_naming_convention.md) §1 + §4):
- **Snake_case pattern**: must match `[a-z][a-z0-9_]*` — lowercase letter start, then lowercase letters / digits / underscores only. (Per ADR-009 §1.)
- Must not collide with an existing directory in the workspace
- Must not be `.adna` (that's the base template; ADR-009 §3.4 template-repo exception)
- Must not be `latlab` or `lattice-protocol` (infrastructure repos)

**Non-conformant name handling** (per ADR-009 §4 enforcement table): if the operator supplies a name that fails the snake_case pattern (e.g., `my-project`, `MyProject`, `1starts_with_digit`), warn explicitly with a citation to ADR-009 §1 and prompt for a corrected form. The operator MAY override and continue with the non-conformant name; if they do, the fork is treated as an ADR-009 §3 exception (4 grandfathered classes: hyphen-flat / no-remote / path-style / template-repo) and SHOULD be documented in `who/coordination/` of the resulting vault for audit transparency.

**Home-class fork**: `project_name = Home` (or a `--home` flag) is a recognized special class — it creates the per-node operational vault `Home.aDNA/` and triggers the Hestia governance install in **Step 3.5**. It is normally invoked by the workspace router's Step 0.3 "offer to bootstrap Home" chain (followed by `skill_inventory_refresh` → `skill_node_bootstrap_interview` → `skill_node_health_check`).

### Step 2: Confirm Target Location

The target directory is `<workspace_root>/<project_name>.aDNA/` (the `.aDNA` suffix marks it as an aDNA project — see Standard §3.5).

Report to the user:
> "I'll create your project at `<project_name>.aDNA/`. This will fork the full aDNA structure — triad directories, templates, skills, context library, and lattice tools. The base template at `.adna/` stays untouched."

If the user explicitly requests no suffix, respect their preference.

Ask for confirmation before proceeding.

**Exemplar-mode detection**: if `--exemplar-home` was passed, or the fork is a `Home.aDNA`-class node vault (per-node operational vault — Hestia or another node persona), set `exemplar_mode = true` and tell the user the fork will additionally receive the premium exemplar HOME (banner + §Gallery + §Topology + persona CSS). The overlay runs at Step 4.5, after the base structure is in place. Exemplar mode is always opt-in: a non-Home fork without the flag stays `exemplar_mode = false` and keeps the plain base HOME.

### Step 3: Fork the Template

```bash
cp -r .adna/ <project_name>.aDNA/
cd <project_name>.aDNA/

# Post-v7.0 (M03 flatten) exclusions: .adna/ IS the cloned repo, so the cp -r
# carries through the template's repo-level files. Remove them so the new project
# starts clean per regression-test R2-R7 (M01 Obj 2 runbook §6):
rm -rf .git              # R1: discard template git history (skill_project_fork installs fresh below)
rm -rf .github           # R2: no CI configs leaked into forked project
rm -f README.md          # R3: no template README at fork root (project authors own)
rm -f LICENSE            # R4: no template LICENSE (project picks own license)
# R6 prepare_for_onboarding.sh is no-op at fork root (moved to how/skills/l1_upgrade/ in v7.0 M03 B2)
# R7 deploy_manifest.yaml is no-op at fork root (moved to .github/ in v7.0 M03 B3 — covered by rm -rf .github above)

# Preserve portable Obsidian config (settings, appearance, snippets)
# but remove plugin binaries (15MB+) — user runs setup.sh to install them
rm -rf .obsidian/plugins/ .obsidian/themes/
rm -f .obsidian/workspace.json .obsidian/graph.json

git init
```

Note: pre-v7.0 the inner `.adna/` had no `.git/` (it was inside the outer `adna/` repo). Post-v7.0 (M03 flatten), `.adna/` IS the cloned repo with its own `.git/`. The `rm -rf .git` step above is required to discard template git history before `git init` creates the fresh repo for the new project.

This gives the new project:
- The full `who/what/how/` triad structure
- All templates, skills, context library, and lattice tools
- A fresh git repository with no history
- Portable Obsidian config (app settings, appearance, CSS snippets, hotkeys, plugin list)
- Run `./setup.sh` to download plugins and theme (~15MB, requires network)

### Step 3.5: Home-class governance install (only when `project_name = Home`)

A Home fork is the per-node operational vault, and the generic base `.adna/CLAUDE.md` (the **Berthier** workspace-router persona) is the wrong governance file for it. For a Home-class fork only, replace the inherited `CLAUDE.md` with the **Hestia** node-operational template:

1. Copy `.adna/how/templates/template_home_claude.md` over the forked `Home.aDNA/CLAUDE.md`.
2. Substitute the bootstrap variables in the new `CLAUDE.md`:
   - `{{persona}}` → `Hestia` (the default Home-class hearth-keeper; the interview may swap it)
   - `{{node_hostname}}` → machine hostname (`scutil --get LocalHostName` on macOS, else `hostname`)
   - `{{operator}}` → operator username (`whoami`)
   - `{{workspace_root}}` → the workspace root path (the directory containing `.adna/`, e.g. `~/aDNA/`)
   - `{{created_date}}` → today's date (`YYYY-MM-DD`)
3. Leave the persona-accent prose at its Hestia default. `skill_node_bootstrap_interview.md` later enriches the persona grounding, greeting accent, and node-local pairings — and swaps the `<!-- persona-accent -->` blocks if a non-Hestia persona is chosen.

The base `.adna/` template already ships the `what/inventory/` + `who/identity/` base-type scaffolds (`AGENTS.md`), so the Home fork inherits them automatically; `skill_inventory_refresh.md` then populates the entries.

> **Home-class onboarding** is the node bootstrap interview (`skill_node_bootstrap_interview.md`), invoked by the router's Step 0.3 chain — not the generic `skill_onboarding.md` of Step 5. The `agent_init` markers set in Step 4 still trigger first-run detection.

Result: a Home fork is governed by Hestia (not the generic Berthier base) from first open.

### Step 4: Prepare for Onboarding

Edit the forked project's governance files to set up first-run detection:

**MANIFEST.md:**
- Remove `role: template` from frontmatter (or delete the field entirely)
- Set `last_edited_by: agent_init`
- Set `updated: <today's date>`
- If the user provided a project description in Step 1, update the project description section

**STATE.md:**
- Set `last_edited_by: agent_init`
- Set `updated: <today's date>`

**CLAUDE.md:**
- Set `last_edited_by: agent_init` in frontmatter
- Set `updated: <today's date>` in frontmatter
- **Persona token** (ADR-042 Class-1): the inherited `CLAUDE.md` carries a `{{persona}}` placeholder in its Identity & Personality section, not a hard-coded name. For a non-Home fork, leave `{{persona}}` as the placeholder for onboarding Step 8 to resolve — or substitute it now from `carry_forward_answers` if a persona name was supplied. (Mirrors the Home-class `{{persona}}` → `Hestia` substitution at Step 3.5; ensures a fresh fork never inherits the base `Berthier` name.)

These markers ensure the project's CLAUDE.md first-run detection will trigger `skill_onboarding.md` on next open.

### Step 4.5: Exemplar HOME overlay (exemplar mode only)

Run only when `exemplar_mode == true` (Step 2). The base fork already laid down `.adna/HOME.md` (the plain inventory HOME); this step overlays the **premium themed superset** from the exemplar bundle the fork carries at `how/templates/template_node_adna_exemplar/` (copied in from `.adna/` at Step 3). Its `README.md` documents the flow; `SUBSTITUTIONS.md` is the authoritative `{{var}}` catalog. In brief:

1. **Collect/confirm theming inputs** beyond the base identity (hostname/operator/persona): the `{{persona}}` accent triple (`{{accent_primary_hex}}` / `secondary` / `tertiary`), the canvas text pair (`{{canvas_text_strong_hex}}` / `{{canvas_text_em_hex}}`), `{{persona_greeting}}`, and a `{{banner_image}}` (the placeholder ships until the operator supplies a real banner). `SUBSTITUTIONS.md` §2 has a per-persona default lookup for all five hexes — accept-all-in-one-keypress. (When the Step-0.3 chain runs the interview instead, these are its **Topic 6**; this flag collects the same set inline.)
2. **Materialize each `*.template`**: substitute every `{{var}}` per `SUBSTITUTIONS.md`, then drop the `.template` suffix. The two `{{persona_lower}}_*.css.template` files are renamed with the persona too (e.g. `hestia_accent.css` + `hestia_canvas.css` — the canvas-chrome snippet is **required** for the topology canvas). `HOME.md.template` → `HOME.md` (replaces the base `.adna/HOME.md`). **Callout-fold rule (load-bearing):** each `{{vaults_table}}` / `{{named_projects_table}}` body line must be `>`-prefixed so it renders INSIDE the `> [!abstract]-` / `> [!note]-` disclosure folds — never a `<div>` or a blank-line-bearing markdown table (see `skill_node_bootstrap_interview.md` Step 9(b) + `SUBSTITUTIONS.md`).
   *(Dry-run/skeleton tool: `python smoke_render.py --materialize DIR` renders the whole bundle with a fabricated profile — useful for smoke-testing the overlay, not for production values.)*
3. **Copy the generators verbatim** (`what/code/build_*.py` — they carry no `{{vars}}`; they read env + inventory at runtime) and rename `topology_relationships.yaml.template` → `topology_relationships.yaml`.
4. **Lay down the skeleton** (`who/assets/` subdirs incl. the icon classes + `who/curation/curation_schema.yaml` + the `canvasforge/` wrapper) and enable **both** CSS snippets under Appearance → CSS snippets.
5. **Copy `ONBOARDING.md` to the fork root** — the first-run walkthrough the operator reads before anything else; it covers steps 4–6 from the fork's side and is deleted after setup.
6. **First regen** (after `skill_inventory_refresh` populates inventory): `CANVAS_CORE_HOME=… TOPOLOGY_GENERATED_DATE=$(date +%F) python what/code/build_topology_canvas.py` and `python what/code/build_curation_cards.py` — these fill §Topology and §Gallery. (`CANVAS_CORE_HOME` locates the `canvas_core` producer in `Canvas.aDNA`, ADR-004; the generator degrades with a clear message if absent — `SUBSTITUTIONS.md` §3. Deprecated alias: `CANVASFORGE_CODE`.)

Leave the canvas/gallery aesthetic to an operator Obsidian sign-off (operator gates — Standing Rule). On the reference node this overlay is normally performed by `skill_node_bootstrap_interview.md` Step 9; this step exists so a node-class fork can produce the exemplar shape in one pass. Point the operator at the fork's `ONBOARDING.md` as their first read.

### Step 5: Offer Immediate Onboarding

Ask the user:
> "Your project is ready at `<path>`. Would you like to run the onboarding interview now to customize it for your domain? Or you can open it later — the setup will trigger automatically on first run."

**If now:**
- Instruct the user to open a new Claude Code session in the project directory: `cd <project_path>` then run `claude`
- Carry forward any answers from Step 1 so the user doesn't repeat themselves
- Note: the onboarding will trigger automatically from the project's own CLAUDE.md first-run detection

**If later:**
- Report the path and explain that onboarding triggers automatically on first `claude` invocation inside the project directory
- Suggest: "To start working in your project, run `cd <project_path> && claude`"

### Step 6: Report

Confirm to the user:
- **Created**: `<workspace_root>/<project_name>/`
- **Structure**: Full aDNA triad (who/what/how) + templates + skills + context library
- **Git**: Initialized with fresh repository (no history from template)
- **Next**: Open the project directory to begin onboarding

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Project directory | Directory | Full aDNA structure at `<workspace_root>/<project_name>/` |
| Prepared MANIFEST.md | File | `role: template` removed, `agent_init` marker set |
| Prepared STATE.md | File | `agent_init` marker set |
| Prepared CLAUDE.md | File | `agent_init` marker set |
| Fresh git repo | Git | `git init` with no history |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Directory already exists | Name collision | Warn user, ask for different name |
| Workspace not writable | Permissions issue | Suggest creating the directory manually or choosing a different location |
| Copy fails | Disk space or permissions | Report the error with the specific path that failed |
| .adna/ doesn't have `role: template` | Not the canonical template | Warn the user — the base template may be corrupted. Suggest `git pull` |

## Related

- [[how/skills/skill_onboarding|skill_onboarding.md]] — Runs after fork to customize the new project
- [[what/docs/projects_folder_pattern|projects_folder_pattern.md]] — Workspace architecture documentation
