# Pre-Push Sanitization Hook — Test Fixtures

> **Purpose**: smoke-test the `pre-push-sanitize.sh` rule logic without requiring a real `git push`. Used by `pre-push-sanitize.sh --self-test` (invoked by `skill_deploy` post-install).

## Layout

```
test_fixtures/
├── clean/              # files that MUST produce zero findings
│   ├── README.md
│   └── what/concepts/example_concept.md
└── dirty/              # files that MUST produce at least one named finding
    ├── what/local/notes.md          # R1: private path leakage
    ├── fake_with_secret.md          # R2: secret pattern match
    ├── config/.env                  # R3: credential filename
    ├── large_binary.bin             # R4: >10 MiB binary
    └── draft_post.md                # R6: frontmatter status: draft
```

## Rule coverage

| Rule | Covered? | Fixture |
|---|---|---|
| R1 (private path leakage) | ✅ | `dirty/what/local/notes.md` |
| R2 (secret-pattern match) | ✅ | `dirty/fake_with_secret.md` |
| R3 (filename patterns) | ✅ | `dirty/config/.env` |
| R4 (large binary > threshold) | ✅ | `dirty/large_binary.bin` (12 MiB) |
| R5 (frontmatter confidential/private: true) | ⏳ deferred | not in M05 S2 fixture set |
| R6 (frontmatter status: draft) | ✅ | `dirty/draft_post.md` |
| R7 (operator deny list) | ⏳ deferred | not in M05 S2 fixture set |

Spec authority: `pre_push_hook_spec.md` §5 (covers R1/R2/R3/R4/R6; R5+R7 deferred to first operator use).

## Authoring conventions

- **Clean fixtures** must trigger zero R1-R7 findings — kept minimal, no frontmatter flags, no private paths, no secret patterns, no large binaries.
- **Dirty fixtures** must each trigger exactly one *named* finding — labeled in the fixture file (in a comment or frontmatter) so the self-test can verify the right rule fired.
- **Synthetic secrets**: any "secret" value in a dirty fixture must be obviously synthetic. The `pragma: allowlist secret` marker is reserved for production false-positive overrides, not fixtures.
- **Binary fixtures**: generated reproducibly via `dd if=/dev/zero ...` so the fixture set rebuilds bit-identical across machines.

## Regenerate

`dirty/large_binary.bin` is gitignored from publishing (the hook treats it as R4 violation, but the fixture file itself is intentionally large for the test). If lost, regenerate:

```bash
dd if=/dev/zero of=dirty/large_binary.bin bs=1M count=12
```

Other fixtures are plain text and version-controlled normally.
