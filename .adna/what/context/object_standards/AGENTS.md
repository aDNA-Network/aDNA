# Object Standards — Context Index

## Overview

Standards, templates, and FAIR metadata requirements for the three core aDNA object types: modules, datasets, and lattices. References the normative aDNA Standard v2.1.

## Subtopics

| # | Subtopic | File | ~Tokens | Quality | Sources |
|---|----------|------|---------|---------|---------|
| 1 | Standards Overview | `context_object_standards_overview.md` | ~1,000 | 3.8 | 6 sources (Standard v2.1, lattice schema, dataset schema, 13 examples, type_vocabulary, fair_mapping) |

## Total Token Budget

~1,000 tokens to load all subtopics

## Usage Notes

Load this topic when creating new modules, datasets, or lattices. Essential for understanding FAIR metadata requirements, type vocabulary usage, and quality criteria for object definitions.

**Relationship to adna_core**: Complements `type_vocabulary` (canonical I/O types) and `fair_mapping` (FAIR envelope interconversion). This file is the practical "how to create objects" guide; adna_core files provide the theoretical underpinning.

## Load/Skip Decision

**Load when**: Creating or auditing modules, datasets, or lattices. Understanding FAIR requirements.
**Skip when**: Working on operational content (campaigns, sessions) with no object creation.

**Token cost**: ~200 tokens (this AGENTS.md)
