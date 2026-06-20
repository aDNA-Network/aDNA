#!/usr/bin/env python
"""render_canvas_offline.py — minimal offline geometry preview of a .canvas file (no Obsidian).

The "offline preview" dev tool what/canvas/AGENTS.md describes (M24 had it in-session only;
persisted at M6.1). Renders node/group rects + edge lines with the canvas's own colors onto a
dark ground — a geometry/structure check, NOT the aesthetic gate (that stays live-Obsidian +
operator eye).

    python what/code/render_canvas_offline.py [path/to/topology.canvas] [out.png]

Defaults: what/canvas/topology.canvas → /tmp/canvas_offline.png. Needs matplotlib (the
`python` anaconda interpreter has it; falls back with a clear message otherwise).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Obsidian canvas preset palette (1-6) on the Tokyo-Night ground
PRESET = {"1": "#e06c75", "2": "#e5c07b", "3": "#e0af68", "4": "#9ece6a",
          "5": "#7dcfff", "6": "#bb9af7"}
GROUND = "#16161e"


def color_of(c: str | None, fallback: str = "#565f89") -> str:
    if not c:
        return fallback
    return PRESET.get(c, c if c.startswith("#") else fallback)


def main() -> int:
    canvas_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("what/canvas/topology.canvas")
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("/tmp/canvas_offline.png")
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle
    except ImportError:
        print("FAIL: matplotlib unavailable under this interpreter (try `python`, not `python3`)",
              file=sys.stderr)
        return 1

    data = json.loads(canvas_path.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in data.get("nodes", [])}

    fig, ax = plt.subplots(figsize=(20, 12), dpi=110)
    ax.set_facecolor(GROUND)
    fig.patch.set_facecolor(GROUND)

    # edges first (under the nodes)
    for e in data.get("edges", []):
        a, b = nodes.get(e.get("fromNode")), nodes.get(e.get("toNode"))
        if not a or not b:
            continue
        ax.plot([a["x"] + a["width"] / 2, b["x"] + b["width"] / 2],
                [a["y"] + a["height"] / 2, b["y"] + b["height"] / 2],
                color=color_of(e.get("color"), "#3a5a6b"), linewidth=1.1, alpha=0.85, zorder=1)

    for n in nodes.values():
        is_group = n.get("type") == "group"
        col = color_of(n.get("color"))
        ax.add_patch(Rectangle((n["x"], n["y"]), n["width"], n["height"],
                               fill=not is_group,
                               facecolor=(col + "26") if not is_group else "none",
                               edgecolor=col, linewidth=1.4 if is_group else 0.9, zorder=2))
        label = n.get("label") or ""
        if not label and n.get("type") == "text":
            label = (n.get("text") or "").splitlines()[0][:38] if n.get("text") else ""
            label = label.replace("<span class=\"cf-glyph\">", "").replace("</span>", "")
        if label:
            ax.text(n["x"] + 6, n["y"] + (2 if is_group else n["height"] / 2), label[:44],
                    color="#c0caf5", fontsize=5.2 if not is_group else 6.5,
                    va="top" if is_group else "center", zorder=3)

    ax.autoscale()
    ax.invert_yaxis()          # canvas y grows downward
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(out_path, facecolor=GROUND, bbox_inches="tight")
    print(f"wrote {out_path}  (nodes={len(nodes)} edges={len(data.get('edges', []))})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
