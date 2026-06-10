---
type: skill
skill_type: agent
created: 2026-03-08
updated: 2026-05-18
status: active
category: development
trigger: When a lattice needs to be published to a registry, pulled from a registry, or composed with another lattice
last_edited_by: agent_stanley
tags: [skill, registry, federation, publish, lattice_object]

requirements:
  tools: [latlab CLI, lattice_validate.py]
  context: [what/lattices/examples/]
  permissions: [registry write access for publish]
---

# Skill: Lattice Publish

## Overview

Agent recipe for the publish/pull/compose workflow. Covers validating a lattice for federation readiness, publishing it to a registry, pulling published lattices, and composing lattices together.

> **Note**: This skill publishes a `.lattice.yaml` *object* to a registry via `latlab`. To publish a *vault* to its GitHub remote, see `skill_vault_publish.md`.

## Trigger

Invoke when:
- A lattice is ready for registry publication
- You need to pull a published lattice from a registry
- You need to compose two lattices together (inline or external pattern)

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `path` | string | Yes | — | Path to the `.lattice.yaml` file |
| `action` | enum | Yes | — | `publish`, `pull`, or `compose` |
| `registry` | string | No | local | Target registry (local or remote URL) |
| `dry_run` | bool | No | false | Preview without executing |

## Requirements

### Tools/APIs
- `latlab` CLI (provides `lattice publish`, `lattice pull`, `lattice compose`)
- `lattice_validate.py` or `latlab lattice validate` for pre-publish validation

### Context Files
- `how/templates/template_registry.md` — federation metadata reference
- `what/lattices/examples/` — example lattices for pattern reference

### Permissions
- Registry write access for `publish` operations
- Read access sufficient for `pull` and validation

## Implementation

### Step 1: Validate Lattice

Run structural and semantic validation:

```bash
# Validate the lattice file
cd ~/aDNA/lattice-protocol
python -c "
from objects.lattices.tools.lattice_validate import validate_lattice_file
result = validate_lattice_file('path/to/lattice.lattice.yaml')
print(f'Valid: {result.is_valid}')
for error in result.errors:
    print(f'  ERROR: {error}')
for warning in result.warnings:
    print(f'  WARN: {warning}')
"
```

### Step 2: Check Federation Readiness

Verify all 6 federation readiness checks pass:

```bash
cd ~/aDNA/lattice-protocol
python -c "
from objects.lattices.federation import check_federation_readiness
import yaml

with open('path/to/lattice.lattice.yaml') as f:
    data = yaml.safe_load(f)

result = check_federation_readiness(data)
print(f'Federation ready: {result.ready}')
for check in result.checks:
    status = 'PASS' if check.passed else 'FAIL'
    print(f'  [{status}] {check.name}: {check.message}')
"
```

The 6 checks are:
1. `federation.shareable` is `true`
2. `federation.source_instance` is set
3. `federation.version_policy` is set
4. `fair.license` is set
5. `fair.keywords` has entries
6. `lattice_type` is a valid discriminator

### Step 3: Publish

```bash
# Dry run first
latlab lattice publish path/to/lattice.lattice.yaml --dry-run

# Publish to local registry
latlab lattice publish path/to/lattice.lattice.yaml

# Publish to specific registry
latlab lattice publish path/to/lattice.lattice.yaml --registry <url>
```

### Step 4: Pull

```bash
# Pull a published lattice by name
latlab lattice pull protein_binder_design

# Pull a specific version
latlab lattice pull protein_binder_design --version 1.0.0
```

### Step 5: Compose

Compose two lattices together using inline or external patterns:

```bash
# External composition (lattices remain separate, connected by seam edges)
latlab lattice compose parent.lattice.yaml child.lattice.yaml \
  --pattern external \
  --seam-edges '[{"source": "parent_node", "target": "child_node", "data_mapping": [{"from": "output_field", "to": "input_field", "type": "pdb_file"}]}]'

# Inline composition (child nodes merged into parent)
latlab lattice compose parent.lattice.yaml child.lattice.yaml \
  --pattern inline \
  --seam-edges '[{"source": "parent_node", "target": "child_node", "data_mapping": [{"from": "output_field", "to": "input_field", "type": "pdb_file"}]}]'
```

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Published entry | Registry record | Lattice registered with metadata, version, and federation info |
| Pulled lattice | `.lattice.yaml` file | Local copy of a published lattice |
| Composed lattice | `.lattice.yaml` file | New lattice combining parent and child |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `ValidationError` | Lattice file has structural issues | Fix errors reported by `validate_lattice_file()` |
| `FederationNotReady` | Missing required federation/FAIR fields | Add missing fields per `template_registry.md` checklist |
| `RegistryNotFound` | Target registry unreachable | Check registry URL and network connectivity |
| `VersionConflict` | Lattice with same name+version already published | Bump version in lattice file |
| `CompositionError: incompatible types` | Seam edge data types don't match | Verify `data_mapping` types align between source output and target input |
| `CompositionError: missing node` | Referenced node not found in lattice | Check node names in `--seam-edges` match actual lattice nodes |

## Federation-Ready Examples

6 of 13 example lattices in `what/lattices/examples/` are federation-ready:

| Lattice | Type | Version Policy |
|---------|------|---------------|
| `protein_binder_design` | pipeline | minor |
| `composed_therapeutics` | pipeline | minor |
| `full_therapeutics` | pipeline | minor |
| `knowledge_base` | context_graph | minor |
| `docking_assessment` | pipeline | locked (extracted) |
| `binder_generation` | pipeline | locked (extracted) |

The remaining 7 (hello_world, learning_path, sales_pipeline, etc.) are instructional examples without federation blocks.

## Related

- **Vault publish (NEW v7.0)**: `how/skills/skill_vault_publish.md` — publish a *vault* to its GitHub remote (distinct from this registry-publish skill)
- **Git remote setup (NEW v7.0)**: `how/skills/skill_git_remote_setup.md` — first-time GitHub remote configuration
- **Publish tarball (NEW v7.0)**: `how/skills/skill_publish_tarball.md` — offline-shipping artifact for non-GitHub channels
- **Deploy hook (NEW v7.0)**: `how/skills/skill_deploy.md` — installs the pre-push sanitization hook (used by `skill_vault_publish`)
- **Publish-skill naming decision**: `what/decisions/adr_010_publish_skill_naming.md` — why these are separate skills
- **Registry template**: `how/templates/template_registry.md`
- **Lattice standard**: `what/lattices/standard_lattice.md`
- **Skills Protocol**: `how/skills/AGENTS.md`
- **Skill–Lattice Interop**: For publishing `lattice_type: skill` entries
