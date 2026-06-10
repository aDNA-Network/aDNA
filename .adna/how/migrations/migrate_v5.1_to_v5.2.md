---
type: migration
source_version: "5.1"
target_version: "5.2"
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

# Migration: v5.1 → v5.2

## Summary

**What changed**: CHANGELOG.md added to repo root with version policy. CLAUDE.md version bump. STATE.md updated with v5.2 reference and CHANGELOG in "What's Working" list.

**Why**: Version history was scattered across STATE.md, git commits, and CLAUDE.md frontmatter. No public-facing changelog existed for GitHub audiences. The versioning scheme (two independent tracks for governance and standard) was implicit, not documented.

**Impact**: Users and agents can now find a single CHANGELOG.md at repo root for version history. The version policy documents what constitutes major vs. minor changes for both tracks. Migration prompts are cross-linked from changelog entries.

## Pre-Flight Checks

1. **Version verification**: Read `CLAUDE.md` frontmatter. Confirm `version: "5.1"`. If the version is already `"5.2"` or higher, STOP — this migration does not apply.
2. **Clean working state**: Run `git status`. If there are uncommitted changes, ask the user to commit or stash first.
3. **Read affected files**: Read `CLAUDE.md` and `STATE.md`. Confirm the patterns described below exist.
4. **Create safety snapshot**: Run `git tag pre-migration-v5.1`. If the tag already exists, STOP — a prior migration attempt may have failed. Investigate or delete the stale tag before proceeding.
5. **Verify no concurrent sessions**: Check `how/sessions/active/` for other active sessions modifying governance files. If found, coordinate or wait.

## Changes

### File: CLAUDE.md

| # | Find | Replace | Why |
|---|------|---------|-----|
| 1 | `version: "5.1"` | `version: "5.2"` | Version bump |
| 2 | `<!-- v5.1 \| 2026-03-18 -->` (top) | `<!-- v5.2 \| 2026-03-19 -->` | Top version comment |
| 3 | `<!-- v5.1 \| 2026-03-18 -->` (bottom) | `<!-- v5.2 \| 2026-03-19 -->` | Bottom version comment |

### File: STATE.md

| # | Find | Replace | Why |
|---|------|---------|-----|
| 1 | `aDNA v5.1` | `aDNA v5.2` | Version reference in status paragraph |
| 2 | (add to "What's Working" list) | `- CHANGELOG.md with version policy and migration cross-links` | New infrastructure |

## Migration Steps

### Step 1: Update CLAUDE.md

1. Open `CLAUDE.md`
2. **Frontmatter version**: Find `version: "5.1"` in frontmatter, replace with `version: "5.2"`
3. **Top version comment**: Find the line `<!-- v5.1 | 2026-03-18 -->` near the top of the file (after frontmatter), replace with `<!-- v5.2 | 2026-03-19 -->`
4. **Bottom version comment**: Find `<!-- v5.1 | 2026-03-18 -->` near the bottom of the file, replace with `<!-- v5.2 | 2026-03-19 -->`
5. **Verify**: Read CLAUDE.md frontmatter. Confirm `version: "5.2"`.

### Step 2: Update STATE.md

1. Open `STATE.md`
2. **Version reference**: Find `aDNA v5.1` in the status summary paragraph, replace with `aDNA v5.2`
3. **What's Working**: Add `- CHANGELOG.md with version policy and migration cross-links` to the "What's Working" bullet list
4. **Verify**: Read STATE.md. Confirm the version reference says `v5.2`.

## Post-Flight Validation

- [ ] `CLAUDE.md` frontmatter: `version: "5.2"`
- [ ] `CLAUDE.md` top version comment: `<!-- v5.2 | 2026-03-19 -->`
- [ ] `CLAUDE.md` bottom version comment: `<!-- v5.2 | 2026-03-19 -->`
- [ ] `STATE.md`: `aDNA v5.2` in status paragraph
- [ ] `STATE.md`: CHANGELOG.md listed in "What's Working"

**Structural checks**:
- [ ] `CLAUDE.md` has valid YAML frontmatter (parseable, no syntax errors)
- [ ] `STATE.md` has valid YAML frontmatter (parseable, no syntax errors)
- [ ] `CHANGELOG.md` exists at repo root

All checks passing = migration complete. Commit the changes:
```
git add CLAUDE.md STATE.md && git commit -m "chore: migrate aDNA vault from v5.1 to v5.2"
git tag migration-v5.1-to-v5.2
```

## Rollback

**Option 1 — Tag-based full rollback** (recommended if pre-migration tag exists):
```
git reset --hard pre-migration-v5.1
git tag -d migration-v5.1-to-v5.2
```
> **Warning**: This discards ALL changes since the tag, not just migration changes. Only use if the migration commit is the only change since the tag.

**Option 2 — Per-file rollback** (surgical, preserves other changes):

- **CLAUDE.md**: Reverse — `"5.2"` → `"5.1"`, `v5.2 | 2026-03-19` → `v5.1 | 2026-03-18` (both top and bottom).
- **STATE.md**: Reverse — `v5.2` → `v5.1`, remove the CHANGELOG.md bullet.

**Option 3 — Commit revert** (if committed):
```
git revert HEAD
```

**Option 4 — Unstaged discard** (if uncommitted):
```
git checkout -- CLAUDE.md STATE.md
```

## Related

- [CHANGELOG](../../CHANGELOG.md) — Version history with cross-links
- [Migration Registry](AGENTS.md) — All available migrations
- [Version Migration Skill](../skills/skill_version_migration.md) — Guided upgrade workflow
- [Migration Safety Framework](../../what/docs/migration_safety_framework.md) — Guarantees, limitations, recovery ladder
