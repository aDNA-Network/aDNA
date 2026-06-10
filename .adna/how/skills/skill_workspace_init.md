---
type: skill
skill_type: agent
created: 2026-03-22
updated: 2026-05-11
status: retired  # formally retired in aDNA v7.0 (campaign_adna_v2_infrastructure M03 close 2026-05-11; was status: deprecated since v6.0 2026-04-03)
category: onboarding
trigger: "RETIRED — see Replacement section below"
last_edited_by: agent_stanley
deprecation_note: "Replaced by the pre-authored root CLAUDE.md (2026-04-03 restructure). The root CLAUDE.md handles project creation and discovery directly — no workspace init step needed."
retirement_note: "Formally retired in aDNA v7.0 (M03 close 2026-05-11) per campaign_adna_v2_infrastructure mission tree. The workspace-init flow is now covered by manual onboarding via `how/templates/template_workspace_claude.md` + `skill_workspace_upgrade.md` for workspaces with existing content. Retained for archival reference per Standing Order #6 (archive, never delete) — see file body below."
retirement_aar: "campaign_adna_v2_infrastructure/missions/artifacts/aar_m03_repo_flatten.md (landed Session 3)"
replacement:
  - "how/templates/template_workspace_claude.md (fresh workspaces — bootstrap workspace router from template)"
  - "how/skills/skill_workspace_upgrade.md (existing-content workspaces — bring up to v7.0 compliance)"
tags: [skill, workspace, bootstrap, onboarding, multi-project, lattice, retired_v7]

requirements:
  tools: []
  context: ["CLAUDE.md", "what/docs/templates/workspace_claude_md.template"]
  permissions: ["write files in parent directory", "copy directories"]
---

# Skill: Workspace Bootstrap — RETIRED in aDNA v7.0

> **⚠️ RETIRED.** This skill was deprecated in v6.0 and formally retired in v7.0
> (campaign_adna_v2_infrastructure M03 close 2026-05-11). It is retained for archival
> reference per Standing Order #6 (archive, never delete). DO NOT invoke this skill
> for new work — see §Replacement below.
>
> The v7.0 workspace-init flow is content-only (no procedural skill needed):
>
> 1. **Fresh workspace bootstrap**: `cp .adna/how/templates/template_workspace_claude.md ~/aDNA/CLAUDE.md` (per [ADR-007](../../what/decisions/adr_007_outer_adna_claude_md_disposition.md))
> 2. **Existing-content workspace upgrade**: run `skill_workspace_upgrade.md` (per M03 Obj 4 Commit 4.2 update; symlink-step removed; Step 3 alternative added)

## Replacement

- `how/templates/template_workspace_claude.md` — fresh workspaces; directly installable as the workspace router
- `how/skills/skill_workspace_upgrade.md` — existing-content workspaces; brings them up to v7.0 compliance with optional template-bootstrap as Step 3 alternative

The pre-authored root `CLAUDE.md` no longer exists post-flatten (the outer wrapper
was converted to `template_workspace_claude.md` per ADR-007 M03 B1). The template
is now the canonical starting point.

---

## Overview (archival — original v6.0 deprecation note)

Creates a workspace-level CLAUDE.md at the parent directory of this aDNA vault. The workspace CLAUDE.md teaches future agents how to discover projects, create new ones by forking the aDNA template, and upgrade the workspace to L1 compute.

This skill is triggered automatically when the aDNA CLAUDE.md detects that the parent directory has no CLAUDE.md. It runs once per workspace — subsequent sessions skip it silently.

## Trigger

Automatic — aDNA CLAUDE.md workspace bootstrap detection triggers this skill when:
1. First-run detection has resolved (onboarding complete or skipped)
2. The parent directory of this vault exists and is not `$HOME`
3. The parent directory does not contain a CLAUDE.md

If all three are true, load this skill and begin at Step 1.

## Parameters

None. This skill is guided through conversation with the user.

## Requirements

### Tools/APIs
- File read/write access to the parent directory
- File copy (for optional project fork in Step 4)

### Context Files
- `what/docs/templates/workspace_claude_md.template` — workspace CLAUDE.md template

### Permissions
- Write CLAUDE.md to the parent directory
- Optionally copy this aDNA vault to a new directory for project forking

## Implementation

### Step 1: Explain and Confirm

Inform the user:

> "Your `~/aDNA/` workspace doesn't have a workspace-level CLAUDE.md yet. I can create one at `<parent_path>/CLAUDE.md` — it will help future agents discover your projects, create new ones from this template, and manage L0→L1 upgrades. Shall I set it up?"

If the user declines, note the skip and proceed with normal session flow. Do not ask again in future sessions (the parent directory still won't have a CLAUDE.md, but the user has declined — record this in `who/coordination/` as a skip note so other agents don't re-trigger).

### Step 2: Detect Workspace State

Scan the parent directory:

1. **Existing projects** — list all subdirectories that contain a `CLAUDE.md` or `MANIFEST.md` file. These are aDNA projects already present in the workspace.
2. **Infrastructure repos** — check if `latlab/` exists (indicates L1). Check if `lattice-protocol/` exists.
3. **Compute tier** — if `latlab/` is present AND a JupyterHub process is running (check port 8000), tier is `L1`. Otherwise `L0`.
4. **aDNA folder name** — the basename of this vault's directory (e.g., `adna` if cloned to `~/aDNA/adna/`).

Report findings to the user:
- "Found X existing project(s): ..."
- "Compute tier: L0 (no latlab detected)" or "Compute tier: L1 (latlab present)"

### Step 3: Create Workspace CLAUDE.md

Read the template from `what/docs/templates/workspace_claude_md.template`.

Resolve variables:
| Variable | Source |
|----------|--------|
| `{{created_date}}` | Today's date (YYYY-MM-DD) |
| `{{compute_tier}}` | From Step 2 detection (L0 or L1) |
| `{{adna_folder}}` | Basename of this vault's directory |

Write the resolved template to `<parent_directory>/CLAUDE.md`.

Confirm to the user: "Created workspace CLAUDE.md at `<path>`."

### Step 4: Offer Project Creation (Optional)

Ask the user: "Would you like to create your first project from this template now?"

If yes, load and execute `how/skills/skill_project_fork.md`. Pass the workspace root and aDNA folder name as parameters. The fork skill handles:
- Collecting project name and description
- Copying the template and stripping `.git/` and `.obsidian/`
- Removing `role: template` from the forked MANIFEST.md
- Setting up first-run markers so onboarding triggers in the new project
- Offering to run onboarding immediately or defer

If the user declines project creation, skip to Step 5.

### Step 5: Summary and Next Steps

Report to the user:

- **Created**: Workspace CLAUDE.md at `<parent_path>/CLAUDE.md`
- **Projects found**: List any existing projects discovered in Step 2
- **New project**: Name and path (if created in Step 4)
- **Compute tier**: L0 or L1

Suggest next steps:
- "To create a new project later, open Claude Code from `<parent_path>/` and say 'create a new project'."
- "To upgrade to L1 compute, read `<adna_folder>/how/skills/skill_l1_upgrade.md`."
- "To work inside a project, open that project's directory directly."

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Workspace CLAUDE.md | File | Created at parent directory |
| Forked project (optional) | Directory | New aDNA project ready for onboarding |

## Error Handling

- **Parent directory not writable**: Warn the user and suggest creating the CLAUDE.md manually. Do not fail the session.
- **Template file missing**: Log error, suggest the user pull latest aDNA updates (`git pull` inside the adna directory).
- **aDNA folder name contains spaces**: Use the folder name as-is in the template but warn that spaces may cause issues with some tools.

## Related

- [[how/skills/skill_project_fork|skill_project_fork.md]] — Fork template into a new project (called from Step 4)
- [[how/skills/skill_onboarding|skill_onboarding.md]] — 5-question interview for customizing new projects
- [[how/skills/skill_l1_upgrade|skill_l1_upgrade.md]] — Phased L0→L1 compute upgrade
- [[what/docs/projects_folder_pattern|projects_folder_pattern.md]] — Multi-project workspace design doc
