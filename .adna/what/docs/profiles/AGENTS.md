---
type: directory_index
created: 2026-10-19
updated: 2026-10-20
status: active
last_edited_by: agent_rosetta
tags: [directory_index, docs, profiles, conformance]
token_estimate: ~800
---

# what/docs/profiles/: the list of named conformance profiles

> **In one sentence:** this directory is a **list, not a library**. It records which named profiles of the aDNA
> standard exist, who looks after each one, and how to check that a copy is unmodified. The profiles themselves live
> with their stewards.

## Purpose

**For a newcomer.** The aDNA standard has conformance levels (Starter, Standard, Full) that say how much of the
standard a graph uses. A **profile** is a named set of extra rules that a field (medicine, for example) adds on top of
one level. It can add rules and never remove one. A clinic's graph can say "I am Starter, plus the medical rules" and a
checker can test both halves. This page is where the standard writes down that such a profile exists.

**For a developer.** Standard §5.5 (Profiles, v2.6): a profile is a named, versioned overlay on exactly one
conformance level, declared as `adna_conformance: <level>+<profile>` with `adna_profile_version: <semver>` in
`MANIFEST.md`. It keeps every base MUST, may add MUSTs and SHOULDs, and never relaxes a base MUST. A validator that does
not know the profile evaluates the base level and reports the profile as **unverified**, never failed. "Official"
means **listed here**, not hosted here.

*Self-reference:* this file shows the rule it states. It holds names, pointers and one hash per row. It holds no rules
of any profile. Compare `what/docs/adna_standard.md` one directory up, which does hold the standard's own text: the
standard travels with this template, and a profile travels with its steward.

## The rule for this directory

| This directory holds | It never holds |
|---|---|
| the listed-profile table below | a steward's profile text, rules or tools |
| this `AGENTS.md` | copies of a profile's release bytes |
| pointers (steward graph, spec path, release manifest root) | any certification, endorsement or compliance claim |

Listing is a §7.7 act of the standard's maintainer at the steward's request. **Listing certifies nothing.** It records
that a profile exists and how to check a copy against its release manifest (§15.5), not that the profile is safe,
sufficient or compliant. Distribution is the steward's.

## Listed profiles

| Profile | Base level | Steward | Current version | Spec (at the steward) | Release manifest root | Listed | Tense |
|---|---|---|---|---|---|---|---|
| *(none listed yet)* | | | | | | | |

### Expected (not yet listed)

| Profile | Base level | Where it stands | Lists when | Tense |
|---|---|---|---|---|
| `medical` (aDNA-Medical) | `starter` (declared `starter+medical`) | spec in draft at its steward | the steward's release, on the steward's request | `HORIZON` |

A row moves from *Expected* to *Listed* only with all four filled: steward, a released version, a spec path at the
steward, and that release's manifest root. Each move carries its own §7.7 line, recorded in the row's `Listed` cell.

## How to add a profile (for a steward)

1. Write the profile spec in **your own** graph. `how/templates/template_profile_spec.md` is the skeleton.
2. Cut a release with `manifest_sha256.txt` at its root (the §15.5 algorithm).
3. Ask the standard's maintainer for listing (see `CONTRIBUTING.md`), with name · base level · version · spec path ·
   manifest root.
4. The maintainer checks the four fields, puts the row to a §7.7 line, and adds it to the standard's copy of this
   file. Nothing of yours is copied in.

## Load/Skip Decision

**Load** when declaring, checking or listing a profile, or answering "is profile X official?". **Skip** for ordinary
graph work at a base level. Nothing here changes what Starter, Standard or Full require.

## Related

`what/docs/adna_standard.md` §5.5 (Profiles) · §15.5 (Release Integrity) · `how/templates/template_profile_spec.md` ·
`what/docs/AGENTS.md` (parent index)
