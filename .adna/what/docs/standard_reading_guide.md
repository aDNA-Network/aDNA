---
type: context
title: "aDNA Standard Reading Guide"
created: 2026-03-19
updated: 2026-03-19
status: active
last_edited_by: agent_init
tags: [adna, standard, reading-guide, navigation]
token_estimate: 3000
---

# aDNA Standard Reading Guide

The [aDNA Universal Standard](adna_standard.md) is 1,336 lines. You don't need all of them. This guide maps three reading paths by what you're trying to do, provides a section-by-section table of contents, and disambiguates the skill/lattice dual identity.

---

## 1. Reading Paths

Three personas, three curated paths through the standard:

| Persona | Goal | Sections to read | ~Lines | Time |
|---------|------|-------------------|--------|------|
| **New adopter** | Get a working vault | §1 (Intro), §2 (Terms), §3 (Triad), §4 (Governance), §5 (Directory Structure), §7 (Frontmatter) | ~350 | 10-15 min |
| **Extension builder** | Add entity types, templates, pipelines | New adopter path + §6 (Naming), §12 (Templates), §14 (Pipelines), §19 (Extensions) | ~550 | 20-25 min |
| **Standard contributor** | Understand the full spec | Everything | 1,336 | 45-60 min |

### New Adopter Path

Read these six sections in order. They give you the structural foundation to set up and operate an aDNA vault.

1. **§1 Introduction & Scope** — What aDNA is, who it's for, RFC 2119 keywords
2. **§2 Terminology** — 12 key terms (triad, governance file, bare/embedded, session, SITREP)
3. **§3 Triad Architecture** — The `who/what/how` ontology, bare vs. embedded deployment forms
4. **§4 Governance Files** — CLAUDE.md, MANIFEST.md, STATE.md, AGENTS.md, README.md — what each does
5. **§5 Directory Structure** — Required/recommended/optional subdirectories for each triad leg
6. **§7 Frontmatter System** — Required YAML fields, tag conventions, type-specific extensions

**After this path**: You can create and operate a standard aDNA vault. Come back for sessions (§8), missions (§9), and collision prevention (§13) when you need them.

### Extension Builder Path

Start with the new adopter path above, then add these four sections:

7. **§6 Naming Conventions** — `type_descriptive_name.md` pattern, ALLCAPS governance list, directory naming
8. **§12 Template System** — Starter/Standard/Full template sets, template conventions
9. **§14 Content-as-Code Pipelines** — Folder-based workflows where file location = processing state
10. **§19 Optional Extensions** — Machine registry, backlog, skill files, testing/CI, reference code, ADRs

**After this path**: You can extend an aDNA vault with custom entity types, templates, pipelines, and optional subsystems.

### Standard Contributor Path

Read everything. The appendices (§20) contain the persona framework, aggregation point patterns, deferred topics, and the full decision traceability matrix mapping all 40 design decisions to their spec locations.

---

## 2. Section Map

All 20 numbered sections of the standard with one-line summaries, persona tags, and line ranges.

| § | Section | Summary | Personas | Lines |
|---|---------|---------|----------|-------|
| 1 | Introduction & Scope | What aDNA is, who it's for, RFC 2119 keywords | All | 19-52 |
| 2 | Terminology | 12 key terms: triad, governance file, bare/embedded, session, SITREP, content-as-code | All | 54-73 |
| 3 | Triad Architecture | `who/what/how` ontology, bare vs. embedded deployment forms, classification question test | All | 75-171 |
| 4 | Governance Files | Five ALLCAPS files (CLAUDE, MANIFEST, STATE, AGENTS, README) — purpose, contents, quickstart | All | 173-294 |
| 5 | Directory Structure | Required/recommended/optional subdirectories for each triad leg, starter/standard/full skeletons | All | 296-462 |
| 6 | Naming Conventions | Underscores not hyphens, `type_descriptive_name.md`, ALLCAPS governance list, `type_` prefixes | Extension+ | 464-516 |
| 7 | Frontmatter System | Required base fields (`type`, `created`, `updated`, `last_edited_by`, `tags`), tag conventions | All | 518-570 |
| 8 | Session Model | Bounded units of agent work — lifecycle (create → execute → close → archive), tiers, SITREP, next-session prompt, 75% rule | Operations | 572-664 |
| 9 | Mission System | Multi-session work decomposition — objectives, acceptance criteria, stages, handoff protocol | Operations | 666-713 |
| 10 | Context Library | `what/context/` — topic organization, context subtypes (research, guide, core), token budget awareness | Operations | 715-759 |
| 11 | Coordination Protocol | `who/coordination/` — cross-agent notes, urgency levels (urgent/info/fyi), ephemeral by design | Multi-agent | 761-789 |
| 12 | Template System | Graduated template sets (starter/standard/full), template naming and conventions | Extension+ | 791-827 |
| 13 | Collision Prevention | Three tiers: universal (frontmatter attribution), sync (file safety tiers), multi-agent (coordination + scope declarations) | Operations | 829-887 |
| 14 | Content-as-Code Pipelines | Folder-based workflows — file location IS processing state, pipeline structure, stage AGENTS.md | Extension+ | 889-939 |
| 15 | Archive & Versioning | Archive patterns for sync vs. git environments, retention, CLAUDE.md version tracking | Reference | 941-970 |
| 16 | Tool Integration Tiers | Three tiers: core standard (Tier 1, universal), frontmatter querying (Tier 2), environment-specific (Tier 3) | Reference | 972-1028 |
| 17 | Error & Recovery Protocol | Three-tier response: data integrity (STOP), state inconsistency (fix + log), process issues (workaround + backlog) | Operations | 1030-1064 |
| 18 | Success Criteria | Minimum viable (cold start, handoff, integrity), recommended (fork, scale, consistency), aspirational (network, collision safety, dual-audience) | Contributor | 1066-1116 |
| 19 | Optional Extensions | Machine registry, backlog, skill files, testing/CI awareness, reference code, ADRs | Extension+ | 1118-1198 |
| 20 | Appendices | Persona framework (App A), aggregation points (App B), deferred topics (App C), decision traceability matrix (App D — 40 decisions) | Contributor | 1200-1336 |

**Persona key**: All = everyone reads this. Extension+ = extension builders and contributors. Operations = anyone running sessions/missions. Multi-agent = concurrent agent environments. Reference = consult when needed. Contributor = standard contributors.

---

## 3. When to Read the Design Document

[`adna_design.md`](adna_design.md) is the companion "why" document. It explains the rationale behind design decisions — why three legs, why these governance files, why these trade-offs. Read it when you want:

- **Rationale** for why the standard works the way it does
- **Worked examples** of deployment patterns (standalone, nested, federated)
- **Trade-off analysis** behind structural decisions

The design document is not required for operational use. The standard tells you **what** to do; the design document tells you **why**.

---

## 4. Skill vs. Lattice: When to Use Which

aDNA has two constructs that both deal with "reusable capabilities" — **skill files** and **skill-type lattices**. They serve different purposes and live in different locations.

### Comparison

| Dimension | Skill File | Skill-Type Lattice |
|-----------|-----------|-------------------|
| **Location** | `how/skills/skill_<name>.md` | `what/lattices/<name>.lattice.yaml` |
| **Format** | Markdown with procedural steps | YAML directed graph with nodes and edges |
| **Purpose** | Agent recipe — step-by-step instructions | Composable computational unit — executable DAG |
| **When to create** | You have a repeatable procedure an agent should follow | You need a composable, publishable, executable workflow |
| **Execution** | Agent reads and follows the steps | Runtime engine traverses the DAG |
| **Registry** | Not publishable (local to the vault) | Publishable via `latlab lattice publish` |
| **Promotion path** | Can be promoted to a lattice via `skill_lattice_publish` | Already a lattice — can be composed with other lattices |

### Decision Rule

**Start with a skill file.** If the procedure needs to be published to a registry, composed with other lattices, or executed by a runtime engine, promote it to a `lattice_type: skill` lattice.

The promotion path is documented in `how/skills/skill_lattice_publish.md`. Most agent recipes stay as skill files — lattice promotion is for procedures that need computational composability.

### Examples

| Scenario | Use | Why |
|----------|-----|-----|
| "Deploy this service in 5 steps" | Skill file | Agent follows the steps — no DAG needed |
| "Run ESM-2 embedding → clustering → visualization" | Lattice | Computational pipeline — needs runtime execution |
| "Review and audit context quality" | Skill file | Procedural checklist — agent walks through it |
| "Compose protein design with docking and scoring" | Lattice | Multi-module DAG — needs composability with other lattices |

---

## 5. Quick Reference

**"I want to..."**

| Goal | Where to look |
|------|--------------|
| Set up my first vault | §3-5 of the standard, or the [README Quick Start](../../README.md#quick-start) |
| Add a new entity type | §6 (Naming) + §7 (Frontmatter) + §19 (Extensions) |
| Track sessions | §8 (Session Model) |
| Run a multi-session project | §9 (Mission System) |
| Write an agent skill | `how/skills/AGENTS.md` + §19.3, then this guide's §4 for lattice promotion |
| Build a pipeline | §14 (Content-as-Code Pipelines) |
| Understand collision prevention | §13 (Collision Prevention) |
| Evaluate aDNA for my project | [`adna_design.md`](adna_design.md) — the "why" document |
| Add aDNA to an existing codebase | [`migration_guide.md`](migration_guide.md) |
| Use aDNA without Obsidian | [`agent_first_guide.md`](agent_first_guide.md) |
| Manage multiple aDNA projects | [`projects_folder_pattern.md`](projects_folder_pattern.md) — workspace pattern with agent-guided scaffolding |

---

## Cross-References

- [aDNA Universal Standard](adna_standard.md) — the normative spec this guide navigates
- [aDNA Design Document](adna_design.md) — architecture rationale and trade-off analysis
- [Migration Guide](migration_guide.md) — adding aDNA to existing projects
- [Agent-First Guide](agent_first_guide.md) — terminal-first aDNA setup
- [Projects Folder Pattern](projects_folder_pattern.md) — multi-project workspace with shared templates
- [Skills Protocol](../../how/skills/AGENTS.md) — skill file conventions and categories
