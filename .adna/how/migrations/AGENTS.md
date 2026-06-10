---
type: directory_index
created: 2026-03-19
updated: 2026-04-06
last_edited_by: agent_init
tags: [directory_index, migrations, versioning]
---

# how/migrations/ — Version Migration Prompts

## Purpose

Version migration prompts that guide agents through upgrading an aDNA vault from one CLAUDE.md version to the next. Each migration is a self-contained instruction set: pre-flight checks, pattern-matched changes, post-flight validation, and rollback procedures.

## Migration Registry

| Migration | Source | Target | Scope | Risk | Status |
|-----------|--------|--------|-------|------|--------|
| `migrate_v5.0_to_v5.1.md` | 5.0 | 5.1 | governance + state | low | active |
| `migrate_v5.1_to_v5.2.md` | 5.1 | 5.2 | governance + state | low | active |
| `migrate_v5.2_to_v6.0.md` | 5.2 | 6.0 | governance + state + manifest | medium | active |
| `migrate_object_skill.md` | pre-lsu | lsu-1.0 | skill objects (frontmatter) | low | active |
| `migrate_object_module.md` | pre-lsu | lsu-1.0 | module objects + companion YAML | medium | active |
| `migrate_object_dataset.md` | pre-lsu | lsu-1.0 | dataset objects + companion YAML | medium | active |
| `migrate_object_lattice.md` | pre-lsu | lsu-1.0 | lattice objects (MD↔YAML pairing) | medium | active |

## Safety Protocol

Every migration creates a `pre-migration-vX.Y` tag before changes and a `migration-vX.Y-to-vX.Z` tag after commit. Tag-based rollback is the primary recovery method. Full safety guarantees, limitations, and recovery procedures: [`what/docs/migration_safety_framework.md`](../../what/docs/migration_safety_framework.md).

## Sequential Application Rules

Migrations MUST be applied in strict version order. These five rules are inviolable:

1. **Exact source match.** The vault's current CLAUDE.md `version` field must exactly match the migration's `source_version` before applying. Do not attempt a migration if the source version does not match.

2. **Chain in version order, never skip.** To go from v5.0 to v5.2, apply v5.0→v5.1 first, then v5.1→v5.2. Never skip intermediate versions — each migration assumes the state left by the previous one.

3. **Complete post-flight before advancing.** Finish all post-flight validation checks for migration N before beginning migration N+1. A partial migration is worse than no migration.

4. **Skip if current version is at or beyond target.** If the vault's version is already >= the migration's target version, skip it entirely.

5. **Each migration is independently rollbackable.** Every migration includes per-file rollback instructions. If a migration fails mid-flight, roll back that migration completely before attempting anything else.

## Discovery Protocol

When an agent needs to check for available upgrades:

1. **Read version.** Open `CLAUDE.md` and extract the `version` field from frontmatter.
2. **Scan registry.** Read this file's Migration Registry table.
3. **Build upgrade chain.** Find all migrations where `source_version` chains from the current version forward. Order by version sequence.
4. **Present to user.** Show the upgrade path with scope, risk, and affected files for each step.
5. **Require explicit approval.** Never auto-apply migrations. The user must confirm before each migration begins.

## Load/Skip Decision

**Load when**:
- User asks to "upgrade", "update", or "check for updates" to their vault
- Agent detects a version mismatch during startup
- Creating a new migration prompt (read this for conventions)

**Skip when**:
- Normal operational work that doesn't involve version management
- Already loaded and working through a specific migration prompt

**Token cost**: ~500 tokens (this AGENTS.md). Individual migration prompts are ~100-150 lines each.

## Cross-References

- [how/skills/skill_version_migration.md](../skills/skill_version_migration.md) — Agent skill for guided upgrades
- [how/templates/template_migration.md](../templates/template_migration.md) — Template for creating new migration prompts
- [what/docs/version_migration_guide.md](../../what/docs/version_migration_guide.md) — Maintainer documentation
- [how/AGENTS.md](../AGENTS.md) — Operations layer index
