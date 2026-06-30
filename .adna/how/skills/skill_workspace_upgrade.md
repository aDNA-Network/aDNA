---
type: skill
skill_type: agent
created: 2026-04-04
updated: 2026-04-04
status: active
category: operations
trigger: "Workspace needs aDNA standard compliance upgrade, or existing workspace has accumulated stale files and lacks project discovery"
last_edited_by: agent_init
tags: [skill, workspace, upgrade, adna, migration, compliance]

requirements:
  tools: []
  context: ["CLAUDE.md (workspace root)", ".adna/CLAUDE.md"]
  permissions: ["read all directories at workspace root", "write workspace CLAUDE.md", "create _archive/ directory", "move files"]
---

# Skill: Workspace Upgrade

## Overview

Upgrades a workspace to aDNA standard compliance. Covers: project discovery, root governance, stale file cleanup, and project compliance verification. Produces an upgraded workspace CLAUDE.md that routes agents to the correct project based on context.

This skill complements `skill_project_fork.md` (creates new projects) — this skill upgrades the workspace that hosts them.

## Trigger

- Workspace has no project discovery in its CLAUDE.md
- Existing projects lack governance files (MANIFEST.md, STATE.md)
- Root directory has accumulated stale files
- User explicitly requests workspace upgrade

## Parameters

| Parameter | Source | Required |
|-----------|--------|----------|
| `workspace_root` | The directory containing your aDNA projects (e.g., `~/aDNA/`) | Yes |
| `cleanup_mode` | `aggressive` (archive everything stale) or `conservative` (only clear stubs) | No (default: `aggressive`) |

## Implementation

### Step 1: Workspace Audit

Scan the workspace root and classify every directory and file:

```
Categories:
- aDNA project     — has CLAUDE.md + who/what/how triad (or MANIFEST.md with role != template)
- Code repo        — has .git/ but no triad structure
- External dep     — third-party code, tools, or libraries
- Working dir      — site-specific working directories (not aDNA projects, but used by the workspace)
- Base template    — adna/ with .adna/ inside (role: template)
- Domain-specific  — has CLAUDE.md but non-standard structure (datarooms, whitepapers, etc.)
- Stale/archive    — MOVED.md stubs, empty reports, orphaned files
- Loose files      — .md/.pdf/.zip at root level not belonging to any project
```

For each directory, record:
- Name, classification, has `.git/`, has `CLAUDE.md`, has `MANIFEST.md`, has triad

Report the audit to the user as a table. Ask for confirmation before proceeding.

### Step 2: Root Cleanup

**Create `_archive/` at workspace root** (if it doesn't exist).

Move stale/archive items and loose files into `_archive/`:
- Empty compliance reports
- MOVED.md stub directories
- Legacy prompt/mission files at root
- Stray documents (.pdf, .zip, .pptx)

**Do NOT move:**
- Active projects (any classification except stale/archive and loose files)
- Working directories
- The base template (adna/)
- CLAUDE.md (we're upgrading it, not archiving it)

Report what was moved. This is reversible — everything is in `_archive/`.

### Step 3: Upgrade Workspace CLAUDE.md

**Back up the existing CLAUDE.md first**: `cp CLAUDE.md _archive/workspace_claude_md_pre_upgrade.md`

Replace the workspace CLAUDE.md with an upgraded version that includes:

1. **Header** — workspace identity (no persona, functional router)
2. **Project Discovery** — two mechanisms:
   - Glob `*.aDNA/` directories for standard projects
   - Named legacy projects (grandfathered, listed explicitly in a table)
3. **Routing Logic**:
   - If user has a specific task → identify the right project, read its CLAUDE.md
   - If cold start → list all projects with brief descriptions
   - If creating new project → invoke `.adna/how/skills/skill_project_fork.md`
4. **Workspace Layout** — updated to reflect post-cleanup state
5. **aDNA Paradigm** — preserved (module/dataset/lattice primitives)
6. **Infrastructure** — preserve any compute tier descriptions or environment context from the existing CLAUDE.md
7. **Standing Rules**:
   - Never modify `.adna/` (base template, updated via `git pull`)
   - Inside a project, that project's CLAUDE.md is authoritative
   - Workspace CLAUDE.md governs routing and discovery only

**Template accessibility (post-v7.0 — direct clone, NO symlink):**

Post-aDNA-v7.0 (campaign_adna_v2_infrastructure M03 flatten 2026-05-11): the `.adna/`
directory IS the git clone of the template repo (no longer a symlink to a nested
`adna/.adna/`). Standard flow for fresh workspace bootstrap:

```bash
cd <workspace_root>           # typically ~/aDNA
git clone https://github.com/aDNA-Network/aDNA.git .adna
```

If a workspace router (`<workspace_root>/CLAUDE.md`) doesn't yet exist, install it from
the template (Step 3 alternative — template-based bootstrap per [ADR-007](../../what/decisions/adr_007_outer_adna_claude_md_disposition.md)):

```bash
cp .adna/how/templates/template_workspace_claude.md CLAUDE.md
```

Then customize the workspace router (Project Discovery + Workspace Layout sections)
to your installed projects.

**Verify**: `.adna/MANIFEST.md` exists and contains `role: template`. If this check
fails, the clone is broken — re-clone or check git remote.

**For pre-v7.0 workspaces (still have the legacy `~/lattice/.adna -> adna/.adna`
symlink + outer `adna/CLAUDE.md` wrapper)**: see `m01_obj2_migration_runbook.md` §2
Path A (in-place rename) or Path B (clean re-clone) for migration to the flat post-v7.0
layout. The `upgrade_v6_to_v7.md` guide (M08a finalized; post-M08b at
`.adna/how/docs/upgrade_v6_to_v7.md`) is the canonical operator-facing reference.

**Naming convention (per [ADR-009](../../what/decisions/adr_009_aDNA_naming_convention.md)):**

The canonical aDNA naming convention is `<name>.aDNA/` directory ↔ `<name>.aDNA.git` GitHub repo where `<name>` is snake_case (`[a-z][a-z0-9_]*`). New projects forked via `skill_project_fork.md` enforce this via the warn-on-non-conformant step (per ADR-009 §4 enforcement).

**4 grandfathered exception classes** (per ADR-009 §3 — operator-discretionary, NOT forced):

1. **Hyphen-flat GitHub repos** (4 vaults: `science-stanley-adna`, `wga-adna`, `context-commons-adna`, `LAStartupLattice`) — pre-`.aDNA/` convention vaults; renaming is operator-discretionary and tracked under v3 successor `campaign_adna_v3_ecosystem_compliance` M04-EC
2. **No-remote vaults** (7 vaults: `Spacemacs.aDNA`, `VideoForge.aDNA`, `III.aDNA`, etc.) — adopt the convention if/when a GitHub remote is configured via `skill_git_remote_setup.md` (M05; new)
3. **Path-style local remote** (1 vault: `LPWhitepaper.aDNA`) — permitted under ADR-009 §1's "Path-style remotes" clause for whitepaper-vault tooling pattern
4. **Template-repo exception** (`aDNA-Network/aDNA.git` — this template; mixed-case canonical per ADR-006 amendment 2026-05-18) — bare short name; recursive `.aDNA.aDNA` form avoided

**Naming decisions for existing projects:**
- Do NOT rename existing projects to add `.aDNA` suffix unless you've assessed the blast radius (per ADR-009 §5 application scope: existing vaults are operator-discretionary)
- Absolute paths in agent configs, Obsidian settings, cross-repo references, and CI can all break
- Future projects use `.aDNA` suffix via `.adna/how/skills/skill_project_fork.md` (which enforces snake_case per ADR-009 §1)
- Workspace CLAUDE.md lists legacy projects explicitly alongside `*.aDNA/` glob

### Step 4: Project Compliance Check

For each project classified as "aDNA project" in Step 1, verify:

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| CLAUDE.md | Yes | Flag — project is unnavigable by agents |
| MANIFEST.md | Recommended | Note — project lacks identity metadata |
| who/what/how triad | Recommended | Note — project lacks standard structure |
| STATE.md | Optional | Note — useful for operational projects |

Report findings. Do NOT modify projects in this step — each project's governance is its own concern.

### Step 5: Validation

1. **Discovery test**: From workspace root, verify the CLAUDE.md correctly lists all projects
2. **Routing test**: Simulate a cold start — does the agent know where to send the user?
3. **Template accessible**: Verify `.adna/MANIFEST.md` exists at workspace root (symlink works)
4. **No broken refs**: Verify workspace CLAUDE.md doesn't reference moved/deleted paths
5. **Backup accessible**: Verify `_archive/` contains the pre-upgrade CLAUDE.md

Report results.

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Audit report | Table | Classification of all workspace contents |
| Upgraded CLAUDE.md | File | Workspace root governance with project discovery |
| Cleanup log | List | Files moved to `_archive/` |
| Compliance report | Table | Per-project governance file check |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| No `.adna/` directory | Template not cloned | Run `git clone <adna-repo> adna/` first |
| CLAUDE.md not writable | Permissions | Check filesystem permissions |
| Project has no CLAUDE.md | Ungoverned project | Flag for user — may need manual CLAUDE.md creation |
| `.adna/` missing post-clone | Clone failed or wrong path | Re-clone: `cd ~/aDNA && rm -rf .adna && git clone https://github.com/aDNA-Network/aDNA.git .adna` |
| Workspace router missing | Pre-bootstrap state | Install from template: `cp .adna/how/templates/template_workspace_claude.md ~/aDNA/CLAUDE.md` |

## Rollback

All changes are reversible:
- Original CLAUDE.md is in `_archive/workspace_claude_md_pre_upgrade.md`
- Archived files are in `_archive/` with original names
- No projects were modified (compliance check is read-only)

To rollback: `cp _archive/workspace_claude_md_pre_upgrade.md CLAUDE.md`

## Related

- `how/skills/skill_project_fork.md` — Creates new aDNA projects in the workspace
- `.adna/CLAUDE.md` — Template's workspace governance (reference for discovery pattern)
- `how/skills/skill_version_migration.md` — Upgrades individual project CLAUDE.md versions
