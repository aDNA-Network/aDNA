---
type: context_research
topic: prompt_engineering
subtopic: claude_md_best_practices
created: 2026-02-19
updated: 2026-03-18
sources: ["Anthropic — Using CLAUDE.MD Files (blog)", "Anthropic — Claude Code Best Practices", "Anthropic — Claude 4 Best Practices", "HumanLayer — Writing a Good CLAUDE.md", "alexop.dev — Progressive Disclosure for AI Coding Tools"]
context_version: "1.0"
token_estimate: ~1500
last_edited_by: agent_init
tags: [context, prompt_engineering]
quality_score: 4.4
signal_density: 5
actionability: 5
coverage_uniformity: 4
source_diversity: 4
cross_topic_coherence: 4
freshness_category: mixed
last_evaluated: 2026-03-17
---

# Prompt Engineering: CLAUDE.md Best Practices

## Key Principles

1. **CLAUDE.md is system prompt, not documentation.** It loads into every session as persistent context. Every token in it competes with working context. Treat it as high-leverage, curated instructions — not a project wiki.

2. **Shorter is better.** Target <300 lines; <60 lines is ideal. A 2000-line CLAUDE.md consumes ~1.8% of a 200K token budget; a 50-line file uses only 0.25%. Research indicates frontier LLMs follow ~150-200 instructions with reasonable consistency — beyond that, adherence degrades uniformly.

3. **Only include what Claude can't infer.** For each line, ask: "Would removing this cause Claude to make mistakes?" If not, cut it. Claude can read your code, configs, and package files — don't restate what's already machine-readable.

4. **Progressive disclosure over front-loading.** Keep CLAUDE.md lean with pointers to detailed docs. Use `@path/to/file` imports, skills (`.claude/skills/`), and directory-level CLAUDE.md files to layer context that loads only when relevant.

5. **Match Claude 4.6 behavior.** Remove anti-laziness prompts ("be thorough", "think carefully") — these cause runaway thinking on Claude 4.6. Soften tool-use language ("Use X when helpful" not "You MUST use X"). Use the `effort` parameter instead of prompt-based intensity control.

## Recommendations

### What to Include

| Category | Examples |
|----------|---------|
| Bash commands Claude can't guess | `npm run test:unit`, custom build scripts, test runners |
| Code style that differs from defaults | Import style, naming conventions, type hint requirements |
| Testing instructions | Preferred frameworks, how to run single tests, verification commands |
| Repository etiquette | Branch naming, PR conventions, commit message format |
| Architectural decisions | Non-obvious patterns, module boundaries, tech choices |
| Environment quirks | Required env vars, non-standard paths, platform notes |
| Common gotchas | Non-obvious behaviors, known issues, edge cases |

### What to Exclude

| Category | Why |
|----------|-----|
| Code style enforceable by linters | "Never send an LLM to do a linter's job" — use ESLint/Prettier/ruff hooks instead |
| Standard language conventions | Claude already knows Python PEP 8, JS conventions, etc. |
| File-by-file codebase descriptions | Claude can read the code directly |
| Detailed API documentation | Link to docs instead of inlining |
| Frequently changing information | Will go stale; use dynamic loading |
| Sensitive information | API keys, credentials, connection strings |
| Self-evident practices | "Write clean code", "follow best practices" |

### File Hierarchy

CLAUDE.md files load hierarchically — more specific overrides more general:

| Location | Scope | Use Case |
|----------|-------|----------|
| `~/.claude/CLAUDE.md` | All projects for this user | Personal preferences, global tooling |
| `./CLAUDE.md` (project root) | All sessions in this project | Team conventions, project architecture |
| `./subdir/CLAUDE.md` | Sessions touching that directory | Domain-specific rules, module conventions |
| `.claude/CLAUDE.md` | Project (alternative location) | If you prefer config in a subdirectory |
| `CLAUDE.local.md` | Project, git-ignored | Personal overrides not shared with team |

Child CLAUDE.md files are pulled in on demand when Claude works with files in those directories.

### Progressive Disclosure Pattern

**Layer 1 — CLAUDE.md (always loaded):** Project overview, essential commands, stack info, pointers to specialized docs.

**Layer 2 — Referenced docs (on-demand):** Domain-specific knowledge loaded via `@` imports or explicit file reads. Examples: `testing-strategy.md`, `api-conventions.md`, architecture guides.

**Layer 3 — Skills (on-demand):** `.claude/skills/` directories with `SKILL.md` files. Claude loads them automatically when relevant, or invoke with `/skill-name`. Use for repeatable workflows and domain expertise.

Critical instruction to include in CLAUDE.md for Layer 2:
> "Before starting any task, identify which docs below are relevant and read them first."

### Structure Template

```markdown
# [Project Name]

## Overview
[1-2 sentences: what the project does, primary technologies]

## Architecture
[High-level directory map, key module boundaries]

## Commands
[Essential dev/test/build/lint commands]

## Code Style
[Only conventions that differ from language defaults]

## Workflow
[Branch naming, PR conventions, verification before commit]

## Gotchas
[Non-obvious behaviors, known pitfalls]

## Reference Docs
[@ imports or file pointers for domain-specific knowledge]
```

### Extending with Skills and Subagents

- **Skills** (`.claude/skills/SKILL.md`): Domain knowledge and repeatable workflows loaded on demand. Use `disable-model-invocation: true` for workflows with side effects.
- **Subagents** (`.claude/agents/`): Specialized assistants with scoped tools and their own context windows. Useful for isolated tasks like security review or code analysis.
- **Hooks** (`.claude/settings.json`): Deterministic scripts that run at specific points. Unlike CLAUDE.md instructions which are advisory, hooks guarantee execution.

## Anti-Patterns

- **The kitchen sink CLAUDE.md.** Too much content causes Claude to ignore critical rules. If Claude keeps violating a rule, the file is probably too long and the rule is getting lost.
- **Duplicating linter behavior.** Style rules in CLAUDE.md when ESLint/Prettier/ruff already enforce them create noise without benefit. Use hooks to run formatters after edits instead.
- **Static codebase descriptions.** File-by-file descriptions go stale immediately. Let Claude explore the code directly — it's trained for this.
- **Anti-laziness prompts.** On Claude 4.6, "be thorough" and "do not be lazy" amplify already-proactive behavior into runaway loops.
- **Assuming /init output is final.** `/init` generates a starting point, not a finished product. Review, prune, and refine based on actual Claude behavior.

## Sources

- [Using CLAUDE.MD Files: Customizing Claude Code](https://claude.com/blog/using-claude-md-files) — Anthropic (2025). Official guide: hierarchy, content recommendations, progressive disclosure.
- [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices) — Anthropic (2025). Comprehensive guide: CLAUDE.md, skills, subagents, hooks, scaling patterns.
- [Claude 4 Prompting Best Practices](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) — Anthropic (2025). Model-specific: effort parameter, anti-laziness, formatting.
- [Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) — HumanLayer (2025). Instruction limits (~150-200), what/why/how framework, length guidelines.
- [Progressive Disclosure for AI Coding Tools](https://alexop.dev/posts/stop-bloating-your-claude-md-progressive-disclosure-ai-coding-tools/) — alexop.dev (2025). Three-layer pattern, token math, /learn feedback loop.
