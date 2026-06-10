---
campaign_id: campaign_adna_workspace_upgrade
type: campaign
campaign_class: governance-tight
title: "aDNA Workspace Upgrade — Standard Compliance + Reusable Upgrade Skill"
owner: <project_owner>
co_executors: []
status: completed
phase_count: 2
mission_count: 5
estimated_sessions: "~4.0"
estimation_class: governance-tight
priority: high
created: 2026-04-04
updated: 2026-04-04
completed: 2026-04-04
last_edited_by: agent_init
tags: [campaign, adna, workspace, upgrade, migration, skill]
---

# Campaign: aDNA Workspace Upgrade

## Goal

Upgrade our `~/lattice/` workspace to full aDNA v6.0 standard compliance, and in the process, create a reusable upgrade skill that any aDNA user can run to bring their workspace into compliance. The procedure we follow BECOMES the documented skill.

## Context

campaign_adna_polish restructured the aDNA base template (324 files → `.adna/`, root CLAUDE.md + README, visual assets, 20 III cycles). But our own `~/lattice/` workspace doesn't yet comply with the standard it defines:

- `lattice-labs/` should be `lattice_labs.aDNA/` (naming convention)
- No MANIFEST.md or STATE.md at project root (governance files)
- Workspace CLAUDE.md exists but lacks project discovery/routing
- No `.aDNA` suffix on project directories

**Strategic value**: If we can't upgrade our own workspace cleanly, the standard isn't ready for others. Dogfooding the upgrade process validates the standard and produces a battle-tested skill.

**Predecessor**: campaign_adna_polish (completed 2026-04-04)

## Scope

### In Scope
- Create `skill_workspace_upgrade.md` — reusable upgrade prompt
- Create `migrate_v6.0_workspace.md` — migration guide
- Rename `lattice-labs/` → `lattice_labs.aDNA/`
- Add MANIFEST.md + STATE.md governance files
- Enhance workspace CLAUDE.md with project discovery
- Update all cross-repo references
- Commit upgrade skill to aDNA base template

### Out of Scope
- Upgrading other users' workspaces (they'll use the skill themselves)
- Visual polish backlog items (demo GIF, plugins, logo — separate backlog)
- aDNA standard specification changes

### Co-Execution

Co-executor validates:
- Obsidian Git sync works after rename (auto-pull doesn't break)
- Obsidian graph view renders correctly post-rename
- No broken wikilinks in Obsidian after structural changes

## Phases & Missions

### Phase 1: Upgrade Infrastructure

| # | Mission | Title | Sessions | Status |
|---|---------|-------|----------|--------|
| M00 | [[missions/mission_adna_ws_upgrade_m00\|M00]] | Audit & Plan | 0.5 | **complete** |
| M01 | [[missions/mission_adna_ws_upgrade_m01\|M01]] | Create skill_workspace_upgrade.md + drafts | 1.0 | **complete** |
| M02 | [[missions/mission_adna_ws_upgrade_m02\|M02]] | Create migrate_v6.0_workspace.md | 0.5 | **complete** (merged into M01) |

**Phase 1 gate**: Upgrade skill in vault `how/skills/`. Migration guide + workspace CLAUDE.md draft in campaign artifacts. **PASSED.**

### Phase 2: Execute & Validate

| # | Mission | Title | Sessions | Status |
|---|---------|-------|----------|--------|
| M03 | [[missions/mission_adna_ws_upgrade_m03\|M03]] | Execute upgrade on ~/lattice/ | 1.5 | **complete** |
| M04 | [[missions/mission_adna_ws_upgrade_m04\|M04]] | Validate + commit skill to aDNA | 0.5 | **complete** |

**M03 actual**: Executed in same session as M01. Symlink `.adna/` at workspace root, archived 12 stale items, applied upgraded CLAUDE.md, validated all 11 projects + 6 working dirs. v6.0 cross-system review identified 3 schema gaps (backlog).

**M04 actual**: Generalized skill for public template (removed Lattice-specific refs, strengthened symlink step per AAR). Committed to `.adna/how/skills/`, updated AGENTS.md index + CLAUDE.md count (13→14). Campaign closed.

**Phase 2 gate (DG-FINAL): PASSED.** Workspace CLAUDE.md discovers projects (glob + named). `.adna/` accessible via symlink. Upgrade skill refined, committed to aDNA base template. Rename evaluation mission created for future GO/NO-GO.

## Decision Points

| # | When | Decision | Status |
|---|------|----------|--------|
| D1 | M00 | Full rename vs symlink bridge — impact on git history, CI, cross-repo refs | **RESOLVED: No rename.** Blast radius unacceptable (40+ refs, 30+ memory files, 3 machines' Obsidian configs). All existing projects grandfathered. Future projects use `.aDNA` suffix. |
| D2 | M00 | Workspace CLAUDE.md persona | **RESOLVED: No persona.** Functional router only. Berthier activates inside projects. |
| D3 | M00 | Workspace CLAUDE.md version control | **RESOLVED: Track in adna repo.** Users get workspace governance via `git pull`. |
| D4 | M00 | Root cleanup scope | **RESOLVED: Aggressive.** Archive everything not an active project or working directory. |
| D5 | M03 | Obsidian sync validation — schedule co-executor test window | pending |

## Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| Workspace CLAUDE.md merge loses JupyterLab context | Medium | Draft in artifacts first, diff against current, user review before apply |
| No git safety net for workspace root changes | Medium | Manual backup to `_archive/` before modification |
| Workspace CLAUDE.md sync across machines | Medium | Tracked in adna repo — users get updates via `git pull` |
| Upgrade skill too complex for external users | Medium | Test with fresh clone, simplify during M04 |
| Cleanup accidentally removes active content | Medium | Archive, never delete. User reviews cleanup list. |

## Campaign AAR (M00-M03, session 1)

- **Worked**: Symlink approach (`ln -s adna/.adna .adna`) cleanly bridges aDNA template accessibility without moving files. Aggressive root cleanup (12 items archived) immediately improved workspace legibility. Merging project discovery + JupyterLab context into one CLAUDE.md works well — agents can route without loading vault governance.
- **Didn't**: Initial plan missed the `.adna/` symlink gap — user caught it. Should have identified this in M00 audit. The D3 decision ("track in adna repo") is partially unresolved — the site-specific CLAUDE.md can't truly live in adna repo since it has local project table.
- **Finding**: Two-convention workspace (legacy names + future `.aDNA` suffix) is functional but creates documentation overhead. The named-projects table in workspace CLAUDE.md will need manual maintenance. v6.0 schema triple alignment claim is not yet true in lattice-labs (lattice_yaml_schema.json missing 2 types + `status` field).
- **Change**: Future workspace upgrades should always check for template accessibility at root — add explicit "symlink or copy .adna/ to workspace root" step to the skill.
- **Follow-up**: (1) ~~M04: commit skill to aDNA base template~~ DONE. (2) mission_adna_rename_evaluation: GO/NO-GO on full .aDNA rename. (3) lattice_yaml_schema.json: add `skill`, `infrastructure` types + `status` field. (4) lattice-protocol GENERATION_CONTEXT.md: fix "agentic-DNA" → "Agentic-DNA".

## Final Campaign AAR

- **Worked**: "Procedure becomes the skill" approach — executing the upgrade ourselves produced a battle-tested, specific skill rather than a theoretical one. Aggressive cleanup (12 items archived) immediately improved workspace legibility. Symlink pattern (`ln -s adna/.adna .adna`) elegantly bridges template accessibility without file duplication.
- **Didn't**: Initial M00 audit missed the `.adna/` symlink requirement — user caught it. D3 ("track workspace CLAUDE.md in adna repo") remains partially unresolved: the site-specific CLAUDE.md has a local project table that can't be templated.
- **Finding**: 5/5 missions, ~1.5 sessions total (62.5% under 4.0 budget). Two-convention workspace (legacy names + `.aDNA` suffix) is functional but creates documentation overhead. The named-projects table requires manual maintenance per workspace.
- **Change**: Skill now includes explicit "CRITICAL — always verify" language on the symlink step. Future skills should be written generically from the start, then specialized for internal use — not the reverse.
- **Follow-up**: (1) mission_adna_rename_evaluation — standalone GO/NO-GO on full rename. (2) 3 schema gaps backlogged (lattice_yaml_schema.json types, GENERATION_CONTEXT capitalization).
