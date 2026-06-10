---
type: skill
skill_type: agent
created: 2026-03-19
updated: 2026-03-19
status: active
category: operations
trigger: "User asks to upgrade, update, or check for vault updates"
last_edited_by: agent_init
tags: [skill, migration, versioning]

requirements:
  tools: []
  context: ["CLAUDE.md", "how/migrations/AGENTS.md"]
  permissions: ["write governance files"]
---

# Skill: Version Migration

## Overview

Guides an agent through upgrading an aDNA vault from its current CLAUDE.md version to the latest available version. Discovers applicable migrations, presents an upgrade plan, applies migrations sequentially, and validates results.

## Trigger

User says any of:
- "Upgrade my vault"
- "Check for updates"
- "Is my vault up to date?"
- "Migrate to the latest version"

Or: agent detects during startup that `CLAUDE.md` version is behind the latest migration target in the registry.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `target_version` | string | No | latest | Specific version to migrate to. If omitted, migrates to the latest available. |

## Requirements

### Tools/APIs
- File read/write access to the vault

### Context Files
- `CLAUDE.md` — current vault version (frontmatter `version` field)
- `how/migrations/AGENTS.md` — migration registry and sequential application rules

### Permissions
- Write governance files (CLAUDE.md, STATE.md, and any files listed in migration `affected_files`)

## Implementation

### Step 1: Version Discovery

1. Read `CLAUDE.md` frontmatter and extract the `version` field. This is the vault's current version.
2. Read `how/migrations/AGENTS.md` and parse the Migration Registry table.
3. Build the upgrade chain: find all migrations where versions chain forward from the current version. Order by version sequence.
4. If no applicable migrations exist (current version >= all targets), report "Vault is up to date at vX.Y" and stop.

### Step 2: User Briefing

Present the upgrade path as a table:

```
Upgrade path: v5.0 → v5.1

| Step | Migration          | Scope      | Risk | Affected Files     |
|------|--------------------|------------|------|--------------------|
| 1    | v5.0 → v5.1        | governance | low  | CLAUDE.md, STATE.md|
```

Include for each migration:
- Scope (governance, content, structure, mixed)
- Risk level (low, medium, high)
- Affected files
- Brief summary of what changes

**Require explicit user approval before proceeding.** Say: "Apply this upgrade? (Y/n)"

If the user declines, stop. Do not re-prompt.

### Step 3: Sequential Application

For each migration in the upgrade chain, in order:

1. **Load the migration prompt** — read the full migration file (e.g., `how/migrations/migrate_v5.0_to_v5.1.md`)
2. **Create safety snapshot** — run `git tag pre-migration-v{current}` (using the source version). If the tag already exists, STOP — a prior migration attempt may have failed. Ask the user to delete the stale tag or investigate before proceeding.
3. **Run pre-flight checks** — execute every check in the Pre-Flight Checks section. If any check fails, STOP and report the failure.
4. **Apply migration steps** — follow each numbered step in the Migration Steps section. Verify after each step.
5. **Run post-flight validation** — execute every check in the Post-Flight Validation section. If any check fails, STOP and report the failure.
6. **Structural sweep** — after migration-specific validation, run these additional checks:
   - Validate YAML frontmatter syntax on all files listed in `affected_files` (parseable `---` blocks, no errors)
   - Check that any wikilinks added or modified by the migration resolve to existing files
   - Verify `CLAUDE.md` frontmatter `version` matches `target_version`
   - *Optional*: For a broader structural check, run `skill_vault_review.md` Steps 1-3
7. **Commit and tag** — stage and commit with the message format from the migration file, then run `git tag migration-v{source}-to-v{target}`

**STOP on any failure.** Do not continue to the next migration if the current one has unresolved issues. Report the exact failure and offer rollback.

### Step 4: Completion Report

After all migrations are applied:

```
Migration complete.

| Migrated | Files Changed | Commit | Tags Created |
|----------|--------------|--------|-------------|
| v5.0 → v5.1 | CLAUDE.md, STATE.md | abc1234 | pre-migration-v5.0, migration-v5.0-to-v5.1 |

Vault is now at v5.1.
```

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Upgraded vault files | Files | Governance and content files updated to new version |
| Migration commits | Git commits | One atomic commit per migration step |
| Completion report | Text | Summary of what was applied |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Version mismatch | CLAUDE.md version doesn't match migration source | STOP. Report current version and available migrations. The user may need a different migration or manual intervention. |
| Pre-flight failure | Expected patterns not found in target files | STOP. The vault may have been manually modified. Report which patterns were expected and what was found. |
| Mid-migration failure | A step fails to apply | STOP. Follow the Rollback section of the current migration prompt. Report what succeeded and what failed. |
| No migrations directory | `how/migrations/` doesn't exist | The vault predates the migration system. Direct user to `what/docs/version_migration_guide.md` for manual upgrade options. |
| Chain gap | No migration exists from current version to next | STOP. Report the gap. The user may need to wait for a migration to be published or upgrade manually. |
| Tag already exists | `pre-migration-v{X}` tag present from prior attempt | STOP. Ask the user to delete the stale tag (`git tag -d pre-migration-v{X}`) or investigate the prior attempt before retrying. |
| Post-migration structural failure | YAML frontmatter invalid or broken wikilinks after migration | Rollback via `git reset --hard pre-migration-v{X}`. Delete the migration tag if it was created. Report which structural check failed. |

## Related

- **Migration Registry**: `how/migrations/AGENTS.md`
- **Migration Template**: `how/templates/template_migration.md`
- **Maintainer Guide**: `what/docs/version_migration_guide.md`
- **Migration Safety Framework**: `what/docs/migration_safety_framework.md`
- **Skills Protocol**: `how/skills/AGENTS.md`
