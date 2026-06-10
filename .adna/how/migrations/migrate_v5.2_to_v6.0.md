---
type: migration
source_version: "5.2"
target_version: "6.0"
scope: mixed
risk_level: medium
affected_files:
  - CLAUDE.md
  - STATE.md
  - MANIFEST.md
created: 2026-04-06
updated: 2026-04-06
status: active
last_edited_by: agent_stanley
tags: [migration]
---

# Migration: v5.2 → v6.0

> **Workspace-root note (2026-06)**: this migration predates the `~/aDNA/` workspace-root default — any historical `~/lattice` paths are intentionally unchanged. New installs default to `~/aDNA/`; legacy roots migrate via `how/skills/skill_workspace_path_migration.md` (agentic) or `how/skills/migrate_workspace_root.sh` (shell).

## Summary

**What changed**: Consolidated upgrade covering v5.3 through v6.0 — 5 minor releases. Major changes: identity rename (adna → Agentic-DNA), Standing Orders and Git Coordination sections added, mandatory AAR enforcement, upstream contribution and side-quest awareness, `.aDNA` directory convention, project fork skill, VISION.md, community quest system, template count corrections (17→22), skill inventory expanded (7→13).

**Why**: This catches up vaults that were last migrated at v5.2. Each intermediate version (v5.3–v5.7) added features incrementally. v6.0 is a major release with the identity rename and significant governance additions. A consolidated migration is provided because the intermediate changes are primarily additive (new files and sections) rather than destructive.

**Impact**: After migrating, the vault will have all v6.0 governance features — standing orders, git coordination protocol, AAR enforcement, upstream contribution awareness, side-quest framework, and the updated skill inventory. New template files and skills are already present in the base template (pulled via git); this migration updates the forked project's governance files to reference them correctly.

## Pre-Flight Checks

1. **Version verification**: Read `CLAUDE.md` frontmatter. Confirm `version: "5.2"`. If the version is already `"5.3"` or higher, STOP — check the migration registry for the correct starting migration. If version is below `"5.2"`, apply earlier migrations first (`migrate_v5.0_to_v5.1.md`, `migrate_v5.1_to_v5.2.md`).
2. **Clean working state**: Run `git status`. If there are uncommitted changes, ask the user to commit or stash first.
3. **Pull latest template**: Ensure `adna/` (or `.adna/` symlink target) is up to date: `cd ~/lattice/adna && git pull`. The migration references files that must exist in the v6.0 template.
4. **Read affected files**: Read `CLAUDE.md`, `STATE.md`, and `MANIFEST.md`. Confirm they exist and have valid YAML frontmatter.
5. **Create safety snapshot**: Run `git tag pre-migration-v5.2`. If the tag already exists, STOP — a prior migration attempt may have failed.
6. **Verify no concurrent sessions**: Check `how/sessions/active/` for other active sessions modifying governance files.

## Changes

### File: CLAUDE.md

| # | Change Type | Description |
|---|------------|-------------|
| 1 | **Version bump** | `version: "5.2"` → `version: "6.0"` in frontmatter |
| 2 | **Title rename** | `# CLAUDE.md — adna` → `# CLAUDE.md — Agentic-DNA` |
| 3 | **Version comments** | Update `<!-- v5.2 ...` to `<!-- v6.0 | 2026-04-03 -->` (top and bottom) |
| 4 | **Add Standing Orders section** | New section after Safety Rules |
| 5 | **Add Git Coordination section** | New section after Standing Orders |
| 6 | **Add Upstream Contribution Awareness** | New subsection under Working with Content |
| 7 | **Add Side-Quest Awareness** | New subsection under Working with Content |
| 8 | **Update skill inventory** | Expand from 7 to 13 skills |
| 9 | **Update template count** | `17 templates` → `22 templates` in Project Map |
| 10 | **Update project tree** | Add `quests/` under `how/`, add `.aDNA` suffix to root directory |

### File: STATE.md

| # | Change Type | Description |
|---|------------|-------------|
| 1 | **Version reference** | Update any `aDNA v5.2` references to `aDNA v6.0` |
| 2 | **What's Working** | Add entries for: CHANGELOG, VISION.md, community quests, project fork skill |

### File: MANIFEST.md

| # | Change Type | Description |
|---|------------|-------------|
| 1 | **Template count** | `17` → `22` wherever template counts appear |
| 2 | **Architecture tree** | Add `community/` and `quests/` directories if not present |

## Migration Steps

### Step 1: Update CLAUDE.md Version and Identity

1. Open `CLAUDE.md`
2. **Frontmatter**: Find `version: "5.2"` → replace with `version: "6.0"`
3. **Title**: Find `# CLAUDE.md — adna` (or similar) → replace with `# CLAUDE.md — Agentic-DNA`
4. **Top version comment**: Find `<!-- v5.2` line near top → replace with `<!-- v6.0 | 2026-04-03 -->`
5. **Bottom version comment**: Find `<!-- v5.2` line near bottom → replace with `<!-- v6.0 | 2026-04-03 -->`
6. **Verify**: Read CLAUDE.md frontmatter. Confirm `version: "6.0"`.

### Step 2: Add Standing Orders Section

Insert the following after the **Safety Rules** section (before Agent Protocol), if not already present:

```markdown
## Standing Orders

These rules apply to every session, mission, and campaign.

1. **Phase gates are human gates.** Never auto-advance between campaign phases without explicit user approval.
2. **Destructive actions require confirmation.** Deleting files, overwriting shared configs, or abandoning missions — ask first.
3. **Context budget is doctrine.** Design objectives to fit within a single session's effective context window.
4. **Local context over global context.** Read the AGENTS.md in the directory you're working in before loading broader context. The local file is authoritative for that space.
5. **Every mission gets an AAR.** Before setting any mission to `status: completed`, append a 5-line AAR (Worked/Didn't/Finding/Change/Follow-up). Template: `how/templates/template_aar_lightweight.md`. No exceptions.
6. **Archive, never delete.** Campaign docs, mission files, session records — permanent audit trail. Set `status: abandoned` or `status: completed`, never remove.
```

### Step 3: Add Git Coordination Section

Insert immediately after Standing Orders:

```markdown
## Git Coordination

Git is the coordination bus for multi-user and multi-agent projects.

- **Pull at session start.** Run `git pull` before modifying any files. Check for merge conflicts.
- **Commit after significant edits.** Do not rely on auto-commit timing. After modifying governance files, mission status, or campaign docs — commit immediately.
- **Push after committing.** Run `git push` after each explicit commit. This closes the revert window.
- **Check git log for context.** Before starting work, run `git log --oneline -10` to see recent activity from other agents or users.
- **Truth hierarchy**: git HEAD > cached file read > memory > assumption. If your memory says a mission is "in_progress" but git shows it "completed", trust git.
```

### Step 4: Add Upstream Contribution and Side-Quest Awareness

In the **Working with Content** section, add these two subsections before the closing `---`:

```markdown
### Upstream Contribution Awareness

While working in any aDNA vault, stay alert for **framework-level** improvement opportunities — missing template fields, undocumented patterns, naming inconsistencies, or gaps you had to work around. These are improvements that would help *all* aDNA users, not just the current project.

When you notice one, mention it to the user at a **natural pause point** (end of task, SITREP). If approved, create a backlog idea file with the `idea_upstream_` prefix. Full protocol: `how/skills/skill_upstream_contribution.md`.

**Do not** interrupt active work, file without user approval, or suggest project-specific tweaks as upstream improvements.

### Side-Quest Awareness

The `how/quests/` directory contains structured validation experiments ("side-quests") that community members can run with spare agent tokens. At natural session-end points, if the user has spare context budget, you may briefly mention available quests. Never interrupt active work for this. See `what/docs/side_quest_guide.md` for the full participation guide and `how/quests/AGENTS.md` for directory structure.
```

### Step 5: Update Skill Inventory

Find the skill inventory table in the Agent Protocol section and replace with the current v6.0 inventory (13 skills):

```markdown
| Skill | Type | Trigger |
|-------|------|---------|
| `skill_onboarding` | agent | First-run detection in forked project (uncustomized, no `role: template`) |
| `skill_project_fork` | agent | User wants to create a new project (called from root CLAUDE.md) |
| `skill_workspace_init` | agent | *Deprecated* — root CLAUDE.md now ships pre-authored |
| `skill_l1_upgrade` | agent | User asks about L1/compute/JupyterHub |
| `skill_lattice_publish` | agent | User wants to publish a lattice to registry |
| `skill_new_entity_type` | agent | User wants to extend the ontology |
| `skill_context_quality_audit` | agent | Audit request for context files |
| `skill_context_graduation` | process | Context promotion to higher quality tier |
| `skill_vault_review` | agent | Governance audit of vault structure |
| `skill_upstream_contribution` | process | Agent notices framework-level gap |
| `skill_version_migration` | process | CLAUDE.md version upgrade |
| `skill_sqlite_persistence` | process | Multiple agents, sessions hard to query, learnings accumulating without validation signal |
| `skill_orchestration_tiers` | process | Multi-file tasks, tier classification, agent spawning, model routing decisions |
```

### Step 6: Update Template Count and Project Tree

1. **Template count**: Find references to `17 templates` or `17 reusable templates` → replace with `22 templates` / `22 reusable templates`
2. **Project tree**: If the `how/` section of the tree does not include `quests/`, add:
   ```
   │   ├── quests/                  # Community validation experiments (side-quests)
   ```
3. **Root directory name**: Optionally update the root of the project tree from `project_name/` to `project_name.aDNA/` (the `.aDNA` suffix is the v6.0 convention for new projects, but existing projects keep their names)

### Step 7: Update STATE.md

1. Find `aDNA v5.2` → replace with `aDNA v6.0`
2. In "What's Working" or equivalent status list, add:
   - `- CHANGELOG.md with version policy and migration cross-links`
   - `- VISION.md ecosystem roadmap`
   - `- Community quest system (how/quests/)`
   - `- Project fork skill (skill_project_fork.md)`
   - `- 22 templates (was 17)`
   - `- 13 skills (was 7)`

### Step 8: Update MANIFEST.md

1. Find template count references (`17`) → replace with `22`
2. Add `community/` to architecture tree if not present
3. Update `updated` and `last_edited_by` in frontmatter

## Post-Flight Validation

- [ ] `CLAUDE.md` frontmatter: `version: "6.0"`
- [ ] `CLAUDE.md` title: contains `Agentic-DNA` (not just `adna`)
- [ ] `CLAUDE.md` top version comment: `<!-- v6.0 | 2026-04-03 -->`
- [ ] `CLAUDE.md` bottom version comment: `<!-- v6.0 | 2026-04-03 -->`
- [ ] `CLAUDE.md` has Standing Orders section (6 rules)
- [ ] `CLAUDE.md` has Git Coordination section (5 bullets + truth hierarchy)
- [ ] `CLAUDE.md` has Upstream Contribution Awareness subsection
- [ ] `CLAUDE.md` has Side-Quest Awareness subsection
- [ ] `CLAUDE.md` skill inventory lists 13 skills
- [ ] `CLAUDE.md` template count shows 22
- [ ] `STATE.md` references `aDNA v6.0`
- [ ] `MANIFEST.md` template count updated

**Structural checks**:
- [ ] All affected files have valid YAML frontmatter
- [ ] New wikilinks resolve to existing files
- [ ] `CLAUDE.md` frontmatter `version` matches `"6.0"`

All checks passing = migration complete. Commit:
```
git add CLAUDE.md STATE.md MANIFEST.md && git commit -m "chore: migrate aDNA vault from v5.2 to v6.0"
git tag migration-v5.2-to-v6.0
```

## New Files to Copy (Optional)

These files were added between v5.2 and v6.0. If they are missing from your vault, copy from the `.adna/` template:

| File | Added In | Purpose |
|------|----------|---------|
| `who/governance/VISION.md` | v5.5 | Ecosystem vision document |
| `how/templates/template_side_quest.md` | v5.4 | Quest specification template |
| `how/templates/template_quest_result.md` | v5.4 | Result submission template |
| `how/templates/template_aar_lightweight.md` | v6.0 | 5-line AAR format |
| `how/templates/template_campaign_mission.md` | v6.0 | Campaign-linked mission template |
| `how/quests/AGENTS.md` | v5.4 | Quest directory index |
| `how/skills/skill_upstream_contribution.md` | v5.3 | Upstream contribution protocol |
| `how/skills/skill_project_fork.md` | v5.7 | Project fork skill |
| `what/docs/side_quest_guide.md` | v5.4 | Side-quest participation guide |

Copy only what you need. Not all files are required for basic vault operation.

## Rollback

**Option 1 — Tag-based full rollback** (recommended):
```
git reset --hard pre-migration-v5.2
git tag -d migration-v5.2-to-v6.0
```

**Option 2 — Per-file rollback** (surgical):

Reverse each change from the Changes and Migration Steps sections. Key reversals:
- `version: "6.0"` → `"5.2"`, `Agentic-DNA` → `adna`
- Remove Standing Orders, Git Coordination, Upstream Contribution Awareness, Side-Quest Awareness sections
- Restore original skill inventory (7 entries) and template count (17)

**Option 3 — Commit revert**:
```
git revert HEAD
```

## Related

- [CHANGELOG](../../CHANGELOG.md) — Full version history v5.2 through v6.0
- [Migration Registry](AGENTS.md) — All available migrations
- [Version Migration Skill](../skills/skill_version_migration.md) — Guided upgrade workflow
- [Migration Safety Framework](../../what/docs/migration_safety_framework.md) — Recovery ladder
