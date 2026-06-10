---
type: context_core
topic: adna_core
subtopic: paradigm_overview
created: 2026-02-20
updated: 2026-03-18
sources: ["aDNA Standard v2.1", "aDNA Design Document", "CLAUDE.md reference implementation"]
context_version: "1.0"
token_estimate: ~1000
last_edited_by: agent_init
tags: [context, adna_core, paradigm, triad, governance]
quality_score: 4.2
signal_density: 4
actionability: 4
coverage_uniformity: 5
source_diversity: 3
cross_topic_coherence: 5
freshness_category: durable
last_evaluated: 2026-02-20
---

# aDNA Core: Paradigm Overview

## Key Principles

1. **aDNA is a knowledge architecture standard for AI-native projects.** It defines how project knowledge is organized so AI agents can orient, operate, and coordinate — alongside humans. An aDNA instance is the complete set of governance files, triad directories, and operational infrastructure implementing the standard.

2. **The what/how/who triad is the universal ontology.** Every piece of project knowledge belongs in exactly one of three categories, determined by the question test:

| Leg | Question | Contains |
|-----|----------|----------|
| **what/** | WHAT does this project know? | Knowledge, context, decisions, domain entities |
| **how/** | HOW does this project work? | Missions, sessions, templates, pipelines, skills |
| **who/** | WHO is involved? | People, teams, coordination, governance |

Three categories are sufficient because they map to the three dimensions of any project: knowledge, operations, people. Additional categories create sorting ambiguity.

3. **Two deployment forms, one ontology.** The triad can be deployed as **bare** (directories at project root — for knowledge bases) or **embedded** (wrapped in `.agentic/` — for git repos). Governance files remain at root in both forms. The ontology is identical; only the nesting differs.

4. **Five governance files orient agents cold.** CLAUDE.md (auto-loaded — structure, rules, persona), MANIFEST.md (what the project IS), STATE.md (where it IS NOW), AGENTS.md (per-directory guide for agents), README.md (per-directory guide for humans). The cold-start path is: CLAUDE.md → STATE.md → ready to work.

5. **Sessions are the unit of accountability.** Every modification happens within a session: create file → execute work → SITREP close-out → archive. Session files provide audit trail, handoff continuity, and conflict detection. The 75% rule reserves 25% of context window for reasoning.

6. **The execution hierarchy provides convergent narrowing.** Campaign → Mission → Objective. Each level narrows the context window, reducing token count while increasing signal density. This is the convergence model applied operationally.

## Recommendations

### Starting a New aDNA Instance

| Step | Action | Skeleton Level |
|------|--------|---------------|
| 1 | Choose deployment form (bare vs embedded) | — |
| 2 | Create governance files (CLAUDE.md, MANIFEST.md, README.md) | Starter |
| 3 | Create triad directories with AGENTS.md | Starter |
| 4 | Add STATE.md, backlog, decisions | Standard |
| 5 | Add domain-specific directories, skills, pipelines | Full |

### Cold-Start Orientation (Agent)

1. Read CLAUDE.md — understand structure, rules, persona
2. Read STATE.md — understand current phase, blockers, recent decisions
3. Check `how/sessions/active/` — identify conflicting sessions
4. Check `who/coordination/` — read urgent cross-agent notes
5. Create session file in `how/sessions/active/` and begin work

### Collision Prevention Tiers

| Tier | Scope | Key Rules |
|------|-------|-----------|
| **1 — Universal** | Every instance | Frontmatter attribution, read-before-write, new-file safety |
| **2 — Sync** | Cloud/team sync | File safety tiers, archive-don't-rename, one config at a time |
| **3 — Multi-agent** | Concurrent agents | Coordination notes, scope declarations, update-field check |

## Anti-Patterns

1. **Loading everything.** Never load an entire context topic or directory — use AGENTS.md to select only needed subtopics.
2. **Skipping STATE.md.** Proceeding without reading STATE.md leads to duplicated work and missed blockers.
3. **Creating files without sessions.** Every file modification must happen within a session — no untracked changes.
4. **Deep hierarchies.** Four+ triad legs create sorting ambiguity. Three is the correct number.
5. **Mixing deployment forms.** A project MUST use exactly one form — bare or embedded.

## Cross-References

- **Convergence model**: `adna_core/convergence_model` — operational quick-reference for the narrowing property
- **Ontology design**: `adna_core/ontology_design` — how to extend the base ontology
- **Context engineering**: `adna_core/context_engineering` — how to write effective context files

## Sources

1. aDNA Universal Standard v2.1 — normative specification (§3 Triad, §4 Governance, §8 Sessions, §13 Collision Prevention)
2. aDNA Design Document — design rationale and trade-offs
3. CLAUDE.md reference implementation — Lattice Labs vault, operational since 2026-02
