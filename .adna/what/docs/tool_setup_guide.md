---
type: context
title: "aDNA Tool-Agnostic Setup Guide"
created: 2026-03-20
updated: 2026-03-20
last_edited_by: agent_init
status: approved
tags: [context, setup, tools, vscode, terminal, obsidian]
---

# aDNA Tool-Agnostic Setup Guide

> Get productive with aDNA using your preferred tool. aDNA is tool-agnostic at Tier 1 — any text editor and file system works.

---

## Prerequisites

All setups require:
- Git (for cloning and version control)
- A text editor that can read markdown and YAML
- Python 3.8+ (for validation tooling)

---

## Setup 1: Terminal + Claude Code (Minimal)

Best for: agent operators, CLI-first workflows, headless environments.

### Quick Start

```bash
# Clone or create an aDNA instance
git clone <your-adna-repo> && cd <repo-name>

# Or bootstrap a new instance
bash setup.sh  # if available, or manually create the triad

# Validate the instance
python what/lattices/tools/adna_validate.py .

# Start working — Claude Code reads CLAUDE.md automatically
claude
```

### What Works

| Feature | Support |
|---------|---------|
| Directory structure (Tier 1) | Full — `ls`, `tree`, `find` |
| YAML frontmatter (Tier 1/2) | Full — any YAML parser |
| Markdown content (Tier 1) | Full — `cat`, `less`, `bat` |
| Validation tooling | Full — Python scripts |
| Wikilinks (Tier 3) | Rendered as plaintext — still navigable via grep |
| Graph view (Tier 3) | Not available |

### Tips

- Use `grep -r "type: mission" how/missions/` to find active missions
- Use `grep -r "status: active" --include="*.md"` for active items
- Session files are your changelog — check `how/sessions/active/`

---

## Setup 2: VS Code / Cursor

Best for: developers, mixed code + knowledge workflows, team environments.

### Quick Start

```bash
# Clone and open
git clone <your-adna-repo>
code <repo-name>   # or: cursor <repo-name>
```

### Recommended Extensions

| Extension | Purpose |
|-----------|---------|
| **YAML** (Red Hat) | Frontmatter syntax highlighting and validation |
| **Markdown All in One** | Markdown preview, TOC generation |
| **Foam** or **Dendron** | Wikilink support, backlinks, graph view |
| **Mermaid Preview** | Render Mermaid diagrams inline |

### Configuration

Add to `.vscode/settings.json` for best experience:

```json
{
  "files.associations": {
    "*.md": "markdown"
  },
  "markdown.validate.enabled": true,
  "yaml.schemas": {
    "what/lattices/lattice_yaml_schema.json": "*.lattice.yaml",
    "what/lattices/tools/frontmatter_schema.json": "*.md"
  }
}
```

### What Works

| Feature | Support |
|---------|---------|
| Directory structure (Tier 1) | Full — file explorer |
| YAML frontmatter (Tier 1/2) | Full with YAML extension |
| Markdown content (Tier 1) | Full with preview |
| Wikilinks (Tier 3) | With Foam/Dendron extension |
| Validation tooling | Full — integrated terminal |
| Graph view (Tier 3) | With Foam extension (basic) |

---

## Setup 3: Obsidian

Best for: knowledge workers, visual thinkers, projects with heavy cross-referencing.

### Quick Start

1. Download [Obsidian](https://obsidian.md)
2. Open the aDNA instance directory as a vault
3. Trust the vault when prompted (required for community plugins)

### Recommended Plugins

| Plugin | Purpose |
|--------|---------|
| **Dataview** | Query frontmatter across the vault (Tier 2) |
| **Templater** | Use aDNA templates from `how/templates/` |
| **Obsidian Git** | Auto-commit and sync |
| **Notebook Navigator** | Enhanced session navigation |

### Tier 3 Features (Obsidian-specific)

- **Wikilinks**: `[[file_name]]` syntax for bidirectional linking
- **Graph View**: Visual map of all cross-references
- **Canvas**: Visual composition of lattice workflows
- **Dataview queries**: Dynamic tables from frontmatter
- **Banner images**: Visual file identification via `banner` field

### What Works

| Feature | Support |
|---------|---------|
| All Tier 1/2/3 features | Full |
| Validation tooling | Via integrated terminal or external |

---

## Conformance by Tool

All three setups support full aDNA conformance:

| Conformance Level | Terminal | VS Code | Obsidian |
|-------------------|----------|---------|----------|
| Starter | Yes | Yes | Yes |
| Standard | Yes | Yes | Yes |
| Full | Yes | Yes | Yes |

The aDNA standard is designed so that **Tier 1 features (directory structure, YAML frontmatter, markdown files, naming conventions) work universally**. Tier 2 adds frontmatter querying (any YAML-aware tool). Tier 3 adds environment-specific enhancements.

---

## Validation (All Tools)

```bash
# Check instance conformance
python what/lattices/tools/adna_validate.py .

# Check governance file consistency
bash what/lattices/tools/governance_sync_check.sh

# Validate a specific lattice YAML
python what/lattices/tools/lattice_validate.py path/to/file.lattice.yaml
```

## Related Docs

- `agent_first_guide.md` — Agent operator setup (Claude Code focus)
- `adna_standard.md` §16 — Tool Integration Tiers specification
- `standard_reading_guide.md` — How to navigate the standard document
