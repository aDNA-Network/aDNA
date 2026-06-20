---
type: directory_index
created: 2026-06-01
updated: 2026-06-01
last_edited_by: agent_hestia
tags: [directory_index, assets, portraits, node_adna, exemplar]
---

# who/assets/portraits/ — Persona portrait images (this node's persona + any sibling personae depicted).

**Naming**: `portrait_<persona>.jpg`

**Consumed by**: curation cards `persona_portrait:` + §Gallery portrait insets

Image binaries are not bundled in the template (operator supplies real assets at bootstrap, or generates them via the node's imagery pipeline). The asset registry (`who/assets/asset_registry.yaml`) tracks which images are live / superseded / skipped.
