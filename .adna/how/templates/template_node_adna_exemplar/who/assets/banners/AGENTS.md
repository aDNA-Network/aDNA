---
type: directory_index
created: 2026-06-01
updated: 2026-06-01
last_edited_by: agent_hestia
tags: [directory_index, assets, banners, node_adna, exemplar]
---

# who/assets/banners/ — Node HOME hero banner(s).

**Naming**: `banner_<name>.jpg` (~1920×400)

**Consumed by**: `HOME.md` `feature:` + the `.banner-{{persona_lower}}` block

Image binaries are not bundled in the template (operator supplies real assets at bootstrap, or generates them via the node's imagery pipeline). The asset registry (`who/assets/asset_registry.yaml`) tracks which images are live / superseded / skipped.
