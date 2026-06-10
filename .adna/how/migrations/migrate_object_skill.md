---
type: migration
migration_id: migrate_object_skill
source_version: "pre-lsu"
target_version: "lsu-1.0"
object_type: skill
created: 2026-03-20
updated: 2026-03-20
last_edited_by: agent_init
status: active
tags: [migration, upgrade-system, skill]
---

# Migration: Skill — pre-LSU → LSU-1.0

## Summary

Registers vault skills as first-class aDNA lattice objects by adding `lattice_type: skill`, normalizing `skill_type`, adding FAIR metadata, and adding federation stubs. Skills are frontmatter-only migrations — no companion files generated. This is the highest-count migration (54+ objects) and lowest risk (no body content changes).

**Gaps addressed**: G-003 (`lattice_type` missing on 55/57 skills), G-007 (`skill_type` legacy/absent on 4 skills), G-012 (FAIR block missing on 55/57), G-013 (federation metadata absent).

## Scope

- **Object type**: skill
- **Discovery**: Files matching `type: skill` in frontmatter
- **Location**: `how/skills/skill_*.md`
- **Version gate**: Skip if `_migration_version: "lsu-1.0"` already present
- **Exclusions**: `how/skills/AGENTS.md`, `how/skills/sync/` (not skill objects)
- **Companion files**: None — all metadata lives in frontmatter

## Pre-Flight

1. [ ] Object file exists and is readable
2. [ ] Current frontmatter parses as valid YAML without error
3. [ ] Object has `type: skill` in frontmatter
4. [ ] Object is not locked by another migration (no `_migration_lock` field)
5. [ ] Compliance checker pre-migration score recorded (run `python compliance_checker.py <vault> --file <path>`)

## Changes

| # | Field | Current | Target | Action | Judgment? |
|---|-------|---------|--------|--------|:---------:|
| 1 | `lattice_type` | absent (55/57 skills) | `skill` | add | No |
| 2 | `skill_type` | `agent_type: agent`/`process` (3 files) OR absent (1 file) OR correct `skill_type` (53 files) | `agent` or `process` | add or rename | No — derive from content (see rules below) |
| 3 | `fair.keywords` | absent (55/57 skills) | ≥1 keyword array | add | Yes — agent reads skill description |
| 4 | `fair.license` | absent | `"Apache-2.0"` | add | No — vault default |
| 5 | `federation.discoverable` | absent | `true` | add | No |
| 6 | `_migration_version` | absent | `"lsu-1.0"` | add | No |

### `skill_type` Derivation Rules

For skills that lack `skill_type` or use the legacy `agent_type` field:

1. **If `trigger:` field exists in frontmatter** → `skill_type: agent`
2. **If body contains "When" trigger pattern** (e.g., "When a task requires...", "When the user asks...") → `skill_type: agent`
3. **If body describes a checklist/process** (e.g., "Step 1:", numbered procedure without event trigger) → `skill_type: process`
4. **If `agent_type:` field exists** → rename to `skill_type:` preserving the value (`agent` or `process`)

### `fair.keywords` Guidance

Read the skill's `## When to Use` or `## Purpose` section and extract 1-3 descriptive keywords. Examples:
- `skill_hub_deploy` → `["deployment", "jupyterhub"]`
- `skill_context_assembly` → `["context", "recipes"]`
- `skill_emergency_procedures` → `["emergency", "recovery", "rollback"]`

Do not invent keywords that aren't supported by the skill's content. If uncertain, use the skill's `category` field value as a single keyword.

## Steps

### Step 1: Read Current State

Read the skill file. Parse frontmatter. Record current fields.

### Step 2: Add `lattice_type`

If `lattice_type` is absent, add it after the `type` field:

```yaml
type: skill
lattice_type: skill
```

If `lattice_type` is already `skill`, skip. If it's a different value, **STOP** — flag for manual review.

### Step 3: Normalize `skill_type`

**Case A — Legacy `agent_type` field exists:**
Remove `agent_type` line. Add `skill_type` with the same value:

```yaml
# Before
agent_type: agent

# After
skill_type: agent
```

**Case B — No `skill_type` or `agent_type`:**
Apply derivation rules from Changes section above. Add the determined value:

```yaml
skill_type: agent  # or process
```

**Case C — `skill_type` already present with valid value:**
No action needed.

### Step 4: Add FAIR Block

If no `fair:` block exists, add it after the last standard field (before `tags`):

```yaml
fair:
  keywords: ["keyword1", "keyword2"]
  license: "Apache-2.0"
```

If a `fair:` block exists but is missing fields, add the missing fields without overwriting existing values.

### Step 5: Add Federation Stub

If no `federation:` block exists, add it after the `fair:` block:

```yaml
federation:
  discoverable: true
```

If `federation:` exists but `discoverable` is missing, add it.

### Step 6: Add Migration Version

Add as the last frontmatter field (before the closing `---`):

```yaml
_migration_version: "lsu-1.0"
```

### Step 7: Verify Frontmatter

Re-read the file. Confirm YAML parses without error. Confirm all 6 target fields are present with correct values.

## Post-Flight

1. [ ] Frontmatter parses as valid YAML without error
2. [ ] `lattice_type: skill` present
3. [ ] `skill_type` present with value `agent` or `process`
4. [ ] `fair.keywords` present with ≥1 keyword
5. [ ] `fair.license` present
6. [ ] `federation.discoverable: true` present
7. [ ] `_migration_version: "lsu-1.0"` present
8. [ ] Body content unchanged (no modifications below the frontmatter closing `---`)
9. [ ] Compliance score improved or unchanged vs pre-migration

## Rollback

- **L1** (single file): `git checkout -- <file_path>`
- **L2** (field-level): Revert specific frontmatter fields using the pre-migration score as reference. Remove added fields (`lattice_type`, `fair`, `federation`, `_migration_version`). Restore `agent_type` if it was renamed.
- **L3** (batch): `git reset --hard <pre-migration-tag>` (e.g., `pre-lsu-m07`)

## Related

- [Migration Registry](AGENTS.md) — All available migrations
- Architecture Spec §4.4 — Skill prompt specification (see operational vault campaign artifacts)
- Gap Register — G-003, G-007, G-012, G-013 (see operational vault campaign artifacts)
