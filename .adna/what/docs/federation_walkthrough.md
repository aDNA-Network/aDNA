---
type: context
title: "Federation Walkthrough — Two aDNA Instances Exchanging a Lattice"
created: 2026-03-20
updated: 2026-03-20
last_edited_by: agent_init
status: approved
tags: [context, federation, walkthrough, interop]
---

# Federation Walkthrough

> A step-by-step demonstration of two aDNA instances exchanging a lattice artifact via the federation protocol.

## Scenario

**Instance A** (`biotech-lab`) has built a `protein_folding` lattice. **Instance B** (`enterprise-pipeline`) wants to compose it into a larger `drug_discovery` workflow.

This walkthrough uses the example projects in `what/docs/examples/adna-projects/`.

---

## Step 1: Verify Federation Readiness (Instance A)

Before exporting, check the 6 federation readiness criteria (per `lattice_federation.md` §2.3):

```bash
# From instance A root
python what/lattices/tools/adna_validate.py . --verbose
# Expect: Standard or Full conformance
```

Federation readiness requires:
1. Lattice YAML validates against schema
2. All module references resolve within the instance
3. I/O types use canonical vocabulary
4. Version metadata present in frontmatter
5. FAIR metadata block exists (keywords + license)
6. No circular dependencies in the lattice graph

## Step 2: Export with lattice:// URIs (Instance A)

The `lattice://` URI scheme uniquely identifies artifacts across instances:

```
lattice://biotech-lab/what/lattices/protein_folding.lattice.yaml
```

Structure: `lattice://<instance-id>/<path-from-root>`

Create a federation manifest for the artifact:

```yaml
# what/lattices/exports/protein_folding_export.yaml
federation:
  source_instance: biotech-lab
  source_uri: lattice://biotech-lab/what/lattices/protein_folding.lattice.yaml
  version: "1.0"
  version_policy: locked    # locked | patch | minor | latest
  exported: 2026-03-20
  checksum: sha256:abc123...
  dependencies:
    - lattice://biotech-lab/what/modules/esm2_embedding.md
    - lattice://biotech-lab/what/modules/esmfold_predict.md
  fair:
    keywords: [protein-folding, esm2, structural-biology]
    license: Apache-2.0
```

## Step 3: Share the Artifact

Transfer happens via any transport mechanism — Git submodule, file copy, API push, or package registry. The federation protocol is transport-agnostic.

```bash
# Simple file-based share
cp -r instance-a/what/lattices/protein_folding* /shared/federation-inbox/
cp instance-a/what/lattices/exports/protein_folding_export.yaml /shared/federation-inbox/
```

## Step 4: Import into Instance B

Instance B creates a reference to the external lattice:

```yaml
# what/lattices/imports/protein_folding_ref.md
---
type: lattice_ref
title: "Protein Folding (from biotech-lab)"
source_uri: lattice://biotech-lab/what/lattices/protein_folding.lattice.yaml
version_policy: locked
version: "1.0"
imported: 2026-03-20
created: 2026-03-20
updated: 2026-03-20
last_edited_by: agent_init
tags: [lattice_ref, federation, import, protein-folding]
---

# Imported Lattice: Protein Folding

**Source**: biotech-lab instance
**URI**: `lattice://biotech-lab/what/lattices/protein_folding.lattice.yaml`
**Version policy**: locked at v1.0

## Usage

Reference this lattice in compositions using the `lattice://` URI.
```

## Step 5: Compose in Instance B

Instance B's `drug_discovery` lattice references the imported artifact:

```yaml
# drug_discovery.lattice.yaml (Instance B)
lattice:
  name: drug_discovery_pipeline
  version: "1.0"
  nodes:
    - id: target_selection
      module: what/modules/target_selector.md
    - id: protein_structure
      module: lattice://biotech-lab/what/lattices/protein_folding.lattice.yaml
      version_policy: locked
    - id: binding_analysis
      module: what/modules/binding_predictor.md
  edges:
    - from: target_selection
      to: protein_structure
      type: protein_sequence → protein_sequence
    - from: protein_structure
      to: binding_analysis
      type: protein_structure → protein_structure
```

## Step 6: Ontology Merge

When Instance B imports from Instance A, their ontologies compose. Per `ontology_unification.md`:

- **Base types** (module, dataset, lattice, session, mission, etc.) are shared — no merge needed
- **Extension types** (`bio_target`, `crm_deal`) use namespace prefixes — no conflict
- **Conflict resolution**: If both instances define the same extension type differently, the importing instance's definition takes precedence locally

## Verification

After completing the walkthrough:

1. Instance A's lattice validates: `python adna_validate.py .`
2. Instance B can resolve the `lattice://` URI to a concrete file path
3. The composed lattice graph has no broken references
4. Ontology merge produces no conflicts (different namespaces)

---

## Key Concepts Demonstrated

| Concept | Where |
|---------|-------|
| Federation readiness criteria | Step 1 |
| `lattice://` URI scheme | Step 2 |
| Transport-agnostic sharing | Step 3 |
| Import reference pattern | Step 4 |
| Cross-instance composition | Step 5 |
| Ontology merge algorithm | Step 6 |

## Related Docs

- `lattice_federation.md` — Full federation protocol specification
- `lattice_interop.md` — Breaking vs non-breaking change classification
- `ontology_unification.md` — Merge algorithm and namespace rules
- `adna_bridge_patterns.md` — Composition patterns (nesting, sibling, monorepo)
