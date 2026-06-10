---
type: context_research
topic: prompt_engineering
subtopic: agentic_scaffolding
created: 2026-02-19
updated: 2026-03-18
sources: ["Anthropic — Effective Context Engineering for AI Agents", "Anthropic — Claude Code Best Practices", "Anthropic — Agent Skills (blog)", "agents.md — Open Format Specification", "Anthropic — Claude 4 Best Practices"]
context_version: "1.0"
token_estimate: ~1500
last_edited_by: agent_init
tags: [context, prompt_engineering]
quality_score: 4.4
signal_density: 4
actionability: 5
coverage_uniformity: 4
source_diversity: 4
cross_topic_coherence: 4
freshness_category: mixed
last_evaluated: 2026-03-17
---

# Prompt Engineering: Agentic Project Scaffolding

## Key Principles

1. **Agents navigate repos through governance files, not exploration.** A well-structured repo lets agents orient in seconds via a chain of governance files (CLAUDE.md → AGENTS.md → directory-level AGENTS.md) rather than reading hundreds of files to build a mental model. Every directory should answer: "What is this? Should I load it?"

2. **Two audiences, two files.** README.md is for humans (quick starts, project description, contribution guides). AGENTS.md is for agents (build commands, test procedures, conventions, architectural decisions). Keeping them separate prevents bloating either audience's context.

3. **Progressive disclosure through directory hierarchy.** Root-level governance provides orientation; directory-level files provide depth. The agent cold-start chain is: root CLAUDE.md/AGENTS.md → relevant directory AGENTS.md → specific files. Each level narrows context, reducing tokens while increasing signal.

4. **Naming conventions are navigation.** Consistent file naming patterns (`type_descriptive_name.md`, `context_{topic}_{subtopic}.md`) let agents predict file locations without searching. Naming is the cheapest form of agent navigation.

5. **Skills as loadable capabilities.** Agent skills (`.claude/skills/SKILL.md`) package domain knowledge into discoverable, on-demand modules. Three-tier loading: metadata always available → core instructions when relevant → supplementary files when needed.

6. **Externalize prompts from code.** Store prompts, agent instructions, and operational knowledge as markdown files in the repo — not embedded in application code. This enables non-technical stakeholders to update agent behavior and makes instructions version-controlled and auditable.

## Recommendations

### Repository Structure Pattern

```
project/
├── CLAUDE.md              # Agent master context (always loaded)
├── AGENTS.md              # Agent-focused conventions (alternative to CLAUDE.md for multi-tool compat)
├── README.md              # Human-focused documentation
├── .claude/               # Claude Code configuration
│   ├── settings.json      # Permissions, hooks
│   ├── skills/            # On-demand agent capabilities
│   │   └── skill_name/
│   │       └── SKILL.md
│   └── agents/            # Custom subagent definitions
│       └── reviewer.md
├── who/                   # People, organizations, governance
│   ├── AGENTS.md          # Directory-level agent instructions
│   └── ...
├── what/                  # Knowledge, technical objects
│   ├── AGENTS.md
│   └── context/           # Context library
│       ├── AGENTS.md      # Topic index with token estimates
│       └── {topic}/
│           ├── AGENTS.md  # Subtopic index
│           └── context_{topic}_{subtopic}.md
└── how/                   # Operations, processes, sessions
    ├── AGENTS.md
    └── ...
```

### Agent Cold-Start Chain

The critical path an agent follows when first encountering a repo:

| Step | File | Purpose | Token Budget |
|------|------|---------|-------------|
| 1 | `CLAUDE.md` or `AGENTS.md` | Identity, architecture, commands, conventions | ~200-500 tokens |
| 2 | State file (e.g., `STATE.md`) | Current operational context, active work | ~300-800 tokens |
| 3 | Relevant directory AGENTS.md | What this area contains, how to use it | ~100-300 tokens each |
| 4 | Specific content files | Actual work material | As needed |

Design the chain so each step tells the agent whether to go deeper or stop. An agent should reach productive work in 3-4 file reads.

### AGENTS.md Design Patterns

**Root AGENTS.md** — project overview, build/test commands, code style, PR conventions, security notes.

**Directory AGENTS.md** — what this directory contains, file naming patterns, relationships to other directories, when to load this content.

**Topic Index AGENTS.md** — subtopic inventory with token estimates, loading guidance ("load X for task Y"), version and source counts.

Key content per AGENTS.md:

| Section | Purpose |
|---------|---------|
| Overview | 1-2 sentences: what and why |
| Contents | What files/subdirectories exist here |
| Conventions | Naming, formatting, type standards |
| Relationships | Links to related directories |
| Token estimate | Cost to load this area |
| Usage guidance | When an agent should/shouldn't load this |

### Governance File Hierarchy

| File | Scope | Agent Behavior |
|------|-------|---------------|
| `CLAUDE.md` | Whole project, always loaded | Identity, rules, architecture map |
| `AGENTS.md` (root) | Whole project, tool-agnostic | Build commands, conventions (AGENTS.md spec) |
| `AGENTS.md` (directory) | Single directory, loaded on demand | Contents, naming, relationships |
| `SKILL.md` | Single capability, loaded on demand | Executable workflow, domain knowledge |
| `STATE.md` | Operational state, loaded at session start | Active work, blockers, next steps |

### Skills Architecture

```
.claude/skills/
└── skill_name/
    ├── SKILL.md           # Core instructions (YAML frontmatter + markdown)
    ├── helpers/            # Scripts the skill can execute
    │   └── validate.py
    └── templates/          # Reference templates
        └── template.md
```

- `SKILL.md` frontmatter: `name`, `description`, optional `disable-model-invocation: true`
- Skill metadata is pre-loaded into system prompt; full content loads when Claude determines relevance
- Bundle executable scripts alongside docs — deterministic operations without token-expensive LLM alternatives
- Use `disable-model-invocation: true` for workflows with side effects (deploy, commit, push)

### Subagent Definitions

```markdown
# .claude/agents/security-reviewer.md
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
[Specialized instructions...]
```

Subagents run in isolated context windows with scoped tools. Use for: security review, code analysis, research tasks, verification — anything where exploration would bloat the main conversation.

## Anti-Patterns

- **No governance files.** Agent must explore the entire repo on every session. Massive token waste, inconsistent orientation.
- **README as agent instructions.** Mixing human and agent audiences dilutes both. Agents need build commands and conventions; humans need quick-start guides.
- **Flat directory structures.** No hierarchy means no progressive disclosure. Agent loads everything or nothing. Use directories with AGENTS.md files to create natural load boundaries.
- **Implicit naming conventions.** If file naming is inconsistent, agents can't predict locations and must search. Codify patterns in AGENTS.md.
- **Monolithic skill files.** A 2000-line SKILL.md defeats progressive disclosure. Split into core instructions plus referenced supplementary files.
- **Missing token estimates.** Without knowing the cost to load a directory or topic, agents can't budget their context window.

## Sources

- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic (2025). Just-in-time context, progressive disclosure, sub-agent architectures.
- [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices) — Anthropic (2025). CLAUDE.md, skills, subagents, hooks, project configuration.
- [Equipping Agents with Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills) — Anthropic (2025). Skill file structure, progressive disclosure, code execution within skills.
- [AGENTS.md Specification](https://agents.md/) — agents.md (2025). Open format for coding agents. 60,000+ repos. Sections, placement, precedence rules.
- [Claude 4 Prompting Best Practices](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) — Anthropic (2025). Subagent orchestration, parallel tools, exploration patterns.
