---
type: directory_index
topic: prompt_engineering
created: 2026-02-19
updated: 2026-03-18
token_estimate: 12500
last_edited_by: agent_init
tags: [directory_index, context, prompt_engineering]
---

# Prompt Engineering — Context Index

## Overview

Research-backed context on prompt engineering, context engineering, and agentic knowledge architecture. Covers formatting for LLM attention, governance file design, project scaffolding, ontology design, federation patterns, diagram best practices, and the functional-analytic convergence model that underpins aDNA's hierarchical context-serving approach.

## Subtopics

| Subtopic | File | Token Estimate | Version | Sources |
|----------|------|---------------|---------|---------|
| Signal-to-Token Optimization | `context_prompt_engineering_signal_to_token.md` | ~1,500 | 1.0 | 5 sources |
| CLAUDE.md Best Practices | `context_prompt_engineering_claude_md_best_practices.md` | ~1,500 | 1.0 | 5 sources |
| Agentic Project Scaffolding | `context_prompt_engineering_agentic_scaffolding.md` | ~1,500 | 1.0 | 5 sources |
| Ontology Design for LLM Agents | `context_prompt_engineering_ontology_design.md` | ~2,000 | 1.0 | 6 sources |
| Federation & Composability | `context_prompt_engineering_federation_composability.md` | ~2,000 | 1.0 | 6 sources |
| Mermaid Diagram Best Practices | `context_prompt_engineering_mermaid_best_practices.md` | ~1,500 | 1.0 | 5 sources |
| Convergence Model | `context_prompt_engineering_convergence_model.md` | ~2,500 | 1.0 | 3 sources |

## Total Token Budget

~12,500 tokens to load all 7 subtopics.

## Usage by Task

| Task | Load These Subtopics |
|------|---------------------|
| Writing context files | signal_to_token, convergence_model |
| Designing CLAUDE.md or governance files | claude_md_best_practices, agentic_scaffolding |
| Structuring a new aDNA instance | agentic_scaffolding, ontology_design |
| Extending or modifying an ontology | ontology_design, federation_composability |
| Creating architecture diagrams | mermaid_best_practices |
| Planning federation or sharing | federation_composability, ontology_design |
| Evaluating ontology structure quality | convergence_model, ontology_design |
| Writing AGENTS.md files | agentic_scaffolding, signal_to_token, convergence_model |

## Dependency Notes

- **convergence_model** builds on signal_to_token and ontology_design — read those first for full context
- **federation_composability** builds on ontology_design — read ontology_design first if unfamiliar with base/extension partitioning
- All other subtopics are independently loadable

## Load/Skip Decision

**Load this directory when**:
- Doing context engineering or writing CLAUDE.md / AGENTS.md governance files
- Designing or evaluating ontology structure for an aDNA instance
- Planning federation, multi-vault composition, or lattice interop
- Creating architecture diagrams with Mermaid
- Writing new context files (load signal_to_token for formatting best practices)

**Skip when**:
- Performing routine operational work (sessions, missions, CRM updates)
- Working on domain-specific content that doesn't involve governance or architecture
- Already loaded the relevant subtopics earlier in this session

**Token cost**: ~400 tokens (this AGENTS.md). Full topic: ~12,500 tokens. Use the "Usage by Task" table to load selectively.
