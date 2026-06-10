---
type: folder_note
tier: 1
folder_path: adna
created: 2026-03-02
updated: 2026-04-03
status: active
last_edited_by: agent_init
tags: [folder-note, adna, git-repo]
icon: dna
cssclasses: [folder-note]
---

# aDNA

> [!abstract] Definition
> Agentic DNA — a standalone **knowledge architecture template** (MIT) for AI-native vaults. Obsidian + Claude Code, zero proprietary dependencies. Version 2.1, triad structure (who/what/how), 19 canonical I/O types, FAIR metadata, Canvas Standard v1.0.0.
>
> **GitHub**: [LatticeProtocol/Agentic-DNA](https://github.com/LatticeProtocol/adna) · **License**: MIT · **Stack**: Obsidian / Claude Code / Python 3.10+

## Triad Structure

| Directory | Purpose | Contents |
|-----------|---------|----------|
| `who/` | Organization | Team, governance, coordination |
| `what/` | Knowledge | Context library, modules, lattices, datasets |
| `how/` | Operations | Missions, sessions, skills, pipelines, templates |

## Navigation

> [!info] WHO
> Organization layer — team, governance, coordination.
> `who/`

> [!info] WHAT
> Knowledge layer — context library, modules, lattices, datasets.
> `what/`

> [!info] HOW
> Operations layer — missions, sessions, skills, pipelines, templates.
> `how/`

## Key Files

| File | Purpose |
|------|---------|
| [[adna/README\|README.md]] | Public documentation — quick-start guide |
| [[adna/CLAUDE\|CLAUDE.md]] | Agent governance (v6.0) — rules, safety, protocol |
| [[adna/MANIFEST\|MANIFEST.md]] | Project identity, architecture, entry points |
| [[adna/STATE\|STATE.md]] | Build state and operational snapshot |
| `setup.sh` | First-run bootstrap script |

## Lattice Tools

| Tool | Purpose |
|------|---------|
| `lattice_validate.py` | Validate `.lattice.yaml` against schema |
| `lattice2canvas.py` | Convert `.lattice.yaml` → Obsidian `.canvas` |
| `canvas2lattice.py` | Convert `.canvas` → `.lattice.yaml` (round-trip) |

## Related

- [[lattice-protocol|Lattice Protocol]] — open-source protocol foundation
- [[latlab/latlab|LatLab]] — product SDK built on the protocol
- [[who/who|Organization]] — vault people layer
- [[what/what|Technical Objects]] — vault knowledge layer
- [[how/how|Operations]] — vault operations layer
