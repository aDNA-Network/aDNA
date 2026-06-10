---
type: migration
migration_id: migrate_object_lattice
source_version: "pre-lsu"
target_version: "lsu-1.0"
object_type: lattice
created: 2026-03-20
updated: 2026-03-20
last_edited_by: agent_init
status: active
tags: [migration, upgrade-system, lattice]
---

# Migration: Lattice — pre-LSU → LSU-1.0

## Summary

Upgrades vault lattices to full aDNA compliance by normalizing `lattice_type`, adding execution metadata, enriching FAIR blocks, and resolving MD↔YAML pairing gaps. Lattices have the most complex migration logic due to three possible pairing states: MD-only, YAML-only, and paired objects.

**Gaps addressed**: G-002 (15 lattice MDs without YAML companions, 6 YAML lattices without MD wrappers), G-013 (federation metadata absent/weak).

## Scope

- **Object type**: lattice (both markdown and YAML)
- **Discovery**: Files matching `type: lattice` in frontmatter (MD) or `*.lattice.yaml` files
- **Locations**:
  - Lattice MDs: `what/lattices/lattice_*.md`
  - Lattice YAMLs: `what/lattices/**/*.lattice.yaml`, `how/campaigns/**/*.lattice.yaml`
- **Version gate**: Skip if `_migration_version: "lsu-1.0"` already present in MD frontmatter or YAML top-level
- **Pairing status** (from M01 audit):
  - **Paired (MD+YAML)**: 6 lattices — verify consistency, add missing fields
  - **MD-only**: 15 lattices — generate `.lattice.yaml` from MD frontmatter
  - **YAML-only**: 6 lattices — generate MD wrapper with extracted metadata

## Pre-Flight

1. [ ] Object file(s) exist and are readable
2. [ ] Current frontmatter/YAML parses without error
3. [ ] Object type is `lattice` (MD) or file extension is `.lattice.yaml`
4. [ ] Object is not locked by another migration (no `_migration_lock` field)
5. [ ] Compliance checker pre-migration score recorded
6. [ ] Pairing state identified (MD-only, YAML-only, or paired)

## Changes

| # | Field | Current | Target | Action | Judgment? |
|---|-------|---------|--------|--------|:---------:|
| 1 | `lattice_type` | may be non-canonical | Canonical enum: `pipeline`, `agent`, `context_graph`, `workflow`, `infrastructure`, `context_set`, `skill` | normalize | No — mechanical mapping |
| 2 | `execution.mode` | may be absent | `batch`, `streaming`, or `interactive` | add | Yes — read workflow description |
| 3 | `execution.tier` | may be absent | `L1`, `L2`, or `L3` | add | Yes — read resource requirements |
| 4 | `fair.keywords` | may be absent | ≥1 keyword array | add/enrich | Yes — read lattice description |
| 5 | `.lattice.yaml` | may be absent for MD docs | Generated companion OR verified existing | generate/verify | Yes — structure, modules, connections |
| 6 | `_migration_version` | absent | `"lsu-1.0"` | add | No |

### `lattice_type` Canonical Values

| Current | Canonical |
|---------|-----------|
| `pipeline`, `data_pipeline` | `pipeline` |
| `agent`, `agent_workflow` | `agent` |
| `context_graph`, `knowledge_graph` | `context_graph` |
| `workflow`, `process` | `workflow` |
| `infrastructure`, `infra` | `infrastructure` |
| `context_set` | `context_set` |
| `skill` | `skill` |

If `lattice_type` is absent, determine from content:
- Bio pipelines (protein design, screening) → `pipeline`
- Content workflows (LinkedIn, presentations) → `workflow`
- Research/discovery lattices → `context_graph`
- Network/infrastructure lattices → `infrastructure`

### `execution.mode` Guidance

- **`batch`**: Lattice runs as a complete job (most bio pipelines, content generation)
- **`streaming`**: Lattice processes continuous input (real-time monitoring, event processing)
- **`interactive`**: Lattice involves human-in-the-loop steps (coaching, review workflows)

Read the lattice description. Look for keywords: "pipeline" → batch, "real-time" → streaming, "interactive"/"review"/"coach" → interactive. Default to `batch` if unclear.

### `execution.tier` Guidance

- **`L1`**: Runs on edge devices / local machines (lightweight tools, small models)
- **`L2`**: Requires HPC / GPU cluster (protein folding, training, large inference)
- **`L3`**: Cloud-based execution (API-dependent, multi-node)

Read module references in the lattice. If it references GPU-heavy models (ESM, RFDiffusion) → `L2`. If it references APIs or cloud services → `L3`. If it's purely local/lightweight → `L1`. Default to `L2` for bio pipelines.

## Steps

### Step 1: Identify Pairing State

Determine which of three cases applies:

| Case | Condition | Action |
|------|-----------|--------|
| **A** | MD exists, no YAML | Upgrade MD frontmatter + generate `.lattice.yaml` |
| **B** | YAML exists, no MD | Generate MD wrapper + upgrade YAML |
| **C** | Both exist | Verify consistency + add missing fields to both |

### Step 2: Upgrade MD Frontmatter (Cases A and C)

#### 2a. Normalize `lattice_type`

If non-canonical or absent, set to canonical value per mapping table.

#### 2b. Add Execution Block

If no `execution:` block exists, add it:

```yaml
execution:
  mode: batch    # or streaming, interactive
  tier: L2       # or L1, L3
```

#### 2c. Add/Enrich FAIR Block

If no `fair:` block or missing fields:

```yaml
fair:
  keywords: ["keyword1", "keyword2"]
  license: "Apache-2.0"
```

**Keywords**: Read the lattice description. Extract 1-3 keywords:
- `lattice_protein_binder_design` → `["protein-design", "binder", "computational-biology"]`
- `lattice_linkedin_content` → `["content-generation", "linkedin", "social-media"]`
- `lattice_network_alpha` → `["network", "infrastructure", "monitoring"]`

#### 2d. Add Federation Stub

If no `federation:` block:

```yaml
federation:
  discoverable: true
```

### Step 3: Generate `.lattice.yaml` (Case A — MD-only)

Follow the 5-step companion generation process:

#### 3a. Extract

Pull from the MD frontmatter:
- `name` (from filename, e.g., `lattice_enzyme_design` → `enzyme_design`)
- `lattice_type` (from Step 2a)
- `version` (if present)
- Module references from body content (look for `[[module_*]]` wikilinks or module mentions)

#### 3b. Template

```yaml
# <lattice_name>.lattice.yaml
# Generated by migrate_object_lattice (lsu-1.0)
name: "<lattice_name>"
lattice_type: "<lattice_type>"
version: "<version or '0.1.0'>"

execution:
  mode: "<mode>"
  tier: "<tier>"

modules: []
  # Populate from MD body module references
  # - name: "<module_name>"
  #   ref: "module://<module_name>"

connections: []
  # Populate from MD body workflow description
  # - from: "<source_module>"
  #   to: "<target_module>"
  #   type: "<io_type>"

fair:
  keywords: []  # Copied from MD
  license: "Apache-2.0"

federation:
  discoverable: true

_migration_version: "lsu-1.0"
```

#### 3c. Judge

Agent reads the MD body to determine:
- **`modules`**: Extract module references from wikilinks, code blocks, or pipeline descriptions. Each module entry needs `name` and optionally `ref` (URI).
- **`connections`**: Extract data flow from the workflow description. Look for "→", "feeds into", "outputs to", step ordering.
- **`execution`**: Copy from MD frontmatter (Step 2b).

If modules/connections cannot be reliably determined, leave as empty arrays with comments indicating manual review needed.

#### 3d. Validate

Before writing, verify:
- YAML parses without error
- `name` matches the lattice name
- `lattice_type` matches MD frontmatter
- `federation.discoverable` is `true`

#### 3e. Write

Save as `what/lattices/<lattice_name>.lattice.yaml` alongside the MD.

### Step 4: Generate MD Wrapper (Case B — YAML-only)

For YAML lattices that have no corresponding MD file:

#### 4a. Extract from YAML

Read the `.lattice.yaml`. Extract: `name`, `lattice_type`, `version`, `modules`, `connections`, `fair`, `federation`.

#### 4b. Generate MD

```markdown
---
type: lattice
lattice_type: <lattice_type>
version: "<version>"
created: <today>
updated: <today>
status: active
last_edited_by: agent_init
execution:
  mode: <mode>
  tier: <tier>
fair:
  keywords: <keywords from YAML>
  license: "<license>"
federation:
  discoverable: true
tags: [lattice, <lattice_type>]
_migration_version: "lsu-1.0"
---

# <lattice_name>

<Brief description derived from YAML structure — modules used, workflow purpose.>

## Modules

<List modules from YAML with descriptions if available.>

## Workflow

<Describe the connection flow from YAML connections array.>

## Companion

Machine-readable specification: `<lattice_name>.lattice.yaml`
```

#### 4c. Write

Save as `what/lattices/lattice_<name>.md`. Naming convention: `lattice_<name>.md` alongside `<name>.lattice.yaml`.

### Step 5: Verify Consistency (Case C — Both Exist)

For lattices that already have both MD and YAML:

1. Compare `lattice_type` in both — if different, MD is authoritative
2. Compare `version` — if different, use the higher version
3. Check that modules listed in YAML are referenced in MD body
4. Add any missing fields to both (execution, FAIR, federation) using Steps 2-3 logic
5. Add `_migration_version: "lsu-1.0"` to both

### Step 6: Add Migration Version

Add to MD frontmatter (all cases):
```yaml
_migration_version: "lsu-1.0"
```

Add to YAML top-level (Cases A and C where YAML exists or was generated):
```yaml
_migration_version: "lsu-1.0"
```

### Step 7: Final Verification

Re-read all files (MD and YAML). Confirm:
- Both parse without error
- Fields are consistent between MD and YAML
- Body content in MD is unchanged (for existing MDs)
- Migration version present in all files

## Post-Flight

1. [ ] MD frontmatter parses as valid YAML without error
2. [ ] `lattice_type` uses canonical enum value
3. [ ] `execution.mode` present with valid value (`batch`, `streaming`, or `interactive`)
4. [ ] `execution.tier` present with valid value (`L1`, `L2`, or `L3`)
5. [ ] `fair.keywords` present with ≥1 keyword
6. [ ] `federation.discoverable: true` present
7. [ ] `_migration_version: "lsu-1.0"` present in MD (and YAML if applicable)
8. [ ] MD body content unchanged (for pre-existing MDs)
9. [ ] Companion `.lattice.yaml` validates — YAML parses, required fields present
10. [ ] MD wrapper validates — frontmatter parses, body has meaningful content (for generated MDs)
11. [ ] Paired lattices have consistent `lattice_type` and `version` between MD and YAML
12. [ ] Compliance score improved or unchanged vs pre-migration

## Rollback

- **L1** (single file): `git checkout -- <md_path>` and/or `rm <yaml_path>` (if companion was generated). For generated MDs (Case B), `rm <md_path>`.
- **L2** (field-level): Revert specific fields in MD frontmatter or YAML. Remove added `execution`, `fair`, `federation`, `_migration_version`.
- **L3** (batch): `git reset --hard <pre-migration-tag>` (e.g., `pre-lsu-m08`)

## Related

- [Migration Registry](AGENTS.md) — All available migrations
- Architecture Spec §4.4-§4.5 — Lattice prompt spec + companion generation (see operational vault campaign artifacts)
- Gap Register — G-002, G-013 (see operational vault campaign artifacts)
- YAML-MD Relationship Map — Pairing status for all 35 lattice objects (see operational vault campaign artifacts)
