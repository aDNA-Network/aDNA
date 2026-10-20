---
type: profile_spec
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_edited_by: agent_{username}
status: draft            # draft → proposed → released (the steward's gates) · listed is the standard's act, recorded at what/docs/profiles/AGENTS.md
profile: <snake_case_name>
profile_version: 0.1.0
base_level: starter | standard | full
adna_conformance_declared: "<base_level>+<profile>"
steward: <Vault>.aDNA
upstream_pin: "aDNA-Network/aDNA@<commit> standard v<x.y>"
requirement_prefix: <PFX>          # e.g. MED — requirement IDs read <PFX>-<section>.<n>
data_tier_ceiling: GREEN | AMBER | RED    # optional — the highest data_tier the triad may carry (RED never appears as content)
tags: [profile_spec, profile, conformance]
---

# {Profile name} profile specification v{profile_version}

> **What this is.** A **profile** of the aDNA standard v{x.y}: a named, versioned overlay on the `{base_level}` level.
> It keeps every `{base_level}` MUST, adds its own, and relaxes none (standard §5.5, Profiles).
>
> **What this is not.** It is not a certification. Say plainly which reviews the profile is *designed for* and that
> a deployment is compliant only by its deployer's controls, never by this document.
>
> **Status.** {draft | proposed | released}. Nothing is ratified until the steward's humans sign (standard §7.7).

*How to use this template.* Keep every numbered section, and write "none, see upstream" where a section adds nothing,
so a reviewer can tell a deliberate silence from a forgotten one. The skeleton generalises the sections of the
first profile spec drafted against the standard (a medical profile). Field-specific sections (§7 in particular) are
where profiles differ most.

*Upstream.* The `<level>+<profile>` syntax (§5.5), release integrity (§15.5) and the purge carve-out (§15.1) cited
below are standard text from v2.6 (decision record: aDNA.aDNA ADR-066 clauses 1, 2 and 4b). A profile pinned to an
earlier standard cannot use them.

## 1. Scope and normative language

1.1 What the profile covers and what its launch scope excludes (excluded features return only as modules, §10).
1.2 Requirement keywords per RFC 2119. Every requirement carries an ID `{PFX}-<section>.<n>` so the validator, the
review checklist and findings can cite it.
1.3 **Silence and conflict.** Where this spec is silent, the pinned upstream standard applies. A profile never
relaxes a base MUST, so a conflict is a defect in the profile or an upstream candidate. Log it, never resolve it
silently.

## 2. Terms

| Term | Meaning |
|---|---|
| Profile · Release · Instance | as upstream §2, §5.5 and §15.5 |
| Profile surface | the files an instance inherits from the release, the scope of `instance_profile` (§11) |
| Work surface | the files the user and agent create |
| Module | a packaged add-back (§10) |
| *(field terms)* | |

## 3. Conformance: `{base_level}+{profile}`

3.1 `{PFX}-3.1` An instance MUST declare `adna_conformance: {base_level}+{profile}` and
`adna_profile_version: <semver>` in `MANIFEST.md`. *(A bare profile name with no level reads as no level upstream,
so the base-level half of the claim cannot be checked. Always write both halves.)*
3.2 **Relation to the base level.** The instance passes the upstream `{base_level}` validator unchanged. Say where
the profile is thinner in surface and where it is stricter in rules.
3.3 `{PFX}-3.3` The profile validator (§13) MUST exit 0. A failing check is non-conformance unless marked SHOULD.
3.4 Installing modules changes the `modules:` list, never the level.

## 4. Skeleton, governance set, size budgets

4.1 Required directories (and any base-level directory the profile keeps empty, with the reason).
4.2 Governance file set: N files, each named.
4.3 Size budgets per file and in total, with the counting method stated (`ceil(bytes/4)` for `token_estimate`,
upstream §5.5).
4.4 `MANIFEST.md` frontmatter fields the profile adds.

## 5. Frontmatter subset

5.1 Required fields per file class. Upstream §7.2 applies, and the profile may only add or narrow.
5.2 **`data_tier`** (GREEN ⊂ AMBER ⊂ RED; upstream §7.2 names the key and mints no values): optional upstream. The profile MAY make it MUST and MAY narrow it (state the ceiling). It is a label, never data.
5.3 Any field-specific label on a different axis carries the profile prefix (upstream §7.6 item 2). Do not mint a
bare base name.

## 6. Session model

What a session records, which upstream session features the profile trims, and the required body sections.

## 7. Data, models, egress, secrets, audit

7.1 Threat model (assets · actors · paths · mitigations).
7.2 Data classes and where each may live; what never enters the triad.
7.3 **Egress.** The default (state it), and how a module declares an exception. Every module that changes data
egress or model routing sits **inside** the `instance_profile` manifest scope (§11). Whatever default a profile ships
is then visible inside the hash-bound surface.
7.4 Pre-commit scan · 7.5 Secrets (by name only, broker-routed) · 7.6 Audit trail.
7.7 **Compliance map:** "designed for review under …", never "compliant with …".
7.8 **Purge.** Material that must not be present (secrets, RED or regulated data) is purged from tree and history,
leaving a payload-free incident record (upstream §15.1, purge exception).

## 8. Human-in-the-loop rule

Which actions need an explicit, displayed, recorded human yes, and the record's fields.

## 9. Errors and escalation

Tiers, what stops work, who is told.

## 10. Module interface

Descriptor fields (name · version · files · hashes · deps · what it adds back · re-validation cost) and how install
and uninstall change the manifest.

## 11. Release manifest

Follows the upstream §15.5 algorithm. **Do not restate it.** Cite it and fill in only
the profile's choices:

| Choice | This profile |
|---|---|
| `# profile:` / `# profile_version:` | |
| `# upstream:` | standard version + commit (= `upstream_pin`) |
| `# excluded:` data paths | |
| `instance_profile` scope: exact file list, or where it is defined | (MUST include governance files + every egress/model-routing module) |

The manifest root identifies the profile's **files**. An exchange's content address identifies a published
**package**. Never conflate the two.

## 12. Red-team record

Seed attacks, findings log, status per finding.

## 13. Validation pack

| Check | Requirement ID | What it verifies | Base-level or profile |
|---|---|---|---|
| V1 | | | |

Plus the per-file human review checklist, signed at one manifest root.

## 14. Versioning and upstream pin

14.1 Semver. A minor release never makes a conformant instance non-conformant (upstream §15.4 applied to the profile).
14.2 Release cut: spec `title` · `updated` · changelog line · MANIFEST `profile_version` · manifest header · manifest
`root` in the release notes. All must agree.
14.3 Rebasing onto a newer upstream is a profile release with its own review delta, never a silent pull.
14.4 **Listing.** On release, the steward asks the standard's maintainer for a row in the standard's
`what/docs/profiles/AGENTS.md` (see `CONTRIBUTING.md`). Listing certifies nothing.

## 15. Requirements traceability

| Requirement source | Where satisfied |
|---|---|

## 16. Open questions and upstream candidates

Each candidate gets an ID, the upstream section it touches, and a proposed disposition. These go to the standard's
maintainer as proposals (`CONTRIBUTING.md`), never as silent local edits.

## Related

`what/docs/adna_standard.md` §5.5 (Profiles) · §15.5 (Release Integrity) · `what/docs/profiles/AGENTS.md` (the
listed-profile table)
