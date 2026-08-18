---
name: Change proposal (improve the standard)
about: Propose a framework-level change or addition to the aDNA standard, template, or a reusable pattern/skill
title: "Proposal: <short description>"
labels: enhancement, proposal
assignees: ''
---

<!--
This is how you propose a change to the aDNA standard itself — a new/edited template field, a pattern, a skill,
a naming or convention change, a governance rule, or anything that would help people using aDNA on *other*
projects (not a fix to one specific vault).

If you are already working inside an aDNA vault, an agent can file this for you via the
`skill_upstream_contribution` recipe (it creates a `how/backlog/idea_upstream_<slug>.md` in your own vault and,
with your approval, opens this issue). This template mirrors that flow so both routes land the same shape.

The standard is authored by agents but *ratified by humans* (governance §7.7): proposals are evaluated, and
accepted ones are batched into a governance release (v8.x) or, if normative, a standard window (v2.x → v2.x+1).
-->

## Observation

What you noticed — the gap, friction, or missing capability. Be specific and reproducible.

## Context

What were you doing when you noticed it? (A proposal grounded in real use is far stronger than a hypothetical.)

## Suggested improvement

What the change or addition would look like. If you can, name whether it is:

- **Template / governance layer** (a template field, skill, doctrine, tooling — ships in a governance release), or
- **Normative / standard layer** (a base entity type, ontology, or conformance rule — needs a standard window).

## Affected files (if known)

Which files in the standard (`aDNA-Network/aDNA`), the template (`.adna/`), or the tooling would change.

## Who benefits

The framework-level test: would this help someone using aDNA on a completely different project? Say how.

## Prior art / links

Existing ADRs, patterns, discussions, or an `idea_upstream_` backlog file if one already exists.
