---
type: decision
adr_id: adr_001
adr_number: 1
title: "Choice of Obsidian as Knowledge Platform"
status: accepted
created: 2026-03-18
updated: 2026-03-18
last_edited_by: agent_init
supersedes:
superseded_by:
tags: [adr, decision, obsidian, platform]
---

# ADR-001: Choice of Obsidian as Knowledge Platform

## Status

Accepted

## Context

The aDNA paradigm requires a knowledge management platform that supports:
- Local-first operation (no mandatory cloud dependency)
- Bidirectional linking between entities (wikilinks)
- Markdown-native storage for git version control
- Plugin extensibility for custom workflows (templates, queries, canvas)
- Multi-user collaboration via git (not proprietary sync)
- AI agent compatibility (plain-text files, predictable structure)

Alternatives evaluated: Notion (cloud-locked, opaque export), Confluence (enterprise-heavy, poor git story), plain Markdown + VS Code (no graph, no link resolution), Logseq (outliner-first, weaker folder structure).

## Decision

Use **Obsidian** as the primary knowledge platform for aDNA vaults. Obsidian operates on a local folder of Markdown files, supports community plugins, and stores all configuration in `.obsidian/` alongside content — making the entire vault git-portable.

Key enablers:
- **Templater plugin** — auto-applies templates per directory (entity type → frontmatter schema)
- **Dataview plugin** — queries frontmatter for dynamic tables and dashboards
- **Canvas** — visual lattice composition and presentation
- **Folder Notes** — index files for progressive disclosure
- **Git plugin** — auto-commit and sync without leaving Obsidian

## Consequences

### Positive
- Full data sovereignty — no vendor lock-in, all content is plain Markdown + YAML
- Git-native sync enables multi-user collaboration across machines and organizations
- Rich plugin ecosystem allows adapting the platform to aDNA workflows
- AI agents (Claude Code, etc.) can read and write vault files directly

### Negative
- Plugin dependency — some workflows rely on community plugins that may lag behind updates
- No native real-time collaboration (async-only via git commits)
- Requires git literacy for multi-user setups (mitigated by Obsidian Git plugin)

### Neutral
- Mobile support exists but is less capable than desktop
- Canvas format (`.canvas` JSON) is Obsidian-specific, though content nodes use standard Markdown
