# CLAUDE.md — aDNA Projects Workspace

This is a **multi-project workspace**, not a project. Each subdirectory (except `.base/` and `shared/`) is a self-contained aDNA vault.

## Your Job

When a user asks to create a new project, run the interview below, then scaffold using `.base/` templates.

## Pre-Flight Interview (5 Questions)

Ask these sequentially. Record the answers — they drive template variable resolution.

### Q1: What are you building?
Free text. Maps to `{{project_description}}`.

### Q2: What's your domain?
Options: `research`, `enterprise`, `biotech`, `software`, `creative`, `personal`, `healthcare`, `legal`, `content`, `other`.
Maps to `{{domain}}`. Suggests ontology extensions:

| Domain | Extensions |
|--------|-----------|
| research | `what/papers/`, `what/datasets/`, `what/hypotheses/`, `what/experiments/` |
| enterprise | `who/customers/`, `who/partners/`, `who/contacts/`, `who/projects/` |
| biotech | `what/experiments/`, `what/compounds/`, `what/protocols/`, `what/targets/` |
| software | `how/incidents/`, `how/deployments/`, `what/services/`, `what/apis/` |
| creative | `who/clients/`, `what/creative_assets/`, `how/revision_cycles/` |
| personal | `what/courses/`, `what/books/`, `how/learning_goals/` |
| healthcare | `who/patients/`, `what/treatments/`, `what/protocols/` |
| legal | `what/cases/`, `what/contracts/`, `what/compliance/` |
| content | `what/publications/`, `how/editorial_pipeline/`, `what/assets/` |

Show the user the suggested extensions for their domain. Ask: "Include these? (Y/n)". For `other`, ask: "Name 2-3 entity types you'll manage."

### Q3: Team or solo?
Options: `solo`, `small-team` (2-5), `organization` (5+).
Maps to skeleton tier:
- **solo** → Starter (CLAUDE.md + MANIFEST.md + README.md + triad + minimal subdirs)
- **small-team** → Standard (adds STATE.md, AGENTS.md chain, sessions with active/history, backlog, coordination)
- **organization** → Full (Standard + governance, collision prevention Tier 3, domain extensions)

### Q4: How will you browse the vault?
Options: `obsidian`, `terminal-only`, `vs-code`, `other`.
Maps to `{{tooling}}`. If `obsidian`, note that they should set up `.obsidian/` manually or via the aDNA repo's `setup.sh`. If `terminal-only` or `vs-code`, skip any `.obsidian/` references.

### Q5: Agent personality?
Options: `berthier` (structured chief of staff, default), `custom` (ask for name + 3 operating principles), `none` (functional only).
Maps to `{{persona_name}}` and `{{persona_style}}`.

## Scaffolding Steps

After the interview:

1. **Create the project directory** using the user's chosen name (ask if not provided). Use underscores for spaces.
2. **Copy each `.base/*.template` file** into the new directory, removing the `.template` extension.
3. **Resolve all `{{variables}}`** in the copied files with interview answers:
   - `{{project_name}}` — directory name
   - `{{project_description}}` — Q1 answer
   - `{{domain}}` — Q2 answer
   - `{{persona_name}}` — Q5 answer (or "Berthier" if default)
   - `{{persona_style}}` — Q5 operating principles (or Berthier defaults)
   - `{{created_date}}` — today's date (YYYY-MM-DD)
4. **Create triad directories** (`who/`, `what/`, `how/`) with AGENTS.md in each.
5. **Create standard subdirs** per skeleton tier (see Q3 mapping above).
6. **Create domain extensions** per Q2 answer (if user confirmed).
7. **Create an onboarding session file** at `how/sessions/active/session_onboarding.md` recording interview answers, files created, and suggested next steps.

## Rules

- Never modify `.base/` templates during scaffolding — they are the fork source.
- Never modify other project directories when scaffolding a new one.
- Each project must work standalone — no dependencies on the workspace root.
- `shared/` is optional and user-managed. Don't create it unless asked.
