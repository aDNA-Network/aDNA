# Vision: The Decentralized Frontier Lab

How a knowledge architecture becomes a living, community-driven system.

---

## The Premise

Every project that adopts aDNA creates a structured knowledge vault — a triad of `who/`, `what/`, `how/` with governance files that give both humans and AI agents instant orientation. Each vault is self-contained, immediately useful, and locally owned.

But knowledge architectures don't evolve in isolation. The patterns that work in one vault — better templates, sharper context structures, cleaner naming conventions — would benefit every other vault using the same standard. The question is: how do you capture that collective learning without centralizing control?

aDNA's answer: make the agents themselves the sensing network.

---

## What Makes This Different

aDNA is not a platform. There is no hosted service, no vendor lock-in, no telemetry. It's a **composable standard** — a set of conventions for organizing project knowledge that any team can adopt, extend, and own.

Three principles shape everything:

1. **You own your vault.** Your data stays in your directories, synced by your git remote, browsed by your tools. aDNA adds structure; it never takes custody.

2. **The standard is open.** The [normative specification](what/docs/adna_standard.md), governance files, templates, and tools are MIT-licensed and public. Fork it, extend it, contribute back — or don't. Each level of participation is self-contained.

3. **Improvement is organic.** AI agents working in aDNA vaults encounter real friction — a missing template field, an undocumented pattern, an awkward naming convention. That friction is signal. The contribution system turns that signal into structured improvements without interrupting the work that surfaced it.

---

## The Decentralized Frontier Lab

Imagine a research lab where every experiment happens in a different location, run by different people, on different problems — but the methodology, equipment standards, and reporting formats are shared. Each lab benefits from the collective refinement of the tools, and each lab's discoveries flow back to improve the tools for everyone else.

That's the model. aDNA vaults are the labs. The standard is the shared methodology. And four pieces of infrastructure make the feedback loop work:

### Agents Surface Improvements Organically

AI agents working in any aDNA vault are trained to notice **framework-level** improvement opportunities during normal work. When an agent encounters a gap — a template missing a useful field, a naming pattern that causes confusion, a workflow that could be smoother — it mentions the finding to the user at a natural pause point.

If the user approves, the agent creates a structured backlog item. If the user has the GitHub CLI configured, the agent can open an upstream issue directly. No special configuration required; this awareness is built into the agent protocol.

Full protocol: [`how/skills/skill_upstream_contribution.md`](how/skills/skill_upstream_contribution.md)

### Side-Quests Generate Community Data

Some improvements need data from multiple environments before the right answer becomes clear. Should frontmatter use flat or nested FAIR metadata? How many tokens does a migration prompt actually consume across different vault sizes?

**Side-quests** are structured experiments that community members can run with spare agent tokens. Each quest specifies a procedure, expected output format, and estimated cost. Results flow back as structured data that maintainers aggregate to make evidence-based decisions.

Current quests: [`how/quests/`](how/quests/)
Participation guide: [`what/docs/side_quest_guide.md`](what/docs/side_quest_guide.md)
Results aggregation: [`what/lattices/tools/aggregate_results.py`](what/lattices/tools/aggregate_results.py)

### Migrations Keep Everyone Current

As the standard evolves, vaults need to keep up. aDNA includes a **version migration system** — structured prompts that walk agents through upgrading a vault from one governance version to the next. Each migration is sequential, safe, and reversible (git-tagged snapshots enable rollback).

The migration system means improvements actually propagate. A better template structure isn't just published — it's delivered to every vault that runs the migration prompt.

Available migrations: [`how/migrations/`](how/migrations/)
Migration guide: [`what/docs/version_migration_guide.md`](what/docs/version_migration_guide.md)

### The Standard Evolves From the Field

Traditional standards evolve through committee. aDNA evolves through usage. The cycle:

1. Agents encounter friction in real vaults
2. Users approve backlog items for promising improvements
3. Side-quests collect data when evidence is needed
4. Maintainers merge validated improvements
5. Migration prompts deliver changes to every vault
6. The next version of the standard reflects what actually worked

This is deliberately bottom-up. The best improvements come from people (and agents) doing real work, not from design committees speculating about requirements.

---

## The Participation Ladder

Every level is self-contained. No level requires the next.

### Level 0: Use aDNA Standalone

Clone the repo. Customize it for your project. Use the triad, templates, and tools for your own knowledge management. You never need to interact with the community, submit anything upstream, or even acknowledge that other aDNA vaults exist.

**Value**: Structured knowledge architecture that both you and your AI agents can navigate. Faster agent orientation, better session continuity, organized project knowledge.

> **Compute Participation**: Level 0 vaults can optionally upgrade to L1
> compute nodes, adding JupyterHub and joining the Lattice compute network.
> This is orthogonal to the knowledge contribution ladder. See
> `how/skills/skill_l1_upgrade.md`.

### Level 1: Submit Upstream Improvements

When your agent surfaces a framework-level improvement, approve the backlog item and (optionally) open a GitHub issue upstream. Your improvement helps every aDNA user — and you benefit from everyone else's improvements when you run migrations.

**Value**: Everything from Level 0, plus your vault improves as the standard improves. Your contributions make the tools better for everyone.

### Level 2: Run Side-Quests

Browse the quest directory. Find an experiment that interests you — or that your spare agent tokens can handle. Run it, submit the structured result. Your data point joins others to inform standard evolution decisions.

**Value**: Everything from Level 1, plus you contribute to evidence-based standard development. Each quest takes 10-30 minutes and costs a few thousand tokens.

### Level 3: Create Quests, Review Contributions, Evolve the Standard

Design quests for questions the community needs answered. Review submitted improvements and results. Contribute to migration prompts. Help shape what aDNA becomes.

**Value**: Everything from Level 2, plus you're actively steering the direction of the knowledge architecture standard.

---

## How Everything Connects

The infrastructure supporting this vision was built across six missions:

| Component | What it does | Location |
|-----------|-------------|----------|
| **Projects folder pattern** | Multi-project workspace with agent-guided scaffolding | [`what/docs/projects_folder_pattern.md`](what/docs/projects_folder_pattern.md) |
| **Version migration system** | Safe, sequential vault upgrades between governance versions | [`how/migrations/`](how/migrations/) |
| **Migration safety framework** | Rollback, validation, and testing for migrations | [`what/docs/migration_safety_framework.md`](what/docs/migration_safety_framework.md) |
| **CHANGELOG** | Two-track version history with migration cross-links | [`CHANGELOG.md`](CHANGELOG.md) |
| **Contribution system** | CONTRIBUTING.md + Agent Contribution Mode + upstream skill | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| **Side-quest infrastructure** | Quest specs, result templates, aggregation tooling | [`how/quests/`](how/quests/) + [`what/lattices/tools/`](what/lattices/tools/) |

Each component works independently. Together, they form the feedback loop that turns individual vault usage into collective standard improvement.

---

## What's Next

The vision is aspirational but the infrastructure is real and delivered. Here's what comes next:

- **Lattice Start Kit** — A 1-click onboarding experience: CLI interview → scaffolded vault with domain-specific templates. Design complete ([PRD](what/docs/start_kit_prd.md)); build pending.

- **Federation** — Cross-instance lattice sharing, registry publishing, and compute orchestration. The protocol layer that connects vaults into a network.

- **Code of Conduct** — Adopting [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) to formalize community standards.

- **Quest CI** — GitHub Actions to validate quest result submissions on PR, ensuring data quality as community participation grows.

- **Standard v3.0** — The next major version of the normative specification, incorporating learnings from the community infrastructure phase.

---

## Get Started

- **New to aDNA?** Start with the [README](README.md) — clone, setup, customize in minutes.
- **Want to contribute?** Read [`CONTRIBUTING.md`](CONTRIBUTING.md) — bug reports, improvements, and Agent Contribution Mode.
- **Want to run a quest?** Browse [`how/quests/`](how/quests/) and follow the [Side-Quest Guide](what/docs/side_quest_guide.md).
- **Want to add aDNA to an existing project?** See the [Migration Guide](what/docs/migration_guide.md).

---

*This document describes the long-term vision for aDNA as a community-driven knowledge architecture standard. The infrastructure described here is delivered and functional. The community growth it enables is aspirational — it depends on adoption, contribution, and collective iteration.*
