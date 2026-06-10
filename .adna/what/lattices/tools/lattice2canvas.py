"""
Lattice YAML to Obsidian Canvas Converter.

Converts .lattice.yaml files to Obsidian .canvas JSON format
for visual editing. Implements the mapping defined in
canvas_yaml_interop.md.

Usage:
    >>> from objects.lattices.tools.lattice2canvas import lattice_to_canvas
    >>> canvas = lattice_to_canvas(yaml_data)
    >>> # canvas is a dict with "nodes" and "edges" keys

    >>> from objects.lattices.tools.lattice2canvas import lattice_file_to_canvas
    >>> lattice_file_to_canvas("pipeline.lattice.yaml", "pipeline.canvas")
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

# Color conventions per canvas_yaml_interop.md
NODE_TYPE_COLORS: dict[str, str] = {
    "module": "4",  # Cyan
    "dataset": "5",  # Green
    "reasoning": "6",  # Purple
    # "process" uses default (no color)
}

# Layout constants
HORIZONTAL_SPACING = 400
DEFAULT_FILE_WIDTH = 350
DEFAULT_FILE_HEIGHT = 300
DEFAULT_TEXT_WIDTH = 350
DEFAULT_TEXT_HEIGHT = 200
META_GROUP_X = -200
META_GROUP_Y = -100
META_GROUP_WIDTH = 300
META_GROUP_HEIGHT = 150


def lattice_to_canvas(data: dict[str, Any]) -> dict[str, Any]:
    """
    Convert a parsed .lattice.yaml dict to Obsidian .canvas JSON dict.

    Implements YAML→Canvas mapping from canvas_yaml_interop.md:
    - module/dataset nodes → file nodes (linking to vault .md records)
    - process/reasoning nodes → text nodes
    - Lattice metadata → group node at top-left
    - Auto-layout: left-to-right, HORIZONTAL_SPACING px apart
    - Color conventions: module=cyan(4), dataset=green(5), reasoning=purple(6)

    Args:
        data: Parsed .lattice.yaml dictionary with root "lattice" key.

    Returns:
        Canvas JSON dictionary with "nodes" and "edges" keys.

    Raises:
        ValueError: If data is missing required "lattice" key.
    """
    if "lattice" not in data:
        raise ValueError("Input must have a 'lattice' root key")

    lattice = data["lattice"]
    canvas_nodes: list[dict[str, Any]] = []
    canvas_edges: list[dict[str, Any]] = []

    # Metadata group node
    name = lattice.get("name", "untitled")
    version = lattice.get("version", "0.0.0")
    canvas_nodes.append(
        {
            "id": "_lattice_meta",
            "type": "group",
            "label": f"{name} v{version}",
            "x": META_GROUP_X,
            "y": META_GROUP_Y,
            "width": META_GROUP_WIDTH,
            "height": META_GROUP_HEIGHT,
        }
    )

    # Build node order for layout
    yaml_nodes = lattice.get("nodes", [])
    for i, node in enumerate(yaml_nodes):
        canvas_node = _convert_node(node, x_position=i * HORIZONTAL_SPACING)
        canvas_nodes.append(canvas_node)

    # Convert edges
    for edge in lattice.get("edges", []):
        canvas_edge = _convert_edge(edge)
        canvas_edges.append(canvas_edge)

    return {"nodes": canvas_nodes, "edges": canvas_edges}


def _convert_node(node: dict[str, Any], x_position: int) -> dict[str, Any]:
    """Convert a YAML node to a canvas node."""
    node_id = node["id"]
    node_type = node.get("type", "process")
    ref = node.get("ref")
    description = node.get("description", "")
    prompt = node.get("prompt", "")

    canvas_node: dict[str, Any] = {
        "id": node_id,
        "x": x_position,
        "y": 0,
    }

    # Type mapping per interop spec
    if node_type in ("module", "dataset") and ref:
        # File nodes — link to vault record
        file_path = ref if ref.endswith(".md") else f"{ref}.md"
        canvas_node["type"] = "file"
        canvas_node["file"] = file_path
        canvas_node["width"] = DEFAULT_FILE_WIDTH
        canvas_node["height"] = DEFAULT_FILE_HEIGHT
    elif node_type == "reasoning":
        # Reasoning text node with prompt
        text = f"## {node_id}\n\n{prompt}" if prompt else f"## {node_id}\n\n{description}"
        canvas_node["type"] = "text"
        canvas_node["text"] = text
        canvas_node["width"] = DEFAULT_TEXT_WIDTH
        canvas_node["height"] = DEFAULT_TEXT_HEIGHT
    else:
        # Process text node (and fallback for module/dataset without ref)
        text = f"## {node_id}\n\n{description}"
        canvas_node["type"] = "text"
        canvas_node["text"] = text
        canvas_node["width"] = DEFAULT_TEXT_WIDTH
        canvas_node["height"] = DEFAULT_TEXT_HEIGHT

    # Color conventions
    color = NODE_TYPE_COLORS.get(node_type)
    if color:
        canvas_node["color"] = color

    return canvas_node


def _convert_edge(edge: dict[str, Any]) -> dict[str, Any]:
    """Convert a YAML edge to a canvas edge."""
    source = edge["from"]
    target = edge["to"]
    label = edge.get("label", "")

    # Append condition to label if present
    condition = edge.get("condition")
    if condition and label:
        label = f"{label} (if: {condition})"
    elif condition:
        label = f"(if: {condition})"

    canvas_edge: dict[str, Any] = {
        "id": f"{source}_to_{target}",
        "fromNode": source,
        "fromSide": "right",
        "toNode": target,
        "toSide": "left",
    }

    if label:
        canvas_edge["label"] = label

    return canvas_edge


def lattice_file_to_canvas(
    yaml_path: str | Path,
    canvas_path: str | Path,
) -> dict[str, Any]:
    """
    Convert a .lattice.yaml file to an Obsidian .canvas file.

    Args:
        yaml_path: Path to input .lattice.yaml file.
        canvas_path: Path to output .canvas file.

    Returns:
        The canvas dictionary that was written.

    Raises:
        FileNotFoundError: If yaml_path does not exist.
        ValueError: If YAML is invalid.
    """
    yaml_path = Path(yaml_path)
    canvas_path = Path(canvas_path)

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    if data is None:
        raise ValueError(f"Empty YAML file: {yaml_path}")

    canvas = lattice_to_canvas(data)

    with open(canvas_path, "w") as f:
        json.dump(canvas, f, indent=2)

    return canvas
