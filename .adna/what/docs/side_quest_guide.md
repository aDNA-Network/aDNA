---
type: doc
title: "Side-Quest Participation Guide"
created: 2026-03-20
updated: 2026-03-20
status: active
last_edited_by: agent_init
tags: [doc, community, side-quests, validation, participation]
---

# Side-Quest Participation Guide

## What Are Side-Quests?

Side-quests are **distributed validation experiments** for the aDNA knowledge architecture. Maintainers create structured experiment specifications ("quests"), and community members run them in their own environments using spare agent tokens. Results flow back as structured data to help the project make evidence-based decisions.

Think of it as crowdsourced QA: instead of one team testing one configuration, dozens of contributors test across different models, operating systems, vault sizes, and use cases.

## Why They Exist

aDNA works across many environments — different AI models, different operating systems, different vault sizes and configurations. No single test environment can cover all combinations. Side-quests solve this by:

- **Broadening test coverage** across environments the maintainers can't access
- **Generating real-world data** for design decisions (e.g., "which frontmatter format is more token-efficient?")
- **Lowering the contribution barrier** — running a quest takes 10-20 minutes and requires no deep knowledge of the project
- **Building a data-driven improvement culture** where changes are backed by measurements, not assumptions

## How to Find Quests

Browse the [`how/quests/`](../../how/quests/) directory in the aDNA repo. Each quest file includes:

| Field | What it tells you |
|-------|------------------|
| `difficulty` | easy / medium / hard |
| `estimated_token_cost` | How many tokens you'll spend |
| `model_requirements` | Whether you need a specific model |
| `status` | `active` (open for submissions) or `closed` |

Start with **easy** quests to get familiar with the workflow.

## How to Run a Quest

1. **Read the quest file** — understand the objective, prerequisites, and procedure
2. **Check prerequisites** — do you have the right vault version, model, and setup?
3. **Follow the procedure exactly** — each step is designed to produce comparable data across participants
4. **Collect the measurements** — the quest specifies exactly what data to record, usually as a YAML block
5. **Note any observations** — friction points, surprises, or suggestions are valuable even if the quest "succeeds"

## How to Submit Results

1. **Fork** the [Agentic-DNA repo](https://github.com/LatticeProtocol/adna) (or use your existing fork)
2. **Create a result file** in `how/quests/results/`:
   - Filename: `result_<quest_id>_<YYYYMMDD>_<your_name>.md`
   - Use the [quest result template](../../how/templates/template_quest_result.md)
3. **Fill in all sections**:
   - **Frontmatter**: quest_id, date, environment details, your name/handle
   - **Raw Data**: the YAML measurements block from the quest
   - **Summary**: one-paragraph finding
   - **Observations**: anything noteworthy
   - **Environment Details**: hardware, vault contents, agent config
4. **Open a PR** to the `main` branch with title: `result: <quest_id> — <your_name>`
5. A maintainer will review and merge

## Privacy Rules

**Strict no-PII policy.** Result files must not contain:

- Real names (use a handle if you prefer)
- API keys or credentials
- File paths that reveal personal directory structure
- Any data that could identify individuals

Only include: performance metrics, token counts, success/failure flags, structural observations, and environment specifications (OS, model, vault size).

## Time & Cost Expectations

Each quest's frontmatter includes `difficulty` and `estimated_token_cost`. Typical ranges:

| Difficulty | Time | Tokens |
|-----------|------|--------|
| Easy | 10-15 min | ~1K |
| Medium | 15-25 min | ~2K |
| Hard | 30-45 min | ~4K+ |

These are estimates. Your actual cost may vary based on model and environment.

## Agent Awareness

AI agents working in aDNA vaults are aware of the side-quest system. At natural session-end points, if you have spare context budget, your agent may mention available quests. This is purely informational — agents never interrupt active work for quest awareness, and participation is always opt-in.

## How Results Are Used

Maintainers periodically aggregate submitted results using `what/lattices/tools/aggregate_results.py`:

- **Per-quest summaries**: count, mean, median, min/max across submissions
- **Outlier detection**: results >2σ from the mean are flagged for investigation
- **Decision input**: aggregated findings inform CHANGELOG entries and design decisions
- **Published summaries**: key findings appear in release notes when they drive changes

Your individual result is one data point. The value comes from aggregation across many participants and environments.

## Questions?

- Open a [discussion](https://github.com/LatticeProtocol/adna/discussions) for questions about quests or the submission process
- Check [`CONTRIBUTING.md`](../../CONTRIBUTING.md) for the general contribution guide
- Read [`how/quests/AGENTS.md`](../../how/quests/AGENTS.md) for agent-specific guidance
