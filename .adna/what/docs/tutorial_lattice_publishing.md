# Tutorial: Lattice Publishing Lifecycle

A step-by-step walkthrough of creating, validating, publishing, pulling, and composing a lattice — using the BrandDoctor marketing strategy lattice as the running example.

## Prerequisites

- An aDNA vault (cloned from [LatticeProtocol/Agentic-DNA](https://github.com/LatticeProtocol/adna))
- `lattice-protocol` repo available at `~/aDNA/lattice-protocol/`
- Python 3.10+ with `pyyaml` installed
- `latlab` CLI installed (`pip install lattice-protocol`)

## 1. Create a Lattice

Start from the registry template at `how/templates/template_registry.md` and fill in the four key sections: metadata, nodes, edges, and federation.

Create a new file at `what/lattices/examples/brand_doctor.lattice.yaml`:

```yaml
lattice:
  name: brand_doctor
  version: "1.0.0"
  lattice_type: pipeline
  description: >
    End-to-end brand strategy pipeline from brand audit through competitive
    analysis, positioning, messaging, visual identity, and content strategy.
  execution:
    mode: hybrid          # Mix of process nodes and LLM reasoning
    runtime: local        # Runs on L1 (laptop/edge)
    tier: L1
  nodes:
    - id: brand_audit
      type: dataset
      description: "Brand assets, metrics, customer perception data"
    - id: competitor_analysis
      type: process
      description: "Market landscape, competitor positioning"
    - id: positioning
      type: reasoning
      prompt: "Given the brand audit {brand_audit_summary} and competitive
        analysis {competitor_landscape}, identify the strongest positioning
        opportunity and produce a positioning statement."
      description: "LLM synthesizes audit + competitive data into positioning"
    - id: messaging_framework
      type: reasoning
      prompt: "Using the positioning statement {positioning_statement},
        generate taglines, value propositions, and an elevator pitch."
      description: "LLM generates messaging assets"
    - id: visual_identity_spec
      type: process
      description: "Color palette, typography, logo usage guidelines"
    - id: content_strategy
      type: process
      description: "Content calendar, channel strategy, tone guidelines"
  edges:
    - from: brand_audit
      to: competitor_analysis
      label: "brand context"
      data_mapping:
        brand_summary: market_context
    - from: brand_audit
      to: positioning
      label: "audit findings"
      data_mapping:
        audit_report: brand_audit_summary
    - from: competitor_analysis
      to: positioning
      label: "competitive landscape"
      data_mapping:
        competitor_report: competitor_landscape
    - from: positioning
      to: messaging_framework
      label: "strategic platform"
      data_mapping:
        positioning_statement: positioning_statement
        platform: strategic_platform
    - from: messaging_framework
      to: visual_identity_spec
      label: "brand voice"
      data_mapping:
        taglines: headline_candidates
        tone: brand_tone
    - from: messaging_framework
      to: content_strategy
      label: "messaging assets"
      data_mapping:
        value_props: content_themes
        audience_segments: target_audiences
  fair:
    license: "MIT"
    creators:
      - "Lattice Labs"
    keywords:
      - brand strategy
      - marketing
      - positioning
    provenance: "Marketing/brand strategy pipeline demonstrating domain-agnostic
      lattice composition"
  federation:
    shareable: true
    source_instance: adna
    version_policy: minor
```

### Key Design Choices

- **`lattice_type: pipeline`** — a deterministic DAG of nodes. Other options: `agent`, `context_graph`, `workflow`, `skill`.
- **`execution.mode: hybrid`** — mixes `process` nodes (human/tool steps) with `reasoning` nodes (LLM calls). Pure-compute lattices use `workflow`.
- **`reasoning` nodes** include a `prompt:` field with placeholder variables that map to incoming edge `data_mapping` values.
- **`data_mapping`** on edges defines how outputs from the source node map to inputs on the target node.
- **`federation`** block with `shareable: true` marks this lattice as ready for registry publication.

## 2. Validate

Run the schema validator to check structural integrity:

```bash
cd ~/aDNA/lattice-protocol-repo
python -c "
from objects.lattices.tools.lattice_validate import validate_lattice_file

result = validate_lattice_file('path/to/brand_doctor.lattice.yaml')
print(f'Valid: {result.valid}')
for error in result.errors:
    print(f'  ERROR: {error}')
for warning in result.warnings:
    print(f'  WARN:  {warning}')
"
```

Expected output:

```
Valid: True
```

No errors means the lattice passes all structural checks: required fields present, valid enum values, node IDs unique, edge references resolve, FAIR metadata complete.

## 3. Check Federation Readiness

Federation readiness is a stricter check — 6 criteria must pass before a lattice can be published:

```bash
cd ~/aDNA/lattice-protocol-repo
python -c "
from objects.lattices.federation import check_federation_readiness
import yaml

with open('path/to/brand_doctor.lattice.yaml') as f:
    data = yaml.safe_load(f)

result = check_federation_readiness(data)
print(f'Federation ready: {result.ready}')
for check_name, passed in result.checks.items():
    status = 'PASS' if passed else 'FAIL'
    print(f'  [{status}] {check_name}')
"
```

Expected output:

```
Federation ready: True
  [PASS] schema
  [PASS] shareable
  [PASS] source_instance
  [PASS] license
  [PASS] keywords
  [PASS] refs
```

### The 6 Federation Readiness Checks

| # | Check | What It Verifies |
|---|-------|-----------------|
| 1 | `schema` | All required fields present (name, version, description, execution, nodes, edges, fair) |
| 2 | `shareable` | `federation.shareable` is `true` |
| 3 | `source_instance` | `federation.source_instance` is set (identifies the publishing vault) |
| 4 | `license` | `fair.license` is declared (SPDX identifier) |
| 5 | `keywords` | `fair.keywords` has at least 1 entry |
| 6 | `refs` | All node `ref` fields resolve or use `lattice://` URIs |

## 4. Publish

Publish the lattice to the local registry:

```bash
# Preview what will be published (no side effects)
latlab lattice publish brand_doctor.lattice.yaml --dry-run

# Publish to local registry
latlab lattice publish brand_doctor.lattice.yaml
```

Dry-run output:

```
Dry run — would publish:
  Name:         brand_doctor
  Version:      1.0.0
  Type:         pipeline
  Path:         /path/to/brand_doctor.lattice.yaml
  License:      MIT
  Keywords:     brand strategy, marketing, positioning
```

Publish output:

```
Published 'brand_doctor' v1.0.0
  Registry ID:  <generated-id>
  Type:         pipeline
  License:      MIT
```

The publish command internally runs federation readiness checks and an export validation before registering the lattice.

## 5. Pull

Pull a published lattice from the registry:

```bash
# Pull to current directory
latlab lattice pull brand_doctor

# Pull to a specific directory
latlab lattice pull brand_doctor --output-dir ./lattices/

# JSON output for scripting
latlab lattice pull brand_doctor --json
```

Expected output:

```
Pulled 'brand_doctor'
  Saved to: /path/to/brand_doctor.lattice.yaml
```

The pulled lattice is a copy of the published file. Federation provenance (import date, source instance, checksum) is recorded in the federation block.

## 6. Compose

Compose two lattices together. This example connects the BrandDoctor lattice to the protein binder design lattice using the external reference pattern — demonstrating cross-domain composition.

```bash
latlab lattice compose \
  protein_binder_design.lattice.yaml \
  brand_doctor.lattice.yaml \
  --pattern external \
  --seam-edges '[{
    "from_node": "ranking",
    "to_node": "brand_doctor",
    "label": "candidate branding",
    "data_mapping": {"top_candidates": "brand_audit_summary"}
  }]'
```

Expected output:

```
Composed (external pattern)
  Output:   composed_protein_binder_design.lattice.yaml
  Nodes:    7   (6 original + 1 opaque brand_doctor node)
  Edges:    8   (7 original + 1 seam edge)
```

### Two Composition Patterns

| Pattern | Mechanism | Result | Use When |
|---------|-----------|--------|----------|
| **External** | Child becomes a single opaque `lattice://` node | Parent + 1 node | Black-box composition — child internals hidden |
| **Inline** | Child nodes merge into parent with `{child_name}_` prefix | Parent + N child nodes | Need fine-grained access to child nodes |

For inline composition:

```bash
latlab lattice compose \
  protein_binder_design.lattice.yaml \
  brand_doctor.lattice.yaml \
  --pattern inline \
  --seam-edges '[{
    "from_node": "ranking",
    "to_node": "brand_audit",
    "label": "candidate branding",
    "data_mapping": {"top_candidates": "brand_summary"}
  }]'
```

With inline, child node IDs are prefixed: `brand_doctor_brand_audit`, `brand_doctor_positioning`, etc.

## 7. Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|------------|
| `ValidationError` | Lattice file has structural issues | Fix errors from `validate_lattice_file()` — check required fields, enum values, node ID format |
| `federation.shareable must be true` | Missing or false `federation.shareable` | Add `federation:` block with `shareable: true` |
| `federation.source_instance must be set` | No source instance identifier | Add `source_instance: adna` (or your vault name) to federation block |
| `fair.license must be declared` | Missing license | Add `fair.license: "MIT"` (or appropriate SPDX identifier) |
| `Node ID collision after namespace prefixing` | Inline compose: prefixed child ID matches a parent ID | Rename conflicting node in parent or child |
| `Seam edge from 'X': node not found` | Seam edge references a non-existent node | Check node names — for external pattern, use child lattice *name*; for inline, use original child node IDs |
| `No lattice found matching 'X'` | Lattice not yet published | Publish first with `latlab lattice publish` |

For the full agent workflow, see `how/skills/skill_lattice_publish.md`.

## 8. Key Concepts

**Federation**
The lifecycle of sharing lattices across instances: validate → export → share → import → compose. A lattice must pass 6 readiness checks before it can be published.

**FAIR Metadata**
Findable, Accessible, Interoperable, Reusable. Every published lattice requires at minimum a `license` and `keywords`. Full FAIR includes `creators`, `provenance`, and an optional `identifier` (DOI).

**Composition Patterns**
Two ways to combine lattices: *inline* merges child nodes into the parent (namespace-prefixed), *external* adds the child as a single opaque reference node with a `lattice://` URI.

**Lattice Types**
Five discriminator values: `pipeline` (deterministic DAG), `agent` (LLM-driven), `context_graph` (knowledge structure), `workflow` (operational process), `skill` (encapsulated agent capability).

**Seam Edges**
Edges that connect parent and child lattices at composition boundaries. Each seam edge requires `from_node`, `to_node`, and `data_mapping` to define how data flows across the boundary.

**Version Policy**
Controls how downstream consumers receive updates: `minor` (auto-receive patch/minor), `locked` (pinned to exact version), `latest` (always latest).

**Lattice URI**
The addressing scheme for federated lattices: `lattice://<instance_id>/<lattice_name>[/<node_id>]`. Used in external composition and cross-instance references.
