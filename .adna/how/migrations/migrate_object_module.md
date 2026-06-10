---
type: migration
migration_id: migrate_object_module
source_version: "pre-lsu"
target_version: "lsu-1.0"
object_type: module
created: 2026-03-20
updated: 2026-03-20
last_edited_by: agent_init
status: active
tags: [migration, upgrade-system, module]
---

# Migration: Module — pre-LSU → LSU-1.0

## Summary

Upgrades vault modules to full aDNA compliance by adding version fields, enriching FAIR metadata, adding federation stubs, and generating companion `.module.yaml` files for federation-critical modules. Scope is limited to ~15-20 federation-critical modules per FA Decision D3 — not all 33.

**Gaps addressed**: G-009 (versioning absent on 23/33 modules), G-010 (zero `.module.yaml` companions exist), G-013 (federation metadata absent).

## Scope

- **Object type**: module
- **Discovery**: Files matching `type: module` in frontmatter
- **Location**: `what/modules/module_*.md`
- **Version gate**: Skip if `_migration_version: "lsu-1.0"` already present
- **Federation-relevance filter**: Only generate companion `.module.yaml` for modules that are federation-critical. A module is federation-critical if ANY of:
  - It is part of a bio pipeline (referenced in a lattice YAML or lattice MD)
  - Its `module_type` is `model`, `tool`, or `runtime` (not `mcp_server`)
  - It has existing `fair:` metadata suggesting external use
- **Companion exclusions**: MCP server modules (`module_mcp_*`) get frontmatter upgrades only — no companion YAML (per D3 scope)

## Pre-Flight

1. [ ] Object file exists and is readable
2. [ ] Current frontmatter parses as valid YAML without error
3. [ ] Object has `type: module` in frontmatter
4. [ ] Object is not locked by another migration (no `_migration_lock` field)
5. [ ] Compliance checker pre-migration score recorded

## Changes

| # | Field | Current | Target | Action | Judgment? |
|---|-------|---------|--------|--------|:---------:|
| 1 | `version` | absent (23/33) | SemVer string (default `"0.1.0"`) | add | Yes — check changelog or commit history |
| 2 | `module_type` | may be non-canonical | Canonical enum: `model`, `tool`, `runtime`, `mcp_server`, `library` | normalize | No — mechanical mapping |
| 3 | `fair.keywords` | absent or minimal | ≥1 keyword array | add/enrich | Yes — read module description |
| 4 | `fair.license` | absent | License identifier string | add | Yes — infer from repo context |
| 5 | `fair.accessibility` | absent | `"internal"` (default) | add | No |
| 6 | `federation.discoverable` | absent | `true` | add | No |
| 7 | `.module.yaml` | absent (all 33) | Generated companion file | generate | Yes — entrypoint, keywords, container |
| 8 | `_migration_version` | absent | `"lsu-1.0"` | add | No |

### `version` Guidance

- If the module has a `changelog` section or `## Version History`, extract the latest version
- If the module references a specific model version (e.g., ESM-2 3B), use `"1.0.0"`
- If no version information exists, use `"0.1.0"` (pre-release)
- MCP servers: use `"0.1.0"` unless the server has a known version

### `module_type` Canonical Values

| Current | Canonical |
|---------|-----------|
| `model`, `ml_model`, `ai_model` | `model` |
| `tool`, `utility` | `tool` |
| `runtime`, `compute` | `runtime` |
| `mcp_server`, `mcp` | `mcp_server` |
| `library`, `sdk` | `library` |

If the current value doesn't map, read the module description to classify.

### `fair.license` Guidance

- Bio pipeline modules: `"Apache-2.0"` (vault default) unless module wraps a restrictively-licensed model
- MCP servers: `"Apache-2.0"`
- External model wrappers: Check the model's actual license (e.g., ESM-2 is MIT, RFDiffusion is BSD)
- If uncertain: `"Apache-2.0"` with a `# TODO: verify license` comment

## Steps

### Step 1: Read Current State

Read the module file. Parse frontmatter. Record current fields and identify which changes apply.

### Step 2: Add/Update `version`

If `version` is absent, determine the appropriate version (see guidance above) and add after `module_type`:

```yaml
version: "0.1.0"
```

### Step 3: Normalize `module_type`

If `module_type` uses a non-canonical value, replace with the canonical equivalent per the mapping table. If already canonical, skip.

### Step 4: Add/Enrich FAIR Block

If no `fair:` block exists, add it:

```yaml
fair:
  keywords: ["keyword1", "keyword2"]
  license: "Apache-2.0"
  accessibility: "internal"
```

If a `fair:` block exists, add missing fields without overwriting existing values.

**Keywords**: Read the module's description, `## Purpose`, or `## Overview` section. Extract 1-3 keywords that describe the module's function. Examples:
- `module_esm` → `["protein", "language-model", "embedding"]`
- `module_mcp_playwright` → `["browser", "automation", "testing"]`
- `module_rfdiffusion` → `["protein-design", "diffusion", "structure-generation"]`

### Step 5: Add Federation Stub

If no `federation:` block exists, add it:

```yaml
federation:
  discoverable: true
```

### Step 6: Generate Companion `.module.yaml` (if federation-critical)

**Skip this step if**: Module is an MCP server (`module_mcp_*`) or fails the federation-relevance filter.

Follow the 5-step companion generation process:

#### 6a. Extract

Pull from the `.md` frontmatter:
- `name` (from filename, e.g., `module_rfdiffusion` → `rfdiffusion`)
- `version` (from Step 2)
- `module_type` (from Step 3)
- `runtime` (if present in frontmatter)
- `entrypoint` (if present, or infer from body content)

#### 6b. Template

```yaml
# <module_name>.module.yaml
# Generated by migrate_object_module (lsu-1.0)
name: "<module_name>"
version: "<version>"
module_type: "<module_type>"

runtime:
  entrypoint: "<entrypoint or null>"
  container: "<container image or null>"
  requirements: []

fair:
  keywords: []  # Copied from .md
  license: "<license>"

federation:
  discoverable: true
```

#### 6c. Judge

Agent determines these fields by reading the module's body content:
- **`entrypoint`**: Look for code blocks, CLI commands, or `## Usage` sections
- **`container`**: Look for Docker references, runtime mentions
- **`keywords`**: Copy from the `.md` FAIR block (Step 4)
- **`requirements`**: Look for dependency lists, pip/conda requirements

If a field cannot be determined, set it to `null`. Do not guess.

#### 6d. Validate

Before writing, verify:
- YAML parses without error
- `name` field matches the module name
- `version` matches the `.md` frontmatter version
- `federation.discoverable` is `true`

#### 6e. Write

Save as `what/modules/<module_name>.module.yaml` alongside the `.md` file.

**Naming convention**: `module_X.module.yaml` alongside `module_X.md`.

### Step 7: Add Migration Version

Add as the last frontmatter field in the `.md` file:

```yaml
_migration_version: "lsu-1.0"
```

### Step 8: Verify

Re-read the `.md` file and companion (if generated). Confirm YAML parses, all target fields present, body unchanged.

## Post-Flight

1. [ ] `.md` frontmatter parses as valid YAML without error
2. [ ] `version` field present with valid SemVer string
3. [ ] `module_type` uses canonical enum value
4. [ ] `fair.keywords` present with ≥1 keyword
5. [ ] `fair.license` present
6. [ ] `federation.discoverable: true` present
7. [ ] `_migration_version: "lsu-1.0"` present
8. [ ] Body content unchanged
9. [ ] Companion `.module.yaml` validates (if generated) — YAML parses, required fields present
10. [ ] Companion filename matches convention (`<module_name>.module.yaml`)
11. [ ] Compliance score improved or unchanged vs pre-migration

## Rollback

- **L1** (single file): `git checkout -- <md_path>` and `rm <yaml_path>` (if companion was generated)
- **L2** (field-level): Revert specific frontmatter fields. Remove `version`, `fair`, `federation`, `_migration_version` if they were added.
- **L3** (batch): `git reset --hard <pre-migration-tag>` (e.g., `pre-lsu-m09`)

## Related

- [Migration Registry](AGENTS.md) — All available migrations
- Architecture Spec §4.4-§4.5 — Module prompt spec + companion generation (see operational vault campaign artifacts)
- Gap Register — G-009, G-010, G-013 (see operational vault campaign artifacts)
