#!/usr/bin/env python3
"""build_topology_canvas.py — M24 node topology canvas generator.

Spatial twin of build_curation_cards.py. Reads, never writes, upstream sources; emits
what/canvas/topology.canvas (Obsidian Advanced Canvas) projecting the node's structure:

  nodes  ← inventory_vaults.yaml         (39 vaults, auto-categorized) + the WHO/WHAT/HOW triad
  federation edges ← on-disk wrapper probe (iii/, siteforge/, … — read-only, like the curation
                                            image probe)
  structural edges ← what/canvas/topology_relationships.yaml (succession · kinship · sequencing)
  node annotations ← topology_relationships.yaml code_repo map (⛓ sibling repo / code-as-WHAT)

Hotspots are IN-VAULT because Obsidian's vault root is Home.aDNA/ and the 39 sibling vaults live
outside it: each vault node wikilinks to its M22 curation card (who/curation/curation_<name>.md),
which links onward to the real CLAUDE/MANIFEST/STATE. Triad nodes → <leg>/<entity>/AGENTS.md;
meta node → STATE.md. The canvas is the spatial index into the §Gallery.

Built on the `canvas_core` CanvasBuilder substrate — owned by Canvas.aDNA since the CanvasForge→Canvas
merge (PT pt09); the node is a consumer of that canvas-generation library (see what/canvasforge/CLAUDE.md).
Substrate code relocation INTO Canvas.aDNA is pending PT P5 (ADR-004: lands at what/production/canvas_core;
resolves via the CanvasForge.aDNA archive shim until then). We gain schema validate(), spatial overlap/containment checks, and a
deterministic sync hash; the topology-specific orchestration (inventory → categories → federation probe →
2-zone layout) stays here.

Deterministic: output is a pure function of the two input files (fixed date + explicit node ids;
no wall-clock), so re-runs don't churn git. Do NOT hand-edit topology.canvas — edit the
inputs/this script and rebuild.

Usage (needs PyYAML + the canvas_core substrate — on this node use `python` 3.12.2, not `python3`):
    python what/code/build_topology_canvas.py            # write the canvas
    python what/code/build_topology_canvas.py --check    # validate only (schema + overlaps), no write
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import warnings
from pathlib import Path

import yaml

# ── Paths (vault-relative; resolved from this file's location) ────────────────
NODE_VAULT = Path(__file__).resolve().parents[2]              # Home.aDNA/
WORKSPACE = NODE_VAULT.parent                                 # ~/aDNA/
INVENTORY = NODE_VAULT / "what" / "inventory" / "inventory_vaults.yaml"
RELATIONSHIPS = NODE_VAULT / "what" / "canvas" / "topology_relationships.yaml"
CURATION_DIR = NODE_VAULT / "who" / "curation"
CREST_DIR = NODE_VAULT / "who" / "assets" / "crests"
SIGIL_DIR = NODE_VAULT / "who" / "assets" / "sigils"
EMBLEM_DIR = NODE_VAULT / "who" / "assets" / "emblems"
OUT = NODE_VAULT / "what" / "canvas" / "topology.canvas"

# canvas_core substrate (CanvasBuilder + spatial) — owned by Canvas.aDNA since the CanvasForge→Canvas merge
# (PT pt09); consumed per what/canvasforge/CLAUDE.md. Canonical home FIXED by Canvas.aDNA ADR-004 (Mondrian,
# 2026-06-19): `Canvas.aDNA/what/production/canvas_core/` — the code physically relocates there at PT P5;
# until then it resolves from the `CanvasForge.aDNA` archive shim. Import name unchanged (location-only move).
# ★ canvas_core hard-imports canvas_std (a SEPARATE lib at Canvas.aDNA/what/code/canvas_std), so we put BOTH
# on sys.path (ADR-004 §4) — else the canvas silently never renders on a fresh node. Locator (override →
# canonical → interim): $CANVAS_CORE_HOME → $CANVASFORGE_CODE (deprecated alias) → Canvas.aDNA/what/production
# (P5+) → CanvasForge.aDNA archive (pre-P5). Set $CANVAS_CORE_HOME if canvas_core lives elsewhere on your node.
_canvas_prod = WORKSPACE / "Canvas.aDNA" / "what" / "production"
CANVAS_CORE_HOME = Path(
    os.environ.get("CANVAS_CORE_HOME")
    or os.environ.get("CANVASFORGE_CODE")                          # deprecated alias
    or (_canvas_prod if (_canvas_prod / "canvas_core").is_dir()    # P5+ canonical home
        else WORKSPACE / "CanvasForge.aDNA" / "what" / "code")     # interim: archive shim (pre-P5)
)
if os.environ.get("CANVASFORGE_CODE") and not os.environ.get("CANVAS_CORE_HOME"):
    warnings.warn("CANVASFORGE_CODE is deprecated; use CANVAS_CORE_HOME", DeprecationWarning)
# canvas_core AND its canvas_std dependency must both resolve (ADR-004 §4 resolution rule).
CANVAS_STD_SRC = WORKSPACE / "Canvas.aDNA" / "what" / "code" / "canvas_std" / "src"
for _p in (CANVAS_CORE_HOME, CANVAS_STD_SRC):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
try:
    from canvas_core.core import CanvasBuilder
    from canvas_core import spatial
except ImportError as exc:  # pragma: no cover - environment guard
    sys.exit(
        f"ERROR: cannot import the canvas_core substrate (looked in {CANVAS_CORE_HOME}).\n"
        f"  ({exc}). Owned by Canvas.aDNA at what/production/canvas_core (ADR-004; lands at PT P5;\n"
        f"  interim via the CanvasForge.aDNA archive). Set $CANVAS_CORE_HOME, ensure `adna-canvas-std`\n"
        f"  is importable, or skip the topology canvas (optional). Run with `python` (3.12.2)."
    )

# Fixed build date (determinism discipline, mirrors build_curation_cards.py).
# Portability (M25): a fresh node sets its own via $TOPOLOGY_GENERATED_DATE; the default
# keeps this node's canvas byte-stable.
GENERATED_DATE = os.environ.get("TOPOLOGY_GENERATED_DATE", "2026-05-31")

EXCLUDE = {"ComicForge.aDNA"}  # superseded/off-disk; also excluded by the curation builder

# ── Category taxonomy (topology-tuned; standard_dev folds into Org-Vault to match the
#    curation builder + HOME §Vaults convention) ────────────────────────────────
CLASS_TO_CATEGORY = {
    "forge": "Forge",
    "framework": "Framework",
    "framework_candidate": "Framework",
    "platform": "Platform",
    "org_vault": "Org-Vault",
    "standard_dev": "Org-Vault",
    "org_graph": "Org-Graph",
    "network": "Network",
    "coordination": "Coordination",
    "node_operational": "Node & Tooling",
    "document": "Node & Tooling",
    "knowledge_graph": "Node & Tooling",
    "tooling": "Node & Tooling",
    "workspace": "Node & Tooling",
}
# Band stacking order. M2.2 de-spaghetti: band order is the PRIMARY node-placement lever (the only
# de-spaghetti that renders — AC won't reroute generated edges). The producer spine (Framework +
# Forge = all 8 federation hubs) sits lower-middle with the heavy consumers (Org-Vault: ZenZachary
# deg-7 / ScienceStanley deg-5) directly below and the lighter consumer bands above, so federation
# edges fan IN to a central spine instead of all reaching to the top. Frozen from an offline
# exhaustive search (routing_metrics crossings 154 → 85, −45%; every top-order shares the
# …Org-Graph, Framework, Forge, Org-Vault tail, and this one preserves the consumer bands' prior
# relative order). The Forge-first narrative costs +36 crossings (best 121) → not chosen. The reorder
# is operator-gated (Standing Order #1); reverting to Forge-first keeps barycenter but ~no de-spaghetti.
CATEGORY_ORDER = [
    "Platform", "Network", "Coordination", "Node & Tooling",
    "Org-Graph", "Framework", "Forge", "Org-Vault",
]
# Category hues — Tokyo Night accent family, cyberpunk-pushed (M25.5 aesthetic pass), tuned for
# legibility as node tints on the #16161e ground. One distinct hue per pattern category.
CATEGORY_COLOR = {
    "Forge": "#ff9e64",          # orange — fire/metal
    "Framework": "#bb9af7",      # purple
    "Platform": "#7aa2f7",       # blue
    "Org-Vault": "#9ece6a",      # green
    "Org-Graph": "#73daca",      # teal
    "Network": "#2ac3de",        # electric cyan-blue
    "Coordination": "#f7768e",   # coral/pink-red
    "Node & Tooling": "#737aa2", # muted blue-grey (meta/tooling)
}
# Category glyphs (monochrome symbols — technical/cyberpunk register, not colorful emoji).
CATEGORY_GLYPH = {
    "Forge": "⚒", "Framework": "◈", "Platform": "▦", "Org-Vault": "⬢",
    "Org-Graph": "⌬", "Network": "⬡", "Coordination": "⇄", "Node & Tooling": "⚙",
}
# Category crest emblems (M25.5 asset set) — neon heraldic icons embedded as band-header emblems
# in the left gutter. Files at who/assets/crests/<slug>.png (skipped gracefully if absent).
CREST_SLUG = {
    "Forge": "forge", "Framework": "framework", "Platform": "platform", "Org-Vault": "org_vault",
    "Org-Graph": "org_graph", "Network": "network", "Coordination": "coordination",
    "Node & Tooling": "node_tooling",
}
# Edge colors — explicit Tokyo Night hex (taxonomy hardening, M25.5): cyan federation · green
# succession · purple kinship · red sequencing. Lines vs node-fills stay separable + the legend is authoritative.
EDGE_COLOR = {
    "federation": "#7dcfff", "succession": "#9ece6a", "kinship": "#bb9af7", "sequencing": "#f7768e",
}
# Opacity-by-importance (M2.2 de-spaghetti; research §2 #3/#4). Node placement caps crossings at ~85
# (the Platform→hub diagonals are irreducible), so the *perceptual* de-spaghetti is to let the 40
# dense federation edges RECEDE to a faint cyan texture at rest while the band structure + the 7
# structural edges (lineage/kinship/sequencing) lead. JSON-Canvas has no per-edge alpha, so this is a
# static muted stroke (hover-highlight is interaction → M2.5, plugin-gated). The legend keeps bright
# cyan #7dcfff as the federation *type* reference; only the drawn stroke is dimmed.
EDGE_REST_DIM = "#3a5a6b"   # muted cyan — recedes on the #16161e ground, still traceable
# Edge NON-COLOR channels (CVD-safe taxonomy). Red↔green merge under protan/deutan, so the 4
# relations must also read WITHOUT hue — via dash + arrowheads (native Advanced Canvas
# styleAttributes that DO render on a loaded canvas; CanvasForge color_accessibility.md). Molecular
# framing (DG-1=DNA): federation = expression flow · succession = lineage · kinship = complementary
# pairing · sequencing = reading-frame gate.
#
# NB (M2.1 F-M2.1-A/B): pathfindingMethod="square" is valid JSON-Canvas metadata, but Advanced
# Canvas does NOT recompute routing for externally-generated edges (only its own UI-drawn ones), so
# it does NOT de-spaghetti a generated canvas — harmless, kept for when a reroute-on-load lands
# (Obsidian.aDNA plugin campaign). The de-spaghetti that actually renders is NODE PLACEMENT (M2.2:
# barycenter within-band ordering + band order). The dash/arrow styles below DO render — load-bearing.
FEDERATION_ROUTING = "square"   # routing hint only — plugin ignores it for generated edges (see NB)
EDGE_STYLE = {
    "federation": {"pathfinding": FEDERATION_ROUTING},                 # solid; routing hint is metadata-only (NB above)
    "succession": {},                                                  # solid bezier, single arrow
    "sequencing": {"from_end": "arrow", "path_style": "long-dashed"},  # double-arrow + dashed (≠ succession on 2 channels)
    "kinship":    {"path_style": "dotted"},                            # dotted (undirected feel)
}
# Tokyo Night ground (for state-luminance blending).
TN_BG = (0x16, 0x16, 0x1e)
# State-luminance: how far a node's category hue blends toward the ground, by health/status
# (active = full neon; genesis/planning = mid; superseded/legacy = dimmed). Unknown → slight dim.
STATE_DIM = {
    "active": 0.0, "production": 0.0, "in_use": 0.0, "live": 0.0,
    "genesis": 0.30, "execution": 0.15, "genesis-execution": 0.20, "planning": 0.38, "provisional": 0.30,
    "superseded": 0.58, "archived": 0.62, "legacy": 0.50, "deprecated": 0.62,
}

# wrapper-dir -> producer vault (federation auto-probe).
# NB (pt19): several producer-vault names below are pre-rename (SiteForge→Astro, ComfyForge→ComfyUI,
# SpeechForge→Oration, MoleculeForge→Molecules, ContextCompass archived→Context) — the coordinated
# refresh is PT pt19. Wrapper-DIR keys keep the old name until P5 re-points them (videoforge precedent
# below). canvasforge→Canvas.aDNA is updated here (CanvasForge merged into Canvas at pt09).
FORGE_FRAMEWORK_WRAPPERS = {
    "iii": "III.aDNA", "siteforge": "SiteForge.aDNA", "canvasforge": "Canvas.aDNA",
    # videoforge wrapper-dir -> Videos.aDNA since 2026-06-10 (VideoForge.aDNA renamed at the org wave;
    # consumer wrapper DIRS keep the old name until Videos exec-campaign Phase-5 re-points them).
    "comfyforge": "ComfyForge.aDNA", "videoforge": "Videos.aDNA",
    "speechforge": "SpeechForge.aDNA",
    "moleculeforge": "MoleculeForge.aDNA", "contextcompass": "ContextCompass.aDNA",
    "visualdna": "VisualDNA.aDNA",
    # literatureforge dropped 2026-06-08: LiteratureForge.aDNA wound down -> Archive.aDNA (no longer a
    # live federation producer). Cleared the 2 dangling-endpoint flags from ScienceStanley/ZenZachary's
    # still-on-disk literatureforge/ wrappers (consumer-side wrapper cleanup is cross-vault — a follow-up).
}

# WHO/WHAT/HOW triad (14 base + 2 node-local: inventory, identity)
TRIAD = {
    "WHO": ["governance", "team", "coordination", "identity"],
    "WHAT": ["context", "decisions", "modules", "lattices", "inventory"],
    "HOW": ["campaigns", "missions", "sessions", "templates", "skills", "pipelines", "backlog"],
}
LEG_DIR = {"WHO": "who", "WHAT": "what", "HOW": "how"}
LEG_COLOR = {"WHO": "#7aa2f7", "WHAT": "#9ece6a", "HOW": "#e0af68"}  # Tokyo Night blue / green / yellow
NODE_LOCAL_ENTITIES = {"inventory", "identity"}  # v8-candidate node-local types (✦)

# ── Layout constants (deterministic grid; widened 2026-05-31 per operator layout review) ──
TRIAD_X, TRIAD_Y = -1320, 40
LANE_W, LANE_GAP = 248, 28
ENT_W, ENT_H, ENT_GAP = 220, 60, 14
LANE_PAD_TOP, LANE_PAD_BOT = 54, 20

VAULT_X, VAULT_Y = 80, 40
PER_ROW = 6
NODE_W, NODE_H, NODE_GAP = 204, 108, 26          # M25.5: +8 node gap (breathing room)
BAND_PAD, BAND_PAD_TOP, BAND_GAP = 20, 56, 108   # M25.5: +24 band gap (clearer strata)
BAND_W = BAND_PAD * 2 + PER_ROW * NODE_W + (PER_ROW - 1) * NODE_GAP

SIDE_X = VAULT_X + BAND_W + 96   # x of legend/meta/drift column
SIDE_W = 420


# ── Optional style-override (Operation Prytaneion M1.3 cadence-harness "improve" surface) ──
# Default-OFF: with no override file the canvas is byte-stable (determinism preserved, per the
# module docstring). The cadence harness writes a bounded set of style knobs here, re-renders,
# and reverts after the dry-run (operator decision D-B: canvas content = Phase 2). Read once at
# import — each render is a fresh `python build_topology_canvas.py` subprocess, so a freshly
# written override takes effect on the very next render. Schema (all sections optional):
#   category_color: {Forge: "#hex", ...}   # merged into CATEGORY_COLOR
#   edge_color:     {federation: "#hex", ...}
#   state_dim:      {active: 0.0, ...}
#   geometry:       {node_w, node_h, node_gap, band_gap, per_row}
CANVAS_STYLE_OVERRIDE = Path(os.environ.get(
    "CANVAS_STYLE_OVERRIDE", str(NODE_VAULT / "what" / "canvas" / "canvas_style.yaml")))


def _apply_style_override() -> str | None:
    """Merge an optional style-override file into the style constants. Returns the override
    path string if applied (for provenance), else None. No file → no-op → byte-stable canvas."""
    global NODE_W, NODE_H, NODE_GAP, BAND_GAP, PER_ROW, BAND_W, SIDE_X, TRIAD_X
    if not CANVAS_STYLE_OVERRIDE.exists():
        return None
    ov = yaml.safe_load(CANVAS_STYLE_OVERRIDE.read_text(encoding="utf-8")) or {}
    CATEGORY_COLOR.update(ov.get("category_color") or {})
    EDGE_COLOR.update(ov.get("edge_color") or {})
    STATE_DIM.update(ov.get("state_dim") or {})
    geo = ov.get("geometry") or {}
    NODE_W = int(geo.get("node_w", NODE_W))
    NODE_H = int(geo.get("node_h", NODE_H))
    NODE_GAP = int(geo.get("node_gap", NODE_GAP))
    BAND_GAP = int(geo.get("band_gap", BAND_GAP))
    PER_ROW = int(geo.get("per_row", PER_ROW))
    TRIAD_X = int(geo.get("triad_x", TRIAD_X))   # layout-compaction knob (triad↔bands gap)
    BAND_W = BAND_PAD * 2 + PER_ROW * NODE_W + (PER_ROW - 1) * NODE_GAP
    SIDE_X = VAULT_X + BAND_W + 96
    # band_order knob (M2.1 de-spaghetti): reorder the category bands so producer bands sit
    # adjacent to their consumer mass (fewer cross-band federation crossings). Must be a permutation
    # of CATEGORY_ORDER; default (no override) keeps the Forge-first narrative order. In-place mutate.
    order = ov.get("band_order")
    if order and set(order) == set(CATEGORY_ORDER):
        CATEGORY_ORDER[:] = order
    return str(CANVAS_STYLE_OVERRIDE)


_STYLE_OVERRIDE_APPLIED = _apply_style_override()


# ── Helpers ───────────────────────────────────────────────────────────────────
def nid(prefix: str, key: str) -> str:
    return prefix + "_" + re.sub(r"[^A-Za-z0-9]+", "_", key).strip("_")


def sides(a: tuple, b: tuple) -> tuple[str, str]:
    """Pick edge attach sides from node geometry (x, y, w, h) → cleaner routing."""
    acx, acy = a[0] + a[2] / 2, a[1] + a[3] / 2
    bcx, bcy = b[0] + b[2] / 2, b[1] + b[3] / 2
    dx, dy = bcx - acx, bcy - acy
    if abs(dx) >= abs(dy):
        return ("right", "left") if dx >= 0 else ("left", "right")
    return ("bottom", "top") if dy >= 0 else ("top", "bottom")


def fed_sides(a: tuple, b: tuple) -> tuple[str, str]:
    """Federation attach: ALWAYS horizontal (left↔right, never top/bottom). With orthogonal
    routing this pulls the 38-edge hub fan off the vertical 'swing' that reads as spaghetti, into
    clean L/Z corridors. Structural arcs keep geometry-picked `sides()` (their swing carries meaning)."""
    acx, bcx = a[0] + a[2] / 2, b[0] + b[2] / 2
    return ("right", "left") if bcx >= acx else ("left", "right")


def _blend(hex_color: str, t: float) -> str:
    """Blend hex toward the Tokyo Night ground by t∈[0,1] (0 = full hue, 1 = ground)."""
    c = tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(round(c[i] * (1 - t) + TN_BG[i] * t) for i in range(3))


def node_color(cat: str, health: str | None) -> str:
    """Category hue dimmed toward the ground by health (state-luminance, M25.5)."""
    return _blend(CATEGORY_COLOR[cat], STATE_DIM.get((health or "").strip().lower(), 0.10))


# ── M2.3 node-card chrome ──────────────────────────────────────────────────────
# Card treatments render via inline <span> accents woven into the node MARKDOWN
# (cards stay markdown-primary so [[curation|name]] click-through + ![[sigil|44]]
# avatars keep working) + a global .canvas-node snippet (.obsidian/snippets/
# <persona>_canvas.css — hestia_canvas.css on the reference node). The status
# pill + corner glyph are inline spans; the left
# accent stripe is a global rule keyed to the node's own --canvas-color (no per-node
# hook needed — AC's styleAttributes/cssclasses are a controlled, non-arbitrary
# vocabulary, verified against the installed plugin source, M2.3 recon).
def _status_class(status: str) -> str:
    """Bucket an effective status into a pill class (mirrors STATE_DIM groupings)."""
    s = (status or "").strip().lower()
    if s in ("active", "production", "in_use", "live"):
        return "active"
    if s in ("superseded", "archived", "legacy", "deprecated"):
        return "dim"
    return "genesis"   # genesis/execution/planning/provisional/unknown → mid-state


def _status_pill(status: str) -> str:
    """Inline status chip rendered as a pill by the canvas snippet."""
    return f'<span class="cf-pill cf-{_status_class(status)}">{status}</span>'


# ── M2.3 WS2: degree-tiered node sizing (size = topological importance) ──────────
# Operator decision (2026-06-08): size by TOTAL degree (federation in+out + structural arcs), BOLD
# contrast. Standard tier = the current NODE_W×NODE_H (so the M1.3 geometry override still flows
# through); hub/leaf scale around it. 3 discrete tiers keep the small-multiples discipline (a few
# sizes, not a continuous ramp). Cutoff ≥6 keeps BOTH brand vaults (ScienceStanley/ZenZachary) as hubs.
HUB_MIN_DEGREE, STANDARD_MIN_DEGREE = 6, 2     # hub ≥6 · standard 2-5 · leaf 0-1
HUB_SCALE = (1.255, 1.222)                     # ≈256×132 at the 204×108 default
LEAF_SCALE = (0.863, 0.889)                    # ≈176×96  at the 204×108 default


def _degree_map(vaults: list[dict], rel: dict, fed_pairs: list[tuple[str, str]]) -> dict[str, int]:
    """Total degree per vault name: federation incidence (in+out — the SAME fed_pairs the barycenter
    consumed) + structural arcs (succession/kinship/sequencing). Pure + deterministic."""
    deg = {v["name"]: 0 for v in vaults}
    for a, b in fed_pairs:
        if a in deg:
            deg[a] += 1
        if b in deg:
            deg[b] += 1
    for key in ("succession", "kinship", "sequencing"):
        for e in (rel.get(key) or []):
            if e.get("from") in deg:
                deg[e["from"]] += 1
            if e.get("to") in deg:
                deg[e["to"]] += 1
    return deg


def _tier_for(degree: int) -> str:
    if degree >= HUB_MIN_DEGREE:
        return "hub"
    if degree >= STANDARD_MIN_DEGREE:
        return "standard"
    return "leaf"


def _tier_size(tier: str) -> tuple[int, int]:
    """(w, h) for a tier. Standard = current NODE_W×NODE_H; hub/leaf scale around it."""
    if tier == "hub":
        return (round(NODE_W * HUB_SCALE[0]), round(NODE_H * HUB_SCALE[1]))
    if tier == "leaf":
        return (round(NODE_W * LEAF_SCALE[0]), round(NODE_H * LEAF_SCALE[1]))
    return (NODE_W, NODE_H)


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_vaults() -> list[dict]:
    data = load_yaml(INVENTORY)
    return [v for v in data.get("vaults", []) if v.get("name") not in EXCLUDE]


def federation_pairs(vaults: list[dict], rel: dict) -> list[tuple[str, str]]:
    """Consumer→producer federation edges from the on-disk wrapper probe (+ manual extras, minus
    excludes). SINGLE SOURCE OF TRUTH shared by the barycenter ordering AND edge emission, so the
    layout and the drawn edges can never diverge. Order-stable (vault order × wrapper-dict order).
    Triad-aware (M25.5 / ADR-004): a wrapper may sit at the vault root or in the WHAT leg."""
    excl = set(rel.get("federation_exclude") or [])
    pairs: list[tuple[str, str]] = []
    for v in vaults:
        vdir = WORKSPACE / v["name"]
        for wrapper, producer in FORGE_FRAMEWORK_WRAPPERS.items():
            present = any((vdir / loc / wrapper).is_dir() for loc in ("", "what"))
            if present and f"{v['name']}->{producer}" not in excl:
                pairs.append((v["name"], producer))
    for spec in (rel.get("federation_extra") or []):
        if "->" in spec:
            a, b = spec.split("->", 1)
            pairs.append((a.strip(), b.strip()))
    return pairs


def _alpha_x_centers(by_cat: dict[str, list[dict]]) -> dict[str, float]:
    """Provisional x-center of every vault node under alphabetical within-band order — the FIXED
    reference frame the barycenter sweep targets (M2.2). A node's x depends only on its within-band
    column (the VAULT_X grid is shared by all bands), so this is independent of band y-order and of
    the sweep's own result → a single, non-oscillating pass. Pure + deterministic."""
    centers: dict[str, float] = {}
    for members in by_cat.values():
        for k, v in enumerate(sorted(members, key=lambda e: e["name"].lower())):
            col = k % PER_ROW
            centers[v["name"]] = VAULT_X + BAND_PAD + col * (NODE_W + NODE_GAP) + NODE_W / 2
    return centers


# ── Build ─────────────────────────────────────────────────────────────────────
def build(vaults: list[dict], rel: dict):
    cb = CanvasBuilder(name="home_topology", version="1.0.0")
    geom: dict[str, tuple] = {}          # node id -> (x, y, w, h)
    name_to_id: dict[str, str] = {}      # vault name -> node id
    group_children: dict[str, list] = {}  # group id -> [member node dicts] (containment check)
    flags: list[str] = []
    code_repo = rel.get("code_repo", {}) or {}

    def add_group(gid, label, x, y, w, h, color):
        cb.add_group(gid, label=label, x=x, y=y, width=w, height=h, color=color)
        geom[gid] = (x, y, w, h)
        group_children.setdefault(gid, [])
        return gid

    def add_text(tid, text, x, y, w, h, parent=None, color=None):
        node = cb.add_text_node(tid, text, x=x, y=y, width=w, height=h, color=color)
        geom[tid] = (x, y, w, h)
        if parent is not None:
            group_children.setdefault(parent, []).append(node)
        return tid

    # Title banner (free text node, above both zones)
    add_text(
        "title",
        ("# 🏛 Home.aDNA — Node Topology\n"
         f"The vault-of-vaults: **{len(vaults)}** installed `.aDNA` vaults grouped by pattern "
         "category, plus the WHO/WHAT/HOW triad. Spatial twin of the §Gallery — click any "
         "vault title to open its curation card."),
        TRIAD_X, TRIAD_Y - 168, (VAULT_X + BAND_W) - TRIAD_X, 120, color="#663399",
    )

    # ── Left zone: WHO/WHAT/HOW triad lanes ──
    for i, leg in enumerate(("WHO", "WHAT", "HOW")):
        lane_x = TRIAD_X + i * (LANE_W + LANE_GAP)
        ents = TRIAD[leg]
        lane_h = LANE_PAD_TOP + len(ents) * (ENT_H + ENT_GAP) - ENT_GAP + LANE_PAD_BOT
        lane_id = add_group(nid("lane", leg), leg, lane_x, TRIAD_Y, LANE_W, lane_h, LEG_COLOR[leg])
        for j, ent in enumerate(ents):
            ex = lane_x + (LANE_W - ENT_W) // 2
            ey = TRIAD_Y + LANE_PAD_TOP + j * (ENT_H + ENT_GAP)
            agents = NODE_VAULT / LEG_DIR[leg] / ent / "AGENTS.md"
            mark = "✦ " if ent in NODE_LOCAL_ENTITIES else ""
            if agents.exists():
                text = f"{mark}[[{LEG_DIR[leg]}/{ent}/AGENTS|{ent}]]"
            else:
                text = f"{mark}**{ent}**\n_(not instantiated)_"
                flags.append(f"triad {LEG_DIR[leg]}/{ent}: no AGENTS.md (rendered as inert)")
            add_text(nid("e", leg + "_" + ent), text, ex, ey, ENT_W, ENT_H, parent=lane_id)

    # ── Right zone: vault-of-vaults category bands ──
    by_cat: dict[str, list[dict]] = {c: [] for c in CATEGORY_ORDER}
    for v in vaults:
        cat = CLASS_TO_CATEGORY.get(v.get("class", ""))
        if cat is None:
            flags.append(f"{v['name']}: unknown class '{v.get('class')}' → Node & Tooling")
            cat = "Node & Tooling"
        by_cat[cat].append(v)

    # ── Within-band ordering: Sugiyama barycenter (M2.2 de-spaghetti) ──
    # Replace the topology-blind alphabetical order with a single down-sweep: order each band's
    # nodes by the mean x-center of the producer hub(s) they federate to, so same-hub consumers
    # align into near-vertical bundles instead of a diagonal fan. This is NODE PLACEMENT — the only
    # de-spaghetti lever that actually renders (Advanced Canvas won't reroute generated edges;
    # M2.1 F-M2.1-B). Determinism: a FIXED alpha reference frame (centers), key = (barycenter,
    # name.lower()) — the name tiebreak is load-bearing (live data has barycenter ties), inf
    # sentinel for unconnected nodes → band's right edge in name order, and EXACTLY ONE sweep
    # (iterating to convergence oscillates and regresses past baseline — measured).
    fed_pairs = federation_pairs(vaults, rel)
    tgt_map: dict[str, list[str]] = {}
    for frm, producer in fed_pairs:
        tgt_map.setdefault(frm, []).append(producer)
    centers = _alpha_x_centers(by_cat)

    def _bary_key(v: dict) -> tuple[float, str]:
        xs = [centers[p] for p in tgt_map.get(v["name"], []) if p in centers]
        return (sum(xs) / len(xs) if xs else float("inf"), v["name"].lower())

    for c in by_cat:
        by_cat[c].sort(key=_bary_key)

    # ── M2.3 WS2: degree-tiered shelf packer (size = topological importance) ──
    # Per-vault total degree → a 3-tier card size (hub/standard/leaf). Within each band the cards are
    # next-fit shelf-packed IN THE EXISTING BARYCENTER ORDER (the WS1 ordering is untouched — _bary_key
    # + the fixed _alpha_x_centers frame — so crossings move only from sizing, never from reordering),
    # wrapped at a FIXED CONTENT_W so every band keeps the same left/right envelope (BAND_W / SIDE_X
    # unchanged) and the strata stay aligned. band_h is recomputed from the packed extent; cards are
    # vertically centered within their shelf. An all-standard band reproduces the prior 6-per-row grid
    # exactly. Determinism: a pure function of (members order, tier sizes).
    degree = _degree_map(vaults, rel, fed_pairs)
    CONTENT_W = PER_ROW * NODE_W + (PER_ROW - 1) * NODE_GAP   # = BAND_W - 2*BAND_PAD; the shelf-wrap width

    running_y = VAULT_Y
    for cat in CATEGORY_ORDER:
        members = by_cat[cat]
        # pass 1 — next-fit pack into shelves (barycenter order preserved)
        shelves: list[list[tuple]] = []
        shelf, used = [], 0
        for v in members:
            w, h = _tier_size(_tier_for(degree.get(v["name"], 0)))
            add = w if not shelf else NODE_GAP + w
            if shelf and used + add > CONTENT_W:
                shelves.append(shelf)
                shelf, used, add = [], 0, w
            shelf.append((v, w, h))
            used += add
        if shelf:
            shelves.append(shelf)
        # band height from the packed extent (Σ shelf heights + inter-shelf gaps + pads)
        y_rel = BAND_PAD_TOP
        for sh in shelves:
            y_rel += max(h for _, _, h in sh) + NODE_GAP
        band_h = (y_rel - NODE_GAP) + BAND_PAD
        band_id = add_group(nid("g", cat), f"{CATEGORY_GLYPH[cat]}  {cat}  ·  {len(members)}",
                            VAULT_X, running_y, BAND_W, band_h, CATEGORY_COLOR[cat])
        # Band-header crest emblem (M25.5) — free node in the left gutter, adjacent to the band.
        if (CREST_DIR / f"{CREST_SLUG[cat]}.png").exists():
            add_text(nid("crest", cat), f"![[who/assets/crests/{CREST_SLUG[cat]}.png]]",
                     VAULT_X - 96, running_y, 84, 84, color=CATEGORY_COLOR[cat])
        # pass 2 — place each shelf; cards vertically centered within the shelf's max height
        shelf_y = BAND_PAD_TOP
        for sh in shelves:
            shelf_h = max(h for _, _, h in sh)
            vx = VAULT_X + BAND_PAD
            for v, w, h in sh:
                name = v["name"]
                vy = running_y + shelf_y + (shelf_h - h) // 2
                disp = v.get("display_name") or name.replace(".aDNA", "")
                persona = v.get("persona") or "—"
                # Effective status drives both the label and the state-luminance: a vault with
                # superseded_by set reads as superseded even if its raw health is still "active"
                # (matches the curation layer's current_status derivation).
                status = "superseded" if v.get("superseded_by") else (v.get("health") or "—")
                cura = CURATION_DIR / f"curation_{name}.md"
                if cura.exists():
                    title = f"[[who/curation/curation_{name}|{disp}]]"
                else:
                    title = f"**{disp}**"
                    flags.append(f"{name}: no curation card → node has no hotspot")
                # M2.4: per-node emblem avatar (topic emblem > persona sigil). Persona-less
                # vaults without a topic emblem fall through to the band crest — no forced icon.
                icon = None
                if (EMBLEM_DIR / f"{name}.png").exists():
                    icon = f"who/assets/emblems/{name}.png"
                elif persona and persona != "—":
                    for cand in (persona, persona.split()[0]):
                        if (SIGIL_DIR / f"{cand}.png").exists():
                            icon = f"who/assets/sigils/{cand}.png"
                            break
                if icon:
                    title = f"![[{icon}|44]] {title}"
                ann = code_repo.get(name)
                # M2.3 card: corner category glyph (2nd channel beyond hue) · title (icon +
                # curation link) · status pill · persona italic · sibling repo mono-boxed.
                glyph = f'<span class="cf-glyph">{CATEGORY_GLYPH[cat]}</span>'
                text = (f"{glyph}{title} {_status_pill(status)}\n"
                        f"_{persona}_" + (f"\n`⛓ {ann}`" if ann else ""))
                vid = nid("v", name)
                name_to_id[name] = vid
                add_text(vid, text, vx, vy, w, h, parent=band_id,
                         color=node_color(cat, status))
                vx += w + NODE_GAP
            shelf_y += shelf_h + NODE_GAP
        running_y += band_h + BAND_GAP

    # ── Left rail (orientation): enclosed Legend / Key panel, anchored beneath the WHO/WHAT/HOW
    #    triad so the left column reads as ONE persistent "how to read this canvas" rail (M2.2 Obj 2
    #    — Gestalt common-region). The legend becomes a bounded GROUP (not a free node); its text
    #    card carries the box/brightness key + the CVD-safe edge taxonomy + glyph key. Anchored below
    #    the tallest triad lane, full triad width, so the triad lanes + legend align into one rail.
    #    NB: we do NOT wrap the 3 lanes in an outer group — that overlaps them and fails spatial_check;
    #    the rail reads via adjacency + shared x-column, not a mega-box. Deterministic (pure constants).
    triad_bottom = TRIAD_Y + max(
        LANE_PAD_TOP + len(TRIAD[leg]) * (ENT_H + ENT_GAP) - ENT_GAP + LANE_PAD_BOT
        for leg in ("WHO", "WHAT", "HOW"))
    LEG_X = TRIAD_X
    LEG_W = 3 * LANE_W + 2 * LANE_GAP            # span the full triad block (rail coherence)
    LEG_Y = triad_bottom + 48                    # snug below the triad, clear of the tallest lane
    LEG_H = 332
    legend_gid = add_group("legend_panel", "Legend · how to read this canvas",
                           LEG_X, LEG_Y, LEG_W, LEG_H, "#7dcfff")
    add_text("legend", (
        "**Box** = gene family (pattern category · count).\n"
        "**Node brightness** = expression — active bright → superseded faint.\n\n"
        "**Edges** — color *and* line-style (colorblind-safe):\n"
        "federation · cyan · dimmed at rest\n"
        "succession · green · solid arrow\n"
        "kinship · purple · dotted\n"
        "sequencing · red · dashed double-arrow\n\n"
        "⛓ sibling code repo · ✦ node-local type (v8 candidate)\n"
        "_Click a vault title → its curation card._"),
        LEG_X + BAND_PAD, LEG_Y + BAND_PAD_TOP,
        LEG_W - 2 * BAND_PAD, LEG_H - BAND_PAD_TOP - BAND_PAD, parent=legend_gid)

    # ── Right column: snapshot + drift status panels (free text; legend moved to the left rail,
    #    so these shift up to fill the column top) ──
    add_text("meta", (
        "## Topology snapshot\n"
        "node **Mac** · operator **stanley**\n"
        f"**{len(vaults)}** vaults · **{len(CATEGORY_ORDER)}** categories\n"
        f"generated {GENERATED_DATE}\n\n"
        "source → [[what/inventory/inventory_vaults|inventory_vaults]]\n"
        "regen → `what/code/build_topology_canvas.py`\n"
        "state → [[STATE|STATE.md]]"),
        SIDE_X, VAULT_Y, SIDE_W, 220, color="#bb9af7")
    add_text("drift", (
        "## ⚠ Drift — surfaced, not resolved\n"
        "**Pygmalion** persona collision\n"
        "`VisualDNA.aDNA` + `ZenZachary.aDNA`\n"
        "→ operator to disambiguate\n\n"
        "_Hestia counts; the operator disposes._"),
        SIDE_X, VAULT_Y + 252, SIDE_W, 200, color="#f7768e")

    # ── Edges (color + non-color taxonomy channels; structural arcs carry their label) ──
    seen: set[tuple] = set()

    def add_edge(frm: str, to: str, etype: str, *, label: str | None = None):
        if frm not in name_to_id or to not in name_to_id:
            flags.append(f"edge {etype}: unresolved endpoint {frm} -> {to}")
            return
        fid, tid = name_to_id[frm], name_to_id[to]
        if fid == tid:
            return
        key = (fid, tid, etype)
        if key in seen:
            return
        seen.add(key)
        # Federation attaches horizontally; structural arcs keep geometry sides. Federation also draws
        # dimmed (opacity-by-importance) so the dense fan recedes; structural edges stay full-bright.
        fs, ts = (fed_sides if etype == "federation" else sides)(geom[fid], geom[tid])
        draw_color = EDGE_REST_DIM if etype == "federation" else EDGE_COLOR[etype]
        cb.add_edge(nid("ed", f"{frm}__{to}__{etype}"), fid, tid,
                    from_side=fs, to_side=ts, to_end="arrow", color=draw_color,
                    label=label, **EDGE_STYLE[etype])

    # federation — drawn from the SAME federation_pairs() the barycenter ordering consumed (probe
    # ran once, above), so the layout and the edges can never disagree. add_edge dedups + skips self.
    for frm, producer in fed_pairs:
        add_edge(frm, producer, "federation")

    # structural edges from relationships.yaml (labeled — each carries its succession/kinship/sequencing tie)
    for s in (rel.get("succession") or []):
        add_edge(s["from"], s["to"], "succession", label=s.get("label"))
    for k in (rel.get("kinship") or []):
        add_edge(k["from"], k["to"], "kinship", label=k.get("label"))
    for q in (rel.get("sequencing") or []):
        add_edge(q["from"], q["to"], "sequencing", label=q.get("label"))

    # ── metadata (my schema; topology hash via CanvasBuilder, source hash via inputs) ──
    inv_bytes = INVENTORY.read_bytes()
    rel_bytes = RELATIONSHIPS.read_bytes()
    source_hash = hashlib.sha256(inv_bytes + rel_bytes).hexdigest()[:16]
    meta = {
        "version": "1.0-1.0",
        "frontmatter": {},
        "_reserved": {
            "authority": "generator",
            "source_yaml": "what/inventory/inventory_vaults.yaml + what/canvas/topology_relationships.yaml",
            "generated_by": "what/code/build_topology_canvas.py",
            "generated_date": GENERATED_DATE,
            "substrate": "Canvas.aDNA/what/production/canvas_core (CanvasBuilder; ADR-004, lands PT P5)",
            "source_hash": f"sha256:{source_hash}",
            "topology_hash": f"sha256:{cb.compute_sync_hash()}",
            "vault_count": len(vaults),
        },
    }
    # Provenance only when a style-override is active (M1.3 dry-run). Omitted in baseline so a
    # default regen stays byte-identical to the pre-M1.3 canvas (determinism discipline).
    if _STYLE_OVERRIDE_APPLIED:
        meta["_reserved"]["style_override"] = _STYLE_OVERRIDE_APPLIED
    info = {"by_cat": by_cat, "flags": flags, "groups": group_children, "geom": geom}
    return cb, meta, info


def spatial_check(cb, groups: dict) -> list[str]:
    """Objective layout gate (canvas_core spatial substrate): bands/lanes/callouts don't
    collide, and every member node sits inside its band/lane. Returns violation strings."""
    problems: list[str] = []
    nodes_by_id = {n["id"]: n for n in cb.nodes}
    group_nodes = [n for n in cb.nodes if n.get("type") == "group"]
    free_text = [n for n in cb.nodes
                 if n.get("type") == "text" and n["id"] not in {
                     c["id"] for kids in groups.values() for c in kids}]

    # 1. groups + free-floating callouts must not overlap each other
    for a, b in spatial.detect_overlaps(group_nodes + free_text):
        problems.append(f"overlap: {a} <-> {b}")

    # 2. every member node contained in its group; 3. siblings within a group don't overlap
    for gid, kids in groups.items():
        parent = nodes_by_id.get(gid)
        if parent is None or not kids:
            continue
        for cid in spatial.containment_check(parent, kids):
            problems.append(f"not-contained: {cid} outside {gid}")
        for a, b in spatial.detect_overlaps(kids):
            problems.append(f"sibling-overlap in {gid}: {a} <-> {b}")
    return problems


# ── Routing metric (objective de-spaghetti gauge; M2.1) ───────────────────────
def _attach_point(g: tuple, side: str) -> tuple[float, float]:
    """Edge attach point on a node box (x, y, w, h) for a given side."""
    x, y, w, h = g
    return {
        "left": (x, y + h / 2), "right": (x + w, y + h / 2),
        "top": (x + w / 2, y), "bottom": (x + w / 2, y + h),
    }[side]


def _seg_cross(p1, p2, p3, p4) -> bool:
    """True iff segment p1p2 properly crosses p3p4 (epsilon-stable orientation; no collinear)."""
    def orient(a, b, c) -> int:
        v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        return (v > 1e-9) - (v < -1e-9)
    o1, o2 = orient(p1, p2, p3), orient(p1, p2, p4)
    o3, o4 = orient(p3, p4, p1), orient(p3, p4, p2)
    return o1 != o2 and o3 != o4 and 0 not in (o1, o2, o3, o4)


def routing_metrics(cb, geom: dict) -> tuple[int, int]:
    """Objective spaghetti gauge — deterministic + byte-stable (integer, no wall-clock):
      vertical = edges attaching on a top/bottom face (the vertical 'swing' that reads as
                 curved spaghetti when endpoints are far apart);
      crossings = pairwise straight-segment intersections (each edge ≈ a segment between its
                 two attach-point centers — a render-independent proxy for the bezier/route).
    Shared-endpoint pairs (a hub's fan-in) are not counted as crossings."""
    segs: list[tuple] = []
    vertical = 0
    for e in cb.edges:
        fg, tg = geom.get(e["fromNode"]), geom.get(e["toNode"])
        if not fg or not tg:
            continue
        fs, ts = e.get("fromSide"), e.get("toSide")
        if fs in ("top", "bottom") or ts in ("top", "bottom"):
            vertical += 1
        segs.append((_attach_point(fg, fs), _attach_point(tg, ts), e["fromNode"], e["toNode"]))
    crossings = 0
    for i in range(len(segs)):
        a1, a2, an1, an2 = segs[i]
        for j in range(i + 1, len(segs)):
            b1, b2, bn1, bn2 = segs[j]
            if {an1, an2} & {bn1, bn2}:        # shared hub node ≠ crossing
                continue
            if _seg_cross(a1, a2, b1, b2):
                crossings += 1
    return vertical, crossings


# ── Driver ────────────────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate only (schema + overlaps), no write")
    args = ap.parse_args()

    vaults = load_vaults()
    rel = load_yaml(RELATIONSHIPS)
    cb, meta, info = build(vaults, rel)

    by_cat, flags = info["by_cat"], info["flags"]
    print("  Categories:")
    for c in CATEGORY_ORDER:
        print(f"    {c:<16} {len(by_cat[c])}")
    et: dict[str, int] = {}
    for e in cb.edges:
        t = e["id"].rsplit("__", 1)[-1]
        et[t] = et.get(t, 0) + 1
    print(f"  Nodes={len(cb.nodes)}  Edges={len(cb.edges)}  "
          + " ".join(f"{k}={v}" for k, v in sorted(et.items())))
    print(f"  Vaults={len(vaults)} (sum check {sum(len(by_cat[c]) for c in CATEGORY_ORDER)})")
    vert, cross = routing_metrics(cb, info["geom"])
    print(f"  Routing: vertical-attach={vert}  crossings={cross}  (lower = less spaghetti)")

    # canvas_core schema validation + spatial layout gate
    schema_errors = cb.validate()
    layout_problems = spatial_check(cb, info["groups"])
    if schema_errors:
        print(f"  Schema errors ({len(schema_errors)}):")
        for e in schema_errors:
            print(f"    ✗ {e}")
    if layout_problems:
        print(f"  Layout violations ({len(layout_problems)}):")
        for p in layout_problems:
            print(f"    ✗ {p}")
    if not schema_errors and not layout_problems:
        print("  Validate: schema OK · no overlaps · all nodes contained ✅")
    if flags:
        print(f"  Flags ({len(flags)}):")
        for f in flags:
            print(f"    ! {f}")

    if schema_errors or layout_problems:
        print("  ABORT: fix schema/layout before writing.")
        return 1

    canvas = {"nodes": cb.nodes, "edges": cb.edges, "metadata": meta}
    if not args.check:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(canvas, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  wrote {OUT.relative_to(NODE_VAULT)}")
    else:
        print("  --check: valid (no write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
