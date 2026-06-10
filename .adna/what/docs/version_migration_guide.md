---
type: context
title: "Version Migration Guide"
created: 2026-03-19
updated: 2026-03-19
status: active
last_edited_by: agent_init
tags: [migration, versioning, maintainer, guide]
token_estimate: 1200
---

# Version Migration Guide

A maintainer's guide to the aDNA version migration system — how it works, when to create migration prompts, and how to write them.

---

## What Is the Migration System?

When the aDNA CLAUDE.md governance file is updated (version bump), vaults running older versions need a way to upgrade. The migration system provides **structured prompts** that guide agents through applying version-specific changes to a vault.

Each migration prompt is a self-contained instruction set:
- **Pre-flight checks** verify the vault is in the expected state
- **Migration steps** describe pattern-matched find/replace operations
- **Post-flight validation** confirms all changes applied correctly
- **Rollback instructions** provide per-file revert paths

Migrations live in `how/migrations/` and are indexed in `how/migrations/AGENTS.md`.

---

## When to Create a Migration Prompt

Create a migration prompt whenever a new CLAUDE.md version is released that changes:

| Change Type | Example | Migration Needed? |
|-------------|---------|-------------------|
| Frontmatter schema | New required field added | Yes |
| Version number | `version: "5.0"` → `"5.1"` | Yes |
| Structural changes | New directory convention, renamed sections | Yes |
| Content corrections | Fixed counts, updated file paths | Yes |
| Additive content only | New section added, no existing content changed | Maybe — only if agents need to know about it |
| Documentation updates | Clarified wording, fixed typos | No |

**Rule of thumb**: If an agent reading the old CLAUDE.md would give incorrect guidance, create a migration prompt.

---

## How to Write a Migration Prompt

### 1. Start from the template

Copy `how/templates/template_migration.md` and fill in the frontmatter:

```yaml
type: migration
source_version: "5.1"        # Exact version this migrates FROM
target_version: "5.2"        # Exact version this migrates TO
scope: governance             # governance | content | structure | mixed
risk_level: low               # low | medium | high
affected_files:
  - CLAUDE.md
  - STATE.md
```

### 2. Name the file

Follow the convention: `migrate_v{from}_to_v{to}.md`

Examples:
- `migrate_v5.0_to_v5.1.md`
- `migrate_v5.1_to_v5.2.md`

### 3. Document the actual diff

Use `git diff` between the two version commits to identify every change. For each changed file:

- List every modification as a find/replace pair
- Use **pattern matching**, not line numbers — user vaults may have different line numbers due to customization
- Include enough surrounding context to make patterns unique
- Explain why each change was made

### 4. Write migration steps

One file per step section. Within each step:

1. Open the file
2. Apply each find/replace from the changes table
3. Micro-verify: read back the changed section to confirm it applied

### 5. Write pre-flight and post-flight

**Pre-flight** must verify:
- Current version matches source_version exactly
- No uncommitted changes
- Expected patterns exist in affected files

**Post-flight** must verify:
- Every change from the changes table applied
- Version fields updated
- No syntax errors introduced (valid YAML frontmatter, valid Markdown)

### 6. Write rollback

Per-file rollback (reverse each find/replace) plus git shortcuts for common recovery scenarios.

### 7. Register the migration

Add a row to the Migration Registry table in `how/migrations/AGENTS.md`.

---

## How to Test a Migration Prompt

1. **Clone a fresh vault** at the source version (or check out the source version commit)
2. **Run the migration** by having an agent follow the prompt
3. **Verify** all post-flight checks pass
4. **Diff** the result against the target version commit — they should be functionally equivalent (whitespace and ordering differences are acceptable)

For the canonical example, see `how/migrations/migrate_v5.0_to_v5.1.md` which was built from the real diff between commits `4cabdf2` (v5.0) and `ca013da` (v5.1).

---

## Sequential Composition Design

Migrations are designed to compose in sequence. Each migration:

- **Assumes** the state left by the previous migration (or a fresh vault at the source version)
- **Leaves** a valid vault state at the target version
- **Does not conflict** with other migrations (no overlapping edits to the same pattern)

This means:
- Migration N+1 can safely reference patterns that migration N introduced
- A vault can jump multiple versions by chaining migrations: v5.0→v5.1→v5.2→...
- Each migration is independently testable and rollbackable

### Avoiding Conflicts

When writing a migration that modifies the same file as a previous migration:
- Reference the patterns as they exist **after** the previous migration, not as they existed in the original
- If you're unsure, test the chain: apply migrations 1 through N-1, then verify your migration N applies cleanly

---

## CHANGELOG Cross-Linking Convention

Every changelog entry for a versioned release includes a **Migration** line linking to the corresponding migration prompt. This creates a bidirectional discovery path:

- **CHANGELOG → migration**: Users reading the changelog find the upgrade instructions inline
- **Migration → CHANGELOG**: Each migration's Related section links back to the CHANGELOG

When creating a new migration prompt, also add the corresponding changelog entry. When adding a changelog entry for a version with a migration, include the migration link.

---

## Future: Detection in CLAUDE.md

The current design requires users to discover the migration system via this guide, the README, or the `skill_version_migration` skill. A future enhancement could add version-check logic directly to CLAUDE.md:

```markdown
## Version Check (Future)

On startup, if `how/migrations/AGENTS.md` exists:
1. Read current version from this file's frontmatter
2. Scan migration registry for applicable upgrades
3. If upgrades available, inform user and offer to run skill_version_migration
```

This is **documented here but not implemented** — adding it to CLAUDE.md would require a version bump and introduce a bootstrapping concern (how does a vault on v5.0 discover the migration system if the detection logic only exists in v5.2?). The skill and README paths avoid this chicken-and-egg problem.

---

## Related

- [`CHANGELOG.md`](../../CHANGELOG.md) — Version history with migration cross-links
- [`how/migrations/AGENTS.md`](../../how/migrations/AGENTS.md) — Migration registry and sequential rules
- [`how/templates/template_migration.md`](../../how/templates/template_migration.md) — Migration prompt template
- [`how/migrations/migrate_v5.0_to_v5.1.md`](../../how/migrations/migrate_v5.0_to_v5.1.md) — Canonical example
- [`how/skills/skill_version_migration.md`](../../how/skills/skill_version_migration.md) — Agent skill for guided upgrades
- [`what/docs/migration_safety_framework.md`](migration_safety_framework.md) — Safety guarantees, limitations, recovery ladder
