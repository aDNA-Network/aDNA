---
type: pattern
created: 2026-05-29
updated: 2026-07-03
status: active
pattern_category: structural   # 5-block layout is structural; activation discipline is operational; primary register is structural per first-contact UX framing
applies_to: [campaigns, missions, sessions, governance, team]
last_edited_by: agent_stanley
tags: [pattern, lattice_home, splash, terminal, cold_start, ascii_render, four_tier_pipeline, dual_gated_activation, vault_portable]
---

# Lattice Home — Terminal Cold-Start Splash Pattern

## Problem

Every aDNA vault opens to an empty terminal. An agent or operator dropping in pays a **discovery tax** to learn what is open, what is recent, what capabilities are wired, and what keybindings exist. The tax compounds across sessions — the same `ls` + `git status` + `grep "status: in_progress"` is re-paid every cold-start.

Worse, the cold-start is silent in a way that fails the dual-audience test: agents see nothing structured to orient against; humans see no welcome, no breadcrumbs, no "where am I." First-contact UX is one of the weakest surfaces in a bare vault.

The pattern generalizes across vaults: any aDNA vault can ship the same surface with bash + awk and zero runtime dependencies.

## Solution

Render a **5-block ASCII splash** at terminal cold-start through a **4-tier single-source pipeline**, **dual-gated** for safety:

### 5-block layout schema

| Block | Content | Width |
|---|---|---|
| **Header** | `{{NODE_ID}} · {{OPERATOR}}` left + `{{VAULT_BADGE}} {{VAULT_NAME}}` right; `{{BRANCH}} ↑N ↓N upstream / ⚠ N uncommitted` git status line | full row |
| **OPEN MISSIONS** | grep-stub list of `status: planned\|in_progress\|active` missions; capped at 5 entries | full row |
| **RECENT** | mtime-sorted last 3 `status: completed` missions with date column | full row |
| **CAPABILITY** | provider probe (`command -v <agent-cli>`) + MCP / theme / graphics probes; cheap stubs with `(probe → …)` markers for unfinished | full row |
| **Keybinding hint** | `SPC g graph · m mission · t theme · p promote · b browser · ?` (ornamental at splash time; wired to TUI later) | full row |

### 4-tier single-source pipeline

```
dossier (design intent + placeholder spec)
   ↓
template (canonical ASCII fence-pair with {{PLACEHOLDER}} markers)
   ↓
graph-local state symlink (vault → user XDG / Application Support)
   ↓
`lattice <verb>` CLI (bash + awk extractor; placeholder substitution)
```

Each tier has exactly one source-of-record; downstream tiers reference upstream via symlink or grep. Edits at one tier propagate to all consumers without per-consumer maintenance.

### Dual-gated activation

The splash fires automatically on **interactive shell start**, but only if **both** gates pass:

1. **Environment gate** — a `<VAULT>_LATTICE` env var defaults to ON; explicit `<VAULT>_LATTICE=0` suppresses (operator escape hatch).
2. **Graph-root gate** — PWD walks up looking for the vault's identity stub (`node.adna.yaml`, `MANIFEST.md`, or equivalent); if absent, splash silently no-ops.

Both gates are silent on miss (`return 1`, not error). The splash never blocks terminal-open and never speaks unless invited.

### Fallback discipline

Every placeholder has a documented fallback for missing data:

| Placeholder | Fallback | Trigger |
|---|---|---|
| `NODE_ID` / `OPERATOR` | `?` | YAML stub missing or unreadable |
| `BRANCH` | `(detached or no repo)` | git rev-parse fails |
| `UPSTREAM_STATUS` | `local-only` | no upstream set |
| `OPEN_MISSIONS` / `RECENT` | `(none)` | grep returns empty |
| `PROVIDERS` | `claude-code ◌` (pending glyph) | `command -v` returns non-zero |

## When to Use

- **Any aDNA vault** where the operator wants an at-a-glance state summary at terminal open
- **Standalone Lattice terminals** opening in a vault's graph root
- **Multi-vault workspaces** where each vault should self-identify on cold-start (avoids the "which graph am I in?" tax)
- **NOT** for sub-directories of a vault (the graph-root gate intentionally prevents pollution)
- **NOT** for non-interactive shells / CI runners (the interactive-shell gate prevents accidental splash in scripts)

## Example

A canonical instance lives at `<Vault>.aDNA/how/configs/bin/lattice` (`cmd_home()`): ~75 LoC of pure bash + awk, sub-second render, idempotent install. It activates via a `<VAULT>_LATTICE` env gate + a graph-root walk for the vault's identity stub, and renders a persona-flavored header (`{{VAULT_BADGE}} <Vault> / {{persona}}`), a mission grep over `how/campaigns/*/missions/*.md`, and vault-specific capability stubs. To adopt, run the install skill (below) — it lifts and parameterizes the recipe rather than copying it verbatim.

**Self-reference**: this pattern doc lives under the `pattern` ontology extension in `what/patterns/`; the surface where the pattern is documented is the same surface where it is installed. The vault is the textbook — the pattern is demonstrated in the graph that ships it.

## Anti-Pattern

| What | Why it breaks |
|---|---|
| **Global shell hook with no graph-root gate** | Pollutes every terminal regardless of cwd; operator sees splash in `/tmp` and `$HOME`; gate-of-last-resort fails |
| **Runtime dependency beyond bash + awk** | Node / Python / Go requirements break the portability promise; pure-bash discipline keeps the pattern viable across nodes |
| **Inline ANSI color codes** | Color choices drift from the vault's semantic-role tokens; reference the palette by role, never embed hex |
| **Blocking probe** | Splash that calls a remote LLM or slow MCP probe blocks terminal-open; cheap `command -v` + `git rev-parse` discipline keeps render sub-second |
| **Verbose multi-screen render** | 5 blocks × full-width is the cap; anything more violates the "at-a-glance state summary" promise; richer data belongs in `lattice <other-verb>` subcommands |
| **Per-vault code copy without parameterization** | Splashes drift across vaults if each copies the bash verbatim; the install skill enforces lift + parameterize, not copy |
| **Splash as canonical AAR substitute** | The splash is a recap surface; it does NOT discharge Standing Order #5 (every mission gets an AAR). The splash augments an AAR, never replaces it |

## Cross-references

- [[skill_lattice_home_install]] — the install recipe
- [[template_lattice_home_render]] — the canonical ASCII template
- [[pattern_dual_audience]] — sibling pattern the splash satisfies (humans see welcome; agents see structured state)
