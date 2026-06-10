# OBSIDIAN_CLAUDE.md — AI Guide for Obsidian Interaction

This guide helps AI agents safely interact with the Obsidian configuration in an aDNA vault.

## Configuration Structure

```
.obsidian/
├── plugins/              # Community plugin installations
├── themes/              # UI themes (Tokyo Night active)
├── snippets/            # CSS customizations (2 bundles)
│   ├── core_theme.css   # Base visual identity
│   ├── editor_polish.css # Editor enhancements
│   └── archive/         # Original individual snippets
├── app.json             # Core app settings
├── appearance.json      # Theme, fonts, enabled snippets
├── community-plugins.json  # Plugin registry
├── core-plugins.json    # Core plugin enablement
├── hotkeys.json         # Keyboard shortcuts
└── OBSIDIAN_CLAUDE.md   # This file

# Vault root
.obsidianignore          # Watcher exclusions
```

### .obsidianignore

The `.obsidianignore` file at vault root tells Obsidian's file watcher to skip paths entirely — no FSEvents, no indexing. This is critical for vaults that contain or symlink git repos, build artifacts, or large binary directories. Without it, Obsidian monitors thousands of irrelevant files.

**Agent rule**: If new git repos or large artifact directories are added to the vault, add them to `.obsidianignore`.

### Per-Device Files

These files are excluded from git (`.gitignore`) because they contain machine-specific state:
- `workspace.json` — window layout, open tabs
- `workspace-mobile.json` — mobile layout
- `graph.json` — graph view settings

**Agent rule**: Never attempt to maintain or sync these files. Each machine keeps its own state.

## Safety Rules

1. **NEVER** modify `app.json` or `appearance.json` without explicit user permission
2. **ALWAYS** backup configuration files before modification
3. **NEVER** delete plugin folders — disable in `community-plugins.json` instead
4. **ALWAYS** validate JSON syntax before saving
5. **NEVER** modify `workspace.json` while Obsidian is running

## Plugins (14 community plugins)

### Essential (vault functionality depends on these)

| Plugin | ID | Purpose | Config Notes |
|--------|----|---------|-------------|
| Dataview | `dataview` | Query frontmatter with TABLE/LIST/TASK | Use WHERE + LIMIT for performance |
| Templater | `templater-obsidian` | Template engine with folder auto-triggers | 10 folder→template mappings |
| Notebook Navigator | `notebook-navigator` | Folder-based notebook nav with icons + folder notes | Triad colors configured. `folderNoteName: AGENTS` — folder notes are `AGENTS.md`, not `README.md` |

### Recommended (significant UX improvement)

| Plugin | ID | Purpose | Config Notes |
|--------|----|---------|-------------|
| Meta Bind | `obsidian-meta-bind-plugin` | Inline metadata editing | Buttons, inputs, embeds |
| Homepage | `homepage` | Set start page on vault open | Configured in plugin data.json |
| Style Settings | `obsidian-style-settings` | GUI controls for CSS snippet options | Required for @settings blocks |
| Icon Folder | `obsidian-icon-folder` | Custom folder/file icons | Triad folder icons |
| Advanced Canvas | `advanced-canvas` | Extended canvas features | Groups, portals, styles |
| BRAT | `obsidian42-brat` | Beta plugin manager | Auto-installs/updates Termy |

### Optional (nice-to-have)

| Plugin | ID | Purpose | Config Notes |
|--------|----|---------|-------------|
| Tasks | `obsidian-tasks-plugin` | Task tracking with queries | Global task search |
| Table Editor | `table-editor-obsidian` | Better markdown table editing | Tab-based navigation |
| Termy | `termy` | Terminal with preset scripts | 3 agent CLI presets (Claude Code, Codex, Gemini) |
| Pretty Properties | `pretty-properties` | Polished property display | Renders frontmatter |
| Fold Properties | `fold-properties-by-default` | Auto-fold frontmatter | Cleaner reading view |

### Templater Folder Mappings

Templater auto-applies templates when creating files in mapped directories:

| Folder | Template |
|--------|----------|
| `what/context` | `template_context.md` |
| `what/decisions` | `template_adr.md` |
| `how/sessions/active` | `template_session.md` |
| `how/missions` | `template_mission.md` |
| `who/coordination` | `template_coordination.md` |
| `how/backlog` | `template_backlog.md` |
| `how/campaigns` | `template_campaign.md` |
| `how/skills` | `template_skill.md` |
| `how/pipelines/prd_rfc/02_requirements` | `template_prd.md` |
| `how/pipelines/prd_rfc/03_design` | `template_rfc.md` |

### Plugin Interaction Patterns

**Dataview queries** — always include `WHERE` for performance:
```dataview
TABLE status, created FROM "who" WHERE type = "customer" SORT created DESC
```

**Meta Bind inputs** — inline metadata editing:
```meta-bind
INPUT[text:status]
```

**Templater functions** — dynamic template content:
```
<% tp.date.now("YYYY-MM-DD") %>
<% tp.file.title %>
```

## CSS Snippet Architecture

### Bundles (2)

| Bundle | Contents | Lines | Style Settings |
|--------|----------|-------|---------------|
| `core_theme.css` | Tokyo Night purple accent, headings, links, code blocks, scrollbar, modals | ~450 | 10 controls |
| `editor_polish.css` | Table stripes, mermaid override, popover size, notebook navigator, callouts, tag contrast | ~350 | 4 controls |

### Style Settings Integration

Both bundles include `/* @settings */` blocks that expose controls in Style Settings GUI (Settings → Style Settings). Users can toggle features without editing CSS.

Available controls:
- **Headings**: center H1, H2 accent border, heading scale
- **Links**: external link arrow, unresolved link dashed underline
- **Code blocks**: border width, border color, tinted inline code
- **Scrollbar**: thumb color, width, track visibility
- **Modals**: blur intensity, accent border
- **Notebook Navigator**: nav background, selected accent, triad colors

### Theme

**Tokyo Night** with **Rebecca Purple** (`#663399`) accent. Installed by `setup.sh` or manually from Settings → Appearance → Themes.

**Font (optional)**: [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk) for a polished look.

## Content Patterns

### Frontmatter Standard

All content files require YAML frontmatter:
```yaml
---
type: <entity_type>
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active|completed|deprecated
last_edited_by: agent_<username>
tags: []
---
```

### Naming Convention

**Always underscores, never hyphens.** Pattern: `type_descriptive_name.md`

### Wikilinks

Use `[[filename]]` for internal links. Obsidian auto-updates links on file rename.

## Triad Architecture

The vault follows the aDNA triad: `who/` (people, orgs) + `what/` (knowledge, objects) + `how/` (operations, processes). This maps to the organizational primitives:

| Directory | Color | Purpose |
|-----------|-------|---------|
| `who/` | Purple (#9d7cd8) | People, organizations, governance |
| `what/` | Cyan (#7dcfff) | Knowledge, models, datasets, lattices |
| `how/` | Green (#9ece6a) | Operations, campaigns, missions, skills |
