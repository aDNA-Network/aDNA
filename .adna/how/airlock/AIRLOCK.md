---
type: airlock
title: "aDNA Template Airlock Entry Point"
status: inactive  # forked vaults flip to `active` to opt in to cross-vault traffic
version: "0.1.0"  # template stub version; advances when this file's shape (not III's spec) changes
created: 2026-05-11
updated: 2026-05-11
last_edited_by: agent_stanley
federation_ref:
  source: "III.aDNA/what/artifacts/iii_airlock_standard_spec.md"
  version: "0.2.0"
  pinned_at: 2026-05-11
authoring_adr: "what/decisions/adr_008_airlock_template_stub.md"  # ADR-008 (status: proposed; ratifies at M03 phase gate Session 3)
tags: [airlock, template, federation_ref, iii_aDNA, opt_in, cross_vault_traffic]
---

# aDNA Template Airlock — Entry Point (template stub)

> **Status: inactive.** This file ships in the aDNA template as an opt-in entry point
> for cross-vault traffic. A fresh fork inherits it unmodified. To **activate** for
> cross-vault traffic, flip the frontmatter `status: inactive → active` and follow
> the §Activation steps below.

## What is the airlock?

The airlock is the aDNA standard for **vault-to-vault traffic** — the contract that
governs how agents and artifacts cross context-graph boundaries between aDNA vaults.

Two surfaces:

- **Entry paths** — inbound, pull-based. An external agent enters this vault to do
  localized work (e.g., run a quality-improvement loop) using this vault's own context.
- **Cross-vault requests** — bidirectional, ephemeral. An agent in vault A commissions
  an agent in this vault to do work for vault A, with a handshake + memo lifecycle.

## Federation source

This stub federates to the **III.aDNA Airlock Standard** at the version pinned in
frontmatter. III is the canonical implementer; this template ships only the entry-point
file. For the full schema (the 5 canonical entry paths + cross-vault request patterns +
handshake profiles + payload contract + secret-delegation rules + idempotency keys), read:

- `~/aDNA/III.aDNA/what/artifacts/iii_airlock_standard_spec.md` (the spec)
- `~/aDNA/III.aDNA/how/airlock/AIRLOCK.md` (the reference instance)

Worked example (bilateral commission across vaults):

- `~/aDNA/CanvasForge.aDNA/who/coordination/coord_2026_05_08_videoforge_requests_carly_herb_deck.md`

Multilateral example (17 parallel relationships from `aDNA.aDNA/`):

- `~/aDNA/aDNA.aDNA/who/coordination/coord_2026_05_09_v7_*.md`

## Why opt-in?

Not every aDNA vault participates in cross-vault traffic. A vault that operates entirely
locally — generating site content, running a single-domain pipeline, hosting a knowledge
base — has no need for the airlock surface. The template ships the entry point so that
**adopting the airlock is content-only**, not a structural decision. Vaults that need
the surface flip a frontmatter field; vaults that don't, ignore the file.

## Activation steps

1. Flip the frontmatter `status: inactive → active` in this file.
2. Decide which entry paths your vault supports. The 5 III canonical paths are a starting
   point; your vault may add domain-specific paths (e.g., a SiteForge vault adds a Path B'
   for web-review specifics; a VideoForge vault inherits ADR-006 operation-catalog dispatch
   for Path D').
3. Author your vault's coordination directory (`who/coordination/`) if not present.
4. Reference this file from your vault's `CLAUDE.md` so arriving agents discover it.
5. For ecosystem-wide rollout discipline, see the v3 successor campaign:
   `~/aDNA/aDNA.aDNA/how/campaigns/campaign_adna_v3_ecosystem_compliance/`
   (mission `M05-EC` drives ecosystem-wide airlock adoption with the per-vault content
   template from
   `aDNA.aDNA/how/campaigns/campaign_adna_v2_infrastructure/missions/artifacts/m01_obj8_per_vault_coord_memo_template.md`).

## Version pinning + updates

The frontmatter `federation_ref.version` field pins to a specific III spec version
(currently v0.2.0). When III publishes a minor or major bump, consumers review per
the III ADR-002 §3 consumer contract. The aDNA template's pin is updated by a future
mission in the v7.x or v8.x track (the same M03-class mission that performs the next
round of template-level governance).

## Cross-references

- `~/aDNA/aDNA.aDNA/what/decisions/adr_008_airlock_template_stub.md` — this stub's
  authoring ADR + decision rationale + minimal-stub posture justification
- III.aDNA airlock canonical (federation source) — see §Federation source above
- v3 successor campaign + `M05-EC` mission — see §Activation steps above

---

**Status block**: stub authored M03 Session 2 2026-05-11; status: inactive by default;
activation is operator-discretionary; v3-EC M05-EC drives ecosystem-wide adoption.
