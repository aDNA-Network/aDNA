---
type: context
title: "Migration Safety Framework"
created: 2026-03-19
updated: 2026-03-19
status: active
last_edited_by: agent_init
tags: [migration, safety, versioning, reference]
token_estimate: ~800
---

# Migration Safety Framework

Safety guarantees, known limitations, and recovery procedures for the aDNA version migration system.

---

## Safety Guarantees

The migration system provides these protections by design:

1. **Tagged snapshots.** Every migration is preceded by a git tag (`pre-migration-vX.Y`) capturing the exact vault state before changes begin. This tag serves as a reliable rollback point.

2. **Structural validation.** Every migration is followed by a structural sweep — YAML frontmatter parsing, wikilink integrity check, and version field verification — in addition to migration-specific post-flight checks.

3. **Independent rollback.** Each migration in a chain is independently rollbackable. A failure in migration N does not corrupt the results of migration N-1.

4. **Explicit approval required.** Migrations never auto-apply. The agent presents the upgrade path and requires user confirmation before proceeding.

5. **Pattern-tolerant matching.** Migration prompts use pattern matching (not line numbers) to locate content. Minor user customizations (reworded sections, added content) won't cause silent mis-application — the migration STOPs if a pattern isn't found.

---

## Known Limitations

Honest boundaries of what the system does *not* guarantee:

1. **Customized content may not match.** If a user has heavily rewritten sections that a migration targets, the find/replace patterns will fail. The migration STOPs rather than silently producing incorrect output, but the user must then apply changes manually.

2. **Structural, not semantic, validation.** The post-flight sweep validates syntax (valid YAML, resolvable links, correct version field) but cannot verify that content is *semantically* correct.

3. **`git reset --hard` is total.** Tag-based rollback discards ALL changes since the tag — not just migration changes. If the user made other edits between the tag and the rollback, those edits are lost. Per-file rollback or `git revert` are safer if other changes exist.

4. **No automated test infrastructure.** Migrations are tested via manual agent-driven worktree procedures. There is no CI/CD pipeline for migration validation.

5. **Per-machine independence.** Each machine migrates its own vault copy independently. Cross-machine consistency depends on git push/pull — the migration system does not verify that all clones are at the same version.

---

## Backup Best Practices

User responsibilities before running a migration:

1. **Ensure the vault is a git repo with a remote.** The entire safety model depends on git. Non-git vaults lack rollback capability.

2. **Push before migrating.** Run `git push` before starting any migration. This creates a remote backup that survives local rollback operations.

3. **Non-git users: zip/tar backup.** If the vault is not git-managed, create a full archive (`zip -r vault-backup.zip .` or `tar czf vault-backup.tar.gz .`) before migrating.

4. **Push after success.** After a successful migration, push to propagate the migration commit and tags to the remote: `git push && git push --tags`.

---

## Error Recovery Ladder

Escalation path from least to most disruptive:

| Level | Method | When to Use | What It Does |
|-------|--------|-------------|-------------|
| **L1** | `git reset --hard pre-migration-vX.Y` | Migration failed, no other changes since tag | Restores exact pre-migration state |
| **L2** | `git checkout -- <file>` | Single file needs reverting, other files are fine | Restores one file to last committed state |
| **L3** | `git revert HEAD` | Migration committed, want to undo but preserve history | Creates a new commit that reverses the migration |
| **L4** | Manual repair | Automated rollback insufficient, specific edits needed | Re-read the migration prompt, apply changes by hand |
| **L5** | Fresh start | Vault is in an unrecoverable state | Clone the aDNA template, re-apply customizations |

**Always try L1 first** if the pre-migration tag exists. Escalate only if L1 is insufficient (e.g., non-migration changes would be lost).

---

## Testing Procedure

Worktree-based protocol for validating migration prompts before release:

1. **Create worktree** at the source version commit:
   ```
   git worktree add /tmp/migration-test <source-commit>
   ```

2. **Apply the migration** step by step in the worktree, following the prompt exactly — including all pre-flight checks, safety snapshot, migration steps, and post-flight validation.

3. **Diff against known-good target**:
   ```
   git diff <target-commit> -- <affected-files>
   ```
   Acceptable: whitespace, ordering, metadata timing differences. Unacceptable: missing version fields, wrong counts, broken patterns.

4. **Test rollback**: `git reset --hard pre-migration-vX.Y` — verify full restoration.

5. **Cleanup**: `git worktree remove /tmp/migration-test`

Record results in a test report artifact. See `m11_e2e_test_report.md` for the canonical example.

---

## Related

- [`how/migrations/AGENTS.md`](../../how/migrations/AGENTS.md) — Migration registry and sequential rules
- [`how/templates/template_migration.md`](../../how/templates/template_migration.md) — Migration prompt template
- [`how/skills/skill_version_migration.md`](../../how/skills/skill_version_migration.md) — Agent skill for guided upgrades
- [`what/docs/version_migration_guide.md`](version_migration_guide.md) — Maintainer guide
