---
type: context
title: "aDNA Standard Governance Model"
created: 2026-03-20
updated: 2026-03-20
last_edited_by: agent_init
status: approved
tags: [context, governance, standard, stewardship, release-cadence]
---

# aDNA Standard Governance Model

> How the aDNA standard evolves: stewardship, release cadence, backwards compatibility, and the process for proposing changes.

---

## Stewardship

### Founding Architect Model

The aDNA standard is currently governed under a **Founding Architect** stewardship model:

- **Steward**: The Founding Architect (FA) holds decision authority over standard changes
- **Scope**: All normative changes to `adna_standard.md`, conformance level definitions, and governance file requirements
- **Authority transfer**: The FA may delegate stewardship to a **Standard Council** (3+ members) as the community grows. This transition is a governance decision, not a standard version change

### Community Input

- Anyone may propose standard changes via the process defined below
- The FA reviews all proposals and provides written rationale for acceptance or rejection
- Community feedback is gathered via GitHub Issues on the aDNA repository

---

## Release Cadence

| Track | Cadence | Scope |
|-------|---------|-------|
| **Standard** (`adna_standard.md` version) | As needed, estimated quarterly | Normative specification changes — conformance levels, required files, naming rules |
| **Governance** (`CLAUDE.md` version, `CHANGELOG.md`) | Continuous | Operational changes — protocols, templates, skills, tooling |

### Version Numbering

Both tracks use `Major.Minor` versioning:

- **Major** (e.g., v2.x → v3.0): May introduce breaking changes. Requires migration guidance.
- **Minor** (e.g., v2.1 → v2.2): Additive only. MUST NOT invalidate conformant instances.

See `adna_standard.md` §15.4 for the normative backwards compatibility promise.

---

## Backwards Compatibility Promise

This promise is normative (defined in `adna_standard.md` §15.4):

1. **Minor standard versions** MUST NOT invalidate conformant instances. An instance passing Starter/Standard/Full conformance at v2.1 MUST still pass at v2.2.
2. **Major standard versions** MAY introduce breaking changes. When they do:
   - Migration guidance MUST be published before or alongside the release
   - A migration tool or checklist SHOULD be provided
   - The previous major version MUST remain documented for reference
3. **Governance version changes** do not affect standard conformance. A CLAUDE.md update from v5.5 to v6.0 does not require instance changes.

---

## Proposing Standard Changes

### Lightweight RFC Process

1. **Open a GitHub Issue** with the `standard-change` label
2. **Describe**: What you want to change, why, and the impact on existing conformant instances
3. **Classification**: Is this a minor (additive) or major (breaking) change?
4. **Discussion**: Community and FA discuss in the issue
5. **Decision**: FA accepts, modifies, or declines with written rationale
6. **Implementation**: Accepted changes are incorporated into the next standard release

### Change Classification

| Type | Examples | Standard Version Impact |
|------|----------|------------------------|
| **Additive** | New optional field, new conformance check, new appendix | Minor bump (v2.2 → v2.3) |
| **Normative tightening** | SHOULD → MUST for existing recommendation | Major bump (v2.x → v3.0) |
| **Structural** | New required governance file, directory rename | Major bump |
| **Editorial** | Typo fixes, clarifications that don't change requirements | No version bump |

---

## Pre-Release Checklist

Before releasing a new standard version:

- [ ] All normative changes reviewed by FA
- [ ] Backwards compatibility verified for minor versions
- [ ] Migration guidance prepared for major versions
- [ ] `governance_sync_check.sh` reports zero drift
- [ ] `adna_validate.py` passes on the reference instance (adna repo)
- [ ] Example projects still pass their expected conformance level
- [ ] CHANGELOG.md updated with release entry
- [ ] Version strings updated in `adna_standard.md`, `README.md`

---

## Future Governance Evolution

As the aDNA community grows, governance may evolve:

1. **Standard Council** (3-5 members) — shared stewardship with majority vote
2. **Working Groups** — domain-specific groups (e.g., Bio-aDNA, Enterprise-aDNA) that propose extensions
3. **Formal RFC process** — structured proposal documents with review periods

These transitions are human-gated decisions, not automatic thresholds.
