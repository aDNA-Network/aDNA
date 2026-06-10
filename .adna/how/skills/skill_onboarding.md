---
type: skill
skill_type: agent
created: 2026-02-19
updated: 2026-03-23
status: active
category: onboarding
trigger: "First-run detection in CLAUDE.md indicates uncustomized forked project (no role: template, last_edited_by: agent_init)"
last_edited_by: agent_init
tags: [skill, onboarding, first-run, project]

requirements:
  tools: []
  context: ["CLAUDE.md", "MANIFEST.md", "STATE.md"]
  permissions: ["write governance files", "create directories"]
---

# Skill: First-Run Onboarding

## Overview

Interactive onboarding flow for **forked aDNA projects** (not the base template). Invoked automatically when CLAUDE.md first-run detection identifies an uncustomized project. Walks the user through understanding aDNA, discovering their project needs, building an initial ontology, and customizing governance files.

**Important**: This skill runs inside a forked project directory, never in the base `adna/` template. If `MANIFEST.md` contains `role: template`, this is the base template — do not run onboarding here. Instead, guide the user to create a project via `skill_project_fork.md`.

## Trigger

Automatic — CLAUDE.md first-run detection triggers this skill when:
1. `MANIFEST.md` does NOT have `role: template` (this is a forked project, not the base template)
2. `how/sessions/history/` is empty (no completed sessions)
3. `MANIFEST.md` frontmatter has `last_edited_by: agent_init`

If conditions 2 and 3 are true (and condition 1 confirms this is a project), load this skill and begin at Step 1.
If only one of conditions 2-3 is true (partial onboarding), resume from the first incomplete step.

## Parameters

None. This skill is self-guided through conversation with the user.

## Requirements

### Tools/APIs
- File read/write access to the vault

### Context Files
- `CLAUDE.md` — project structure and agent protocol
- `MANIFEST.md` — project identity (will be customized)
- `STATE.md` — operational state (will be customized)
- `what/docs/adna_standard.md` — full spec (reference only)

### Permissions
- Write governance files (CLAUDE.md, MANIFEST.md, STATE.md)
- Create directories and AGENTS.md files for ontology extensions

## Implementation

### Step 1: Welcome, Introduce aDNA, and Collect Identity

Greet the user warmly but directly. Introduce yourself as Berthier — the vault's built-in agent chief of staff.

Ask the user what they'd like to be called: "Before we dive in — what should I call you?" Store their answer as `{username}` (lowercase, underscores). This will be used throughout the project for session tracking (`session_{username}_...`), file attribution (`last_edited_by: agent_{username}`), and session metadata (`operator: {username}`).

Explain aDNA in 2-3 accessible sentences: it's a knowledge architecture that gives your project persistent structure both humans and AI agents can navigate. This project was forked from the aDNA template and is ready to be customized for their domain.

Keep it approachable — no spec-heavy language. The user might be a developer, a researcher, or a team lead. Meet them where they are.

### Step 2: Explain the Triad

Introduce the three-directory structure:

- **`what/`** = What you know — knowledge, context, decisions, domain objects
- **`how/`** = How you work — missions, sessions, templates, pipelines
- **`who/`** = Who is involved — people, teams, coordination, governance

Make it concrete with the **Question Test**: "If you have a research paper summary, that answers 'what do we know?' → `what/`. A deployment checklist answers 'how do we deploy?' → `how/`. A team roster answers 'who works on this?' → `who/`."

Mention that this is extensible — they'll add their own entity types under the right leg in Step 6.

### Step 3: Explain Lattices and Context Graphs (brief, skippable)

Lattices are directed graphs connecting datasets, modules, and reasoning nodes into executable compositions. Four types:

| Type | What it does |
|------|-------------|
| `pipeline` | Deterministic DAG of processing stages |
| `agent` | LLM-driven reasoning and decision flow |
| `context_graph` | Knowledge structure connecting concepts |
| `workflow` | Operational process for human/agent procedures |

This vault includes tools to validate and visualize lattices, plus 13 ready-to-use examples across business, creative, research, and biotech domains.

**Lattice-skip path**: If the user's domain is non-computational or they seem unfamiliar with workflow automation, offer the skip:

> "Lattices model executable workflows — pipelines, reasoning chains, multi-step processes. They're powerful for computational work, but **the triad structure handles knowledge management perfectly well without them**. Would you like me to explain lattices in more detail, or shall we move on to exploring your project needs?"

If they skip, acknowledge it naturally and proceed to Step 4. Don't make it feel like they're missing something important — the triad is the core architecture, lattices are an optional layer.

**Tiered depth**: Point to `what/lattices/examples/` for examples. For the full spec, see `what/docs/adna_standard.md`.

Keep this brief — 30 seconds of explanation, not a lecture.

### Step 4: Explain Deployment Diversity

Two deployment forms:
- **Bare triad** (this project) — `what/how/who/` at project root. The full experience.
- **Embedded triad** — `.agentic/what/how/who/` inside an existing repo. For adding aDNA to existing codebases.

This project lives inside a `~/aDNA/` workspace alongside the aDNA base template. Each project in the workspace is self-contained — it can be moved out and still functions independently.

For multi-instance composition (nesting vaults, sibling projects), see `what/docs/adna_bridge_patterns.md`.

One or two sentences is enough here.

### Step 5: Discovery Conversation — Ask About Their Project

This is the most important step. Ask the user about their project, domain, and goals. Choose 2-3 questions that fit the conversation flow:

- "What are you building? What domain are you in?"
- "Is this for a team or are you working solo?"
- "What kind of knowledge will you be managing?" (research, code, operations, customer relationships, etc.)
- "Do you already use AI agents in your workflow?"

Listen for **domain signals** that inform ontology extensions in Step 6:
- Business/CRM terms → `who/customers/`, `who/partners/`, `who/contacts/`, `who/projects/`
- Startup/fundraising terms → `who/investors/`, `what/decisions/` (term sheets), `who/board/`
- Research terms → `what/papers/`, `what/datasets/`, `what/hypotheses/`, `what/experiments/`
- Software terms → `how/incidents/`, `how/deployments/`, `what/services/`, `what/apis/`
- Lab/science terms → `what/experiments/`, `what/compounds/`, `what/protocols/`
- Creative/agency terms → `who/clients/`, `what/creative_assets/`, `how/revision_cycles/`, `what/portfolio/`
- Personal learning terms → `what/courses/`, `what/books/`, `how/learning_goals/`, `what/skills/`
- Healthcare terms → `who/patients/`, `what/treatments/`, `what/protocols/`
- Legal terms → `what/cases/`, `what/contracts/`, `what/compliance/`
- Content/media terms → `what/publications/`, `how/editorial_pipeline/`

Don't ask all questions — read the room and ask what's relevant.

### Step 6: Suggest Ontology Extensions

Based on the discovery conversation, suggest domain-specific entity types with concrete examples. Common extensions:

| Domain | Suggested extensions |
|--------|---------------------|
| **Startup / Business** | `who/customers/`, `who/partners/`, `who/investors/`, `who/board/`, `who/contacts/`, `who/projects/` |
| **Research / Academic** | `what/papers/`, `what/datasets/`, `what/hypotheses/`, `what/experiments/` |
| **Biotech / Science** | `what/experiments/`, `what/compounds/`, `what/protocols/`, `what/datasets/`, `what/targets/` |
| **Software team** | `how/incidents/`, `how/deployments/`, `what/services/`, `what/apis/` |
| **Creative / Agency** | `who/clients/`, `what/creative_assets/`, `how/revision_cycles/`, `what/portfolio/` |
| **Personal Learning** | `what/courses/`, `what/books/`, `how/learning_goals/`, `what/skills/`, `how/habits/` |
| **Healthcare** | `who/patients/`, `what/treatments/`, `what/protocols/`, `what/compliance/` |
| **Legal** | `what/cases/`, `what/contracts/`, `what/compliance/`, `who/clients/` |
| **Content / Media** | `what/publications/`, `how/editorial_pipeline/`, `what/assets/` |

#### Classification Ambiguity Guidance

When suggesting an extension, **explain the triad placement** so the user builds intuition:

> "I'm suggesting `who/investors/` because investors are *people and organizations* — that's the WHO question. Their financial terms (term sheets, SAFE notes) go in `what/decisions/` because those are *things you decided or recorded*. The fundraising process itself goes in `how/campaigns/` because that's *how you execute* the raise."

Common classification decisions to explain:
- **Clients vs. projects**: Clients are WHO (people/orgs). Projects with clients are also WHO (they answer "who is this work for?"). But project *deliverables* are WHAT (knowledge artifacts).
- **Protocols vs. experiments**: A protocol template is HOW (process). A specific experiment using that protocol is WHAT (a knowledge record of what was done and learned).
- **Contracts**: The contract document itself is WHAT (a knowledge artifact). The client who signed it is WHO. The compliance process is HOW.

For each confirmed extension, use the **entity scaffolding skill** (`how/skills/skill_new_entity_type.md`) which automates:
1. Creating the directory under the appropriate triad leg
2. Generating an `AGENTS.md` with purpose and working rules
3. Creating a template in `how/templates/`

**Ask user to confirm before creating anything.** Show them the proposed structure with triad placement rationale and get approval.

### Step 7: Customize Governance Files

Update the three governance files with the user's project identity. Use the `{username}` collected in Step 1 for all `last_edited_by` fields.

**MANIFEST.md:**
- Replace the project description (line 13) with the user's project name and description
- Replace the detail paragraph (lines 15-16) with project-specific details
- Set `last_edited_by: agent_{username}` and `updated: <today>` in frontmatter

**STATE.md:**
- Update current phase to "Phase 1 — Onboarding Complete"
- Replace next steps with domain-specific actions based on discovery conversation
- Set `last_edited_by: agent_{username}` and `updated: <today>` in frontmatter

**CLAUDE.md:**
- If the user shared a project description in Step 5, update the project description in the Identity & Personality section (first paragraph after the personality block)
- Keep Berthier personality unless they choose otherwise in Step 8
- Set `last_edited_by: agent_{username}` and `updated: <today>` in frontmatter

### Step 8: Personality Customization Offer

Conversational offer — don't make it a big deal:

"I'm operating as Berthier — a structured, operations-focused chief of staff. I can help you design your own agent personality for this vault, or you can keep me as-is. What would you prefer?"

**If user wants custom:**
1. Ask for: name, archetype/inspiration, 3-4 operating style principles, greeting style
2. Edit the Identity & Personality section of CLAUDE.md (between `## Identity & Personality` header and the first `---` separator)
3. Show them the result before saving

**If user keeps Berthier:**
- Confirm and move on. No changes needed.

### Step 9: Marketplace Teaser

Brief mention — 2-3 sentences max:

"One more thing — what you build here has value beyond your project. Ontology extensions, lattice definitions, skills, and templates you create can eventually be published to the **Lattice Protocol marketplace** for others to discover, deploy, and build on — with agentic residuals flowing back to you. The marketplace is coming soon. For now, just know that everything you build here is portable and composable."

This is a teaser, not a tutorial. Don't oversell.

### Step 10: Next Steps and Session Close

Summarize what was configured during onboarding.

Suggest 3-4 concrete next steps tailored to the user's domain:
- Create a context entry in `what/context/` for a key domain topic
- Start a mission in `how/missions/` for their first real task
- Create or customize a lattice definition for a workflow they described
- Add team members or governance to `who/governance/`

Offer branching guidance based on the user's interests:

| Interest | Next step |
|----------|-----------|
| Building workflows or pipelines | See README § Your First Lattice for a hands-on walkthrough |
| Managing domain knowledge | Explore `what/context/AGENTS.md` for the context library system |
| Coordinating a team or multi-session work | Start a mission in `how/missions/` |
| Visual-first exploration | Open `what/lattices/examples/hello_world.canvas` in Obsidian |

This session IS the onboarding session — create the session file (or update if already created), log all files touched, close with a standard SITREP.

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Customized MANIFEST.md | File | Project identity updated |
| Customized STATE.md | File | Next steps updated |
| Customized CLAUDE.md | File | Project description (and optionally personality) updated |
| Domain directories | Directories | Ontology extensions with AGENTS.md files |
| Session file | File | Onboarding session record in history |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| User quits mid-onboarding | Session interrupted | Safe to resume — Steps 1-4 are conversational (no vault changes). Steps 5-9 check existing state before modifying. |
| Governance files already customized | Partial prior onboarding | Check what's already done, skip completed steps, resume from first incomplete step |
| User declines all extensions | No domain fit yet | That's fine — the base ontology works standalone. They can extend later. |
| User declines governance edits | Wants to do it manually | Respect the choice. Summarize what they'd need to edit and where. |

## Completion Markers

After successful onboarding:
- `MANIFEST.md` will have a non-init `last_edited_by` value
- `MANIFEST.md` will NOT have `role: template` (if it does, the fork procedure failed — strip it manually)
- A session file will exist in `how/sessions/history/`
- Both first-run indicators cleared — future sessions skip onboarding

## Related

- **Skills Protocol**: `how/skills/AGENTS.md`
- **CLAUDE.md**: First-run detection section
- **aDNA Standard**: `what/docs/adna_standard.md`
- **Bridge Patterns**: `what/docs/adna_bridge_patterns.md`
