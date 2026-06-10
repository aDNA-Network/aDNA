---
quest_id: quest_migration_smoke_test
type: side_quest
title: "Migration Smoke Test — v5.1 to v5.2"
difficulty: easy
estimated_token_cost: ~1K
model_requirements: "any"
status: active
created: 2026-03-20
updated: 2026-03-20
last_edited_by: agent_init
tags: [side_quest, migration, smoke-test, version-management]
---

# Quest: Migration Smoke Test

## Objective

Run the `migrate_v5.1_to_v5.2` migration prompt on a fresh vault and measure success/failure, token cost, friction points, and rollback behavior.

## Prerequisites

- aDNA vault version: v5.1 (you will migrate it to v5.2)
- Model: any (record which model you use)
- Vault state: fresh clone of the adna repo, checked out at the v5.1 tag or with CLAUDE.md manually set to `version: "5.1"`
- Estimated time: 10-15 minutes
- Estimated token cost: ~1K tokens

## Procedure

1. **Setup** — Clone a fresh copy of the adna repo. Verify `CLAUDE.md` frontmatter shows `version: "5.1"`. If the repo is at a later version, edit the version field to `"5.1"` and remove any v5.2+ additions (CHANGELOG.md) to simulate a pre-migration state.

2. **Run migration** — Open a new agent session in the vault. Provide the migration prompt from `how/migrations/migrate_v5.1_to_v5.2.md`. Let the agent execute the migration steps.

3. **Record outcome** — Note:
   - Did the migration complete without errors? (`success: true/false`)
   - How many tokens did the migration session consume?
   - Were there any steps where the agent hesitated, asked for clarification, or made an error?
   - Did the agent correctly create `CHANGELOG.md`?
   - Did the agent correctly update `CLAUDE.md` version to `"5.2"`?

4. **Rollback test** — After migration, run `git diff` to see all changes. Then run `git checkout .` to rollback. Verify the vault returns to pre-migration state cleanly.

5. **Collect** — Fill in the measurements below.

## Expected Output

```yaml
# Paste this into your result file's Raw Data section
quest_id: quest_migration_smoke_test
measurements:
  migration_success: true | false
  total_tokens: <value>
  agent_errors: <count of errors or hesitations>
  changelog_created: true | false
  version_bumped: true | false
  rollback_clean: true | false
  friction_points: <count>
success: true | false
notes: "describe any friction points or unexpected behavior"
```

## Submission Instructions

1. Fork the [Agentic-DNA repo](https://github.com/LatticeProtocol/adna) (or use your existing fork)
2. Create a result file: `how/quests/results/result_migration_smoke_test_<YYYYMMDD>_<your_name>.md`
3. Use the [quest result template](../../how/templates/template_quest_result.md) for the file format
4. Fill in all required sections — especially the Raw Data YAML block
5. Open a PR to the `main` branch with title: `result: quest_migration_smoke_test — <your_name>`
6. **Privacy**: Do not include PII, API keys, or sensitive data. Only performance metrics and structural observations.
