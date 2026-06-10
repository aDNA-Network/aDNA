# .obsidian/ — Obsidian Configuration

This directory contains Obsidian vault configuration. Most files are checked into git to ensure a consistent experience across clones.

> **Quick setup**: Run `./setup.sh` from the repo root to download all plugins and the theme automatically.

## Plugins (15 community plugins)

| Plugin | ID | Purpose |
|--------|----|---------|
| Dataview | `dataview` | Query and display structured data from frontmatter |
| Templater | `templater-obsidian` | Template engine with folder-based auto-triggers |
| Meta Bind | `obsidian-meta-bind-plugin` | Inline metadata editing |
| Homepage | `homepage` | Set a start page on vault open |
| Tasks | `obsidian-tasks-plugin` | Task tracking with queries |
| Style Settings | `obsidian-style-settings` | Customize CSS snippet options via GUI |
| Table Editor | `table-editor-obsidian` | Better markdown table editing |
| Omnisearch | `omnisearch` | Vault-wide fuzzy search |
| Terminal | `terminal` | Terminal access from Obsidian |
| Folder Notes | `folder-notes` | Index files for folder navigation |
| Notebook Navigator | `notebook-navigator` | Folder-based notebook navigation with icons |
| Icon Folder | `obsidian-icon-folder` | Custom folder/file icons (triad colors) |
| Advanced Canvas | `obsidian-advanced-canvas` | Extended canvas features (groups, portals) |
| Pretty Properties | `pretty-properties` | Polished frontmatter property display |
| Fold Properties | `fold-properties-by-default` | Auto-fold frontmatter in reading view |

## Theme

**Tokyo Night** — installed by `setup.sh`, or manually from Settings → Appearance → Themes.

**Font (optional)**: Install [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk) for a polished look. The vault uses system default fonts out of the box — Space Grotesk can be set in Settings → Appearance → Font after installation.

**Accent**: Rebecca Purple (`#663399`) — configured in `appearance.json`.

## CSS Snippets (2 bundles)

Consolidated from 10 individual snippets into 2 bundles. All enabled in `appearance.json`. Originals preserved in `snippets/archive/`.

| Bundle | Contents | Style Settings |
|--------|----------|---------------|
| `core_theme.css` | Tokyo Night purple accent, headings, links, code blocks, scrollbar, modals | 10 controls |
| `editor_polish.css` | Table stripes, mermaid override, popover size, notebook navigator, callouts, tag contrast | 4 controls |

All `/* @settings */` blocks are preserved — configure visual options via Settings → Style Settings.

## Per-Device Files

These files are excluded from git (see `.gitignore`) because they contain machine-specific state:

- `workspace.json` — window layout, open tabs
- `workspace-mobile.json` — mobile layout
- `graph.json` — graph view settings

## Templater Folder Mappings

Templater is configured to auto-apply templates when creating new files in specific directories (10 mappings). See `plugins/templater-obsidian/data.json` for the full list.

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

## Agent Documentation

See `OBSIDIAN_CLAUDE.md` in this directory for AI agent interaction guidelines, plugin documentation, and safety rules.
