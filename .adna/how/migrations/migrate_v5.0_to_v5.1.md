---
type: migration
source_version: "5.0"
target_version: "5.1"
scope: governance
risk_level: low
affected_files:
  - CLAUDE.md
  - STATE.md
created: 2026-03-19
updated: 2026-03-19
status: active
last_edited_by: agent_init
tags: [migration]
---

# Migration: v5.0 → v5.1

## Summary

**What changed**: CLAUDE.md governance updates — lattice types table expanded (7 values), template count corrected (10→17), standard file path references fixed (pointed to context library instead of nonexistent standalone files). STATE.md counts and version references updated to match.

**Why**: The comprehensive review campaign (M08) identified factual drift between CLAUDE.md and the actual vault state. Template counts, file paths, and lattice type coverage were out of date.

**Impact**: Agents reading CLAUDE.md will get accurate template counts, correct file paths for object standards, and the full lattice type vocabulary. No behavioral changes — this is a governance accuracy fix.

## Pre-Flight Checks

1. **Version verification**: Read `CLAUDE.md` frontmatter. Confirm `version: "5.0"`. If the version is already `"5.1"` or higher, STOP — this migration does not apply.
2. **Clean working state**: Run `git status`. If there are uncommitted changes, ask the user to commit or stash first.
3. **Read affected files**: Read `CLAUDE.md` and `STATE.md`. Confirm the patterns described below exist.
4. **Create safety snapshot**: Run `git tag pre-migration-v5.0`. If the tag already exists, STOP — a prior migration attempt may have failed. Investigate or delete the stale tag before proceeding.

## Changes

### File: CLAUDE.md

| # | Find | Replace | Why |
|---|------|---------|-----|
| 1 | `version: "5.0"` | `version: "5.1"` | Version bump |
| 2 | `token_estimate: ~650` | `token_estimate: ~2500` | Corrected token count |
| 3 | `<!-- v5.0 |` (top of file, after frontmatter) | `<!-- v5.1 | 2026-03-18 -->` | Version comment |
| 4 | `templates/               # 10 reusable templates` | `templates/               # 17 reusable templates` | Corrected template count |
| 5 | Standard file path references (see Step 1.5 below) | Context library references | Paths pointed to nonexistent standalone files |
| 6 | `<!-- v5.0 |` (bottom of file) | `<!-- v5.1 | 2026-03-18 -->` | Footer version comment |

### File: STATE.md

| # | Find | Replace | Why |
|---|------|---------|-----|
| 1 | `aDNA v5.0` | `aDNA v5.1` | Version reference in status line |
| 2 | `4 topics, 20 subtopics` | `4 topics, 23 subtopics` | Corrected subtopic count |
| 3 | `14 templates including` | `17 templates including` | Corrected template count |

## Migration Steps

### Step 1: Update CLAUDE.md

1. Open `CLAUDE.md`

2. **Frontmatter version**: Find `version: "5.0"` in frontmatter, replace with `version: "5.1"`

3. **Token estimate**: Find `token_estimate: ~650` in frontmatter, replace with `token_estimate: ~2500`

4. **Top version comment**: Find the line starting with `<!-- v5.0 |` near the top of the file (after the frontmatter closing `---`), replace with `<!-- v5.1 | 2026-03-18 -->`

5. **Template count in project map**: Find `templates/               # 10 reusable templates` in the project map tree, replace `10` with `17`

6. **Object standard file paths**: In the Object Standards table, find rows referencing standalone files like `what/modules/standard_module.md` or `what/datasets/standard_dataset.md`. Replace the "Standard" column header with "Context Reference" and point all three rows (Module, Dataset, Lattice) to `what/context/object_standards/`. The Lattice row keeps its schema reference to `what/lattices/lattice_yaml_schema.json`.

7. **Lattice types table**: If the Lattice Types table has fewer than 7 entries, add the missing types: `infrastructure`, `context_set`, `skill`. These go after the existing entries (`pipeline`, `agent`, `context_graph`, `workflow`).

8. **Bottom version comment**: Find `<!-- v5.0 |` near the bottom of the file, replace with `<!-- v5.1 | 2026-03-18 -->`

9. **Verify**: Read CLAUDE.md frontmatter. Confirm `version: "5.1"` and `token_estimate: ~2500`.

### Step 2: Update STATE.md

1. Open `STATE.md`

2. **Version reference**: Find `aDNA v5.0` in the status summary paragraph, replace with `aDNA v5.1`

3. **Subtopic count**: Find `4 topics, 20 subtopics` and replace with `4 topics, 23 subtopics`

4. **Template count**: Find the line mentioning template count (e.g., `14 templates including`) and update the number to `17`. Also update the template list to include: `AAR, strategic compass, campaign CLAUDE.md, registry, data record, folder note, PRD, RFC`

5. **Verify**: Read STATE.md. Confirm the version reference says `v5.1` and counts are updated.

## Post-Flight Validation

- [ ] `CLAUDE.md` frontmatter: `version: "5.1"`
- [ ] `CLAUDE.md` frontmatter: `token_estimate: ~2500`
- [ ] `CLAUDE.md` top version comment: `<!-- v5.1 | 2026-03-18 -->`
- [ ] `CLAUDE.md` bottom version comment: `<!-- v5.1 | 2026-03-18 -->`
- [ ] `CLAUDE.md` project map: `17 reusable templates`
- [ ] `STATE.md`: `aDNA v5.1` in status paragraph

**Structural checks**:
- [ ] `CLAUDE.md` has valid YAML frontmatter (parseable, no syntax errors)
- [ ] `STATE.md` has valid YAML frontmatter (parseable, no syntax errors)
- [ ] No broken wikilinks introduced by the migration

All checks passing = migration complete. Commit the changes:
```
git add CLAUDE.md STATE.md && git commit -m "chore: migrate aDNA vault from v5.0 to v5.1"
git tag migration-v5.0-to-v5.1
```

## Rollback

**Option 1 — Tag-based full rollback** (recommended if pre-migration tag exists):
```
git reset --hard pre-migration-v5.0
git tag -d migration-v5.0-to-v5.1
```
> **Warning**: This discards ALL changes since the tag, not just migration changes. Only use if the migration commit is the only change since the tag.

**Option 2 — Per-file rollback** (surgical, preserves other changes):

- **CLAUDE.md**: Reverse each replacement — `"5.1"` → `"5.0"`, `~2500` → `~650`, `v5.1` → `v5.0`, `17` → `10`, restore original standard file paths.
- **STATE.md**: Reverse — `v5.1` → `v5.0`, `23` → `20`, `17` → `14`.

**Option 3 — Commit revert** (if committed):
```
git revert HEAD
```

**Option 4 — Unstaged discard** (if uncommitted):
```
git checkout -- CLAUDE.md STATE.md
```

## Related

- [Migration Registry](AGENTS.md) — All available migrations
- [Version Migration Skill](../skills/skill_version_migration.md) — Guided upgrade workflow
- [Migration Safety Framework](../../what/docs/migration_safety_framework.md) — Guarantees, limitations, recovery ladder
