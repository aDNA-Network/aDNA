# Contributing to aDNA

Thank you for your interest in improving aDNA. This guide covers how to report issues, suggest improvements, and submit changes.

aDNA is a knowledge architecture standard — contributions are primarily **documentation, templates, and design patterns** rather than application code. Every file in this repo is Markdown, YAML, JSON, or shell script.

---

## Code of Conduct

This project will adopt the [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) as its Code of Conduct. The `CODE_OF_CONDUCT.md` file will be added in a future update. By participating, you agree to uphold community standards of respectful, constructive collaboration.

---

## Ways to Contribute

### Report a Bug

Found something broken — a dead link, incorrect schema, template that doesn't match the standard?

1. Check [existing issues](https://github.com/aDNA-Network/aDNA/issues) to avoid duplicates
2. Open a [bug report](https://github.com/aDNA-Network/aDNA/issues/new?template=bug_report.md)
3. Include the aDNA version (`CLAUDE.md` frontmatter `version` field) and steps to reproduce

### Suggest an Improvement

Have an idea for a better template, a missing context topic, or a workflow enhancement?

- Open a [GitHub issue](https://github.com/aDNA-Network/aDNA/issues/new) describing the improvement
- For detailed proposals, submit a PR with the change — see [Suggesting Improvements](#suggesting-improvements) below

### Submit a Pull Request

1. Fork the repository
2. Create a feature branch (`git checkout -b proposal/your-description`)
3. Make your changes following the [style guide](#style-guide) below
4. Submit a PR with a clear description of the change and why it helps

---

## Development Setup

aDNA is a Markdown-based knowledge architecture — no build step, no dependencies beyond a text editor.

### Quick Start

```bash
# Clone the repo
git clone https://github.com/aDNA-Network/aDNA.git ~/aDNA
cd ~/aDNA

# Run setup (downloads Obsidian plugins for the template)
chmod +x .adna/setup.sh
./.adna/setup.sh

# Option A: Browse in Obsidian
# Open the .adna/ folder as an Obsidian vault

# Option B: Work with Claude Code
# Run 'claude' — the root CLAUDE.md guides project creation
```

### Validation

```bash
# Validate lattice YAML files
python .adna/what/lattices/tools/lattice_validate.py .adna/what/lattices/examples/*.yaml
```

---

## Suggesting Improvements

The best aDNA improvements come from real usage. When you (or your AI agent) discover friction, missing templates, or documentation gaps while working in an aDNA vault, here's how to route that feedback upstream.

### Human Contributors

1. Check [existing issues](https://github.com/aDNA-Network/aDNA/issues) for duplicates
2. Open a GitHub issue describing what you observed, what task you were doing, and what improvement you'd suggest
3. For larger changes, submit a PR with the fix — see [Submit a Pull Request](#submit-a-pull-request) above

### Agent Contribution Mode

AI agents working in aDNA vaults are trained to notice **framework-level** improvement opportunities during normal work — things like missing template fields, undocumented patterns, or naming inconsistencies.

The agent workflow:
1. Agent notices a framework-level gap during a task
2. At a natural pause point (end of task, session close), agent mentions it to the user
3. If the user approves, agent creates a backlog idea file: `how/backlog/idea_upstream_<description>.md`
4. Optionally (if `gh` CLI is configured), agent opens a GitHub issue on `aDNA-Network/aDNA`

This is **organic, not forced** — agents surface suggestions only when they encounter real friction, and only with user approval. No configuration needed; the behavior is part of the agent's standard awareness.

Full protocol: [`how/skills/skill_upstream_contribution.md`](how/skills/skill_upstream_contribution.md)

---

## Style Guide

### Naming

- **Always underscores, never hyphens**: `template_proposal.md`, not `template-proposal.md`
- **Type prefix**: `proposal_`, `template_`, `context_`, etc.
- **Dates in filenames**: `YYYYMMDD` format (e.g., `proposal_20260320_new_context_recipe.md`)

### Frontmatter

Every content file needs YAML frontmatter:

```yaml
---
type: {entity_type}
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
last_edited_by: {your_name}
tags: []
---
```

### Content

- Write in plain Markdown (CommonMark)
- Use tables for structured comparisons
- Use wikilinks (`[[target]]`) for internal references within the vault
- Use standard Markdown links for external references and GitHub rendering

### Commits

- One logical change per commit
- Descriptive commit messages: `feat(templates): add migration checklist template`
- Prefix with conventional commit types: `feat`, `fix`, `docs`, `chore`

---

## Review Process

1. **Triage** — Maintainers label and prioritize within 1 week
2. **Review** — At least one maintainer reviews for:
   - Consistency with aDNA standard (`what/docs/adna_standard.md`)
   - Naming conventions
   - Frontmatter completeness
   - No breaking changes to existing structure
3. **Merge** — Squash-merge to `main` with a changelog-worthy commit message

### What Makes a Good Contribution

- **Solves a real problem** you encountered while using aDNA
- **Follows existing patterns** rather than inventing new conventions
- **Includes context** — why this change helps, not just what it changes
- **Scoped tightly** — one improvement per PR, not a kitchen-sink refactor

---

## Questions?

- Open a [discussion](https://github.com/aDNA-Network/aDNA/discussions) for questions about aDNA architecture
- Check [`what/docs/`](what/docs/) for specification documents and design rationale
- Read the [README](README.md) for a project overview
