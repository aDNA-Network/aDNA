---
type: directory_index
created: 2026-03-18
updated: 2026-04-03
token_estimate: 200
last_edited_by: agent_init
tags: [directory_index, context, lattice_basics]
---

# Lattice Basics — Context Index

## Overview

Orienting new users and agents to the aDNA framework: vault structure, `.lattice.yaml` format, object types, and core concepts. This is the entry-point topic for agents unfamiliar with the vault.

## Subtopics

| # | Subtopic | File | ~Tokens | Quality | Sources |
|---|----------|------|---------|---------|---------|
| 1 | Core Concepts | `context_lattice_basics_core_concepts.md` | ~1,000 | 4.0 | 5 sources (Standard v2.1, Design Doc, lattice_design context, hello_world example, type_vocabulary) |
| 2 | Vault Architecture | `context_lattice_basics_vault_architecture.md` | ~1,000 | 4.0 | 5 sources (Standard v2.1, Design Doc, CLAUDE.md, MANIFEST.md, template library) |

## Total Token Budget

~2,000 tokens to load all subtopics

## Usage Notes

Load this topic when onboarding new users, explaining vault structure, or when an agent needs to understand the aDNA framework basics. This is the starting point for agents unfamiliar with the vault.

**Relationship to adna_core**: These files are beginner-oriented overviews. For reference-grade depth, load `adna_core/` subtopics (e.g., `lattice_design` for full YAML schema, `paradigm_overview` for triad theory).

## Load/Skip Decision

**Load when**: First session in a vault, onboarding users, explaining aDNA to newcomers.
**Skip when**: Already oriented — use `adna_core/` for deeper reference work.

**Token cost**: ~200 tokens (this AGENTS.md)
