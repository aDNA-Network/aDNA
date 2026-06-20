---
type: directory_index
created: 2026-06-01
updated: 2026-06-01
last_edited_by: agent_hestia
tags: [directory_index, curation, node_adna, exemplar]
---

# who/curation/ — Per-Vault Curation Cards (generated)

One curation card per installed vault, the single source of truth for the §Gallery. Each is a pair:
`curation_<Vault>.aDNA.yaml` (structured, editable) + `.md` (rendered). **Generated** by `what/code/build_curation_cards.py` from `inventory_vaults.yaml` + each vault's MANIFEST/STATE + the node's vault-card images/portraits — do not hand-edit the cards; edit upstreams + rebuild:

```bash
python what/code/build_curation_cards.py            # all live vaults
python what/code/build_curation_cards.py --only Foo.aDNA  # one vault
python what/code/build_curation_cards.py --check          # validate, no write
```

Schema + the class→archetype / health→status derivation maps: `curation_schema.yaml`. `operator_note` is the only field permitting non-upstream editorial text. On a vault **rename**, rebuild the new card and delete the orphaned old one (see `skill_inventory_refresh.md` Step 9.5).
