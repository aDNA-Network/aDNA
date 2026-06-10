"""
Obsidian Canvas to Lattice YAML Converter.

Converts Obsidian .canvas JSON files to .lattice.yaml format.
Implements the Canvas→YAML mapping defined in canvas_yaml_interop.md.

Usage:
    >>> from objects.lattices.tools.canvas2lattice import canvas_to_lattice
    >>> lattice = canvas_to_lattice(canvas_data)
    >>> # lattice is a dict with root "lattice" key

    >>> from objects.lattices.tools.canvas2lattice import canvas_file_to_lattice
    >>> canvas_file_to_lattice("pipeline.canvas", "pipeline.lattice.yaml")
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

# Reasoning node convention: text starts with "## Reasoning:" prefix
REASONING_PREFIX_PATTERN = re.compile(r"^##\s*Reasoning:", re.IGNORECASE)

# Valid lattice node ID pattern: ^[a-z][a-z0-9_]*$
_VALID_ID = re.compile(r"^[a-z][a-z0-9_]*$")


def _sanitize_node_id(raw_id: str) -> str:
    """Convert a canvas node ID (often a UUID) to a valid lattice node ID.

    Valid IDs: ^[a-z][a-z0-9_]*$ (lowercase, underscores, starts with letter).
    UUIDs like '4a3b2c1d' get prefixed with 'n_' and hyphens replaced.
    """
    if _VALID_ID.match(raw_id):
        return raw_id
    sanitized = raw_id.lower().replace("-", "_").replace(" ", "_")
    sanitized = re.sub(r"[^a-z0-9_]", "", sanitized)
    if not sanitized or not sanitized[0].isalpha():
        sanitized = "n_" + sanitized
    return sanitized


def canvas_to_lattice(
    data: dict[str, Any],
    *,
    name: str = "untitled",
    version: str = "0.1.0",
    description: str = "Lattice imported from Obsidian canvas",
    lattice_type: str = "pipeline",
    mode: str = "workflow",
    runtime: str = "local",
    tier: str = "L1",
) -> dict[str, Any]:
    """
    Convert a parsed .canvas JSON dict to .lattice.yaml dict.

    Implements Canvas→YAML mapping from canvas_yaml_interop.md:
    - file nodes with what/modules/ path → module nodes
    - file nodes with what/datasets/ path → dataset nodes
    - text nodes → process nodes (or reasoning if prefixed)
    - group/link nodes → ignored
    - _lattice_meta group → extracts name/version for root fields

    Args:
        data: Parsed canvas JSON dictionary with "nodes" and "edges".
        name: Default lattice name (overridden by _lattice_meta if present).
        version: Default version (overridden by _lattice_meta if present).
        description: Default description.
        lattice_type: Default lattice type.
        mode: Default execution mode.
        runtime: Default runtime.
        tier: Default tier.

    Returns:
        Lattice YAML dictionary with root "lattice" key.
    """
    canvas_nodes = data.get("nodes", [])
    canvas_edges = data.get("edges", [])

    # Extract metadata from _lattice_meta group if present
    meta_name, meta_version = _extract_meta(canvas_nodes)
    if meta_name:
        name = meta_name
    if meta_version:
        version = meta_version

    # Convert nodes (skip groups and links)
    lattice_nodes: list[dict[str, Any]] = []
    for cnode in canvas_nodes:
        lnode = _convert_node(cnode)
        if lnode is not None:
            lattice_nodes.append(lnode)

    # Convert edges
    lattice_edges: list[dict[str, Any]] = []
    for cedge in canvas_edges:
        ledge = _convert_edge(cedge)
        lattice_edges.append(ledge)

    return {
        "lattice": {
            "name": name,
            "version": version,
            "lattice_type": lattice_type,
            "description": description,
            "execution": {
                "mode": mode,
                "runtime": runtime,
                "tier": tier,
            },
            "nodes": lattice_nodes,
            "edges": lattice_edges,
            "fair": {
                "license": "MIT",
                "keywords": ["imported-from-canvas"],
            },
        }
    }


def _extract_meta(
    canvas_nodes: list[dict[str, Any]],
) -> tuple[str | None, str | None]:
    """Extract name and version from _lattice_meta group node."""
    for node in canvas_nodes:
        if node.get("id") == "_lattice_meta" and node.get("type") == "group":
            label = node.get("label", "")
            # Parse "name vX.Y.Z" format
            parts = label.rsplit(" v", 1)
            if len(parts) == 2:
                return parts[0].strip(), parts[1].strip()
            return label.strip() or None, None
    return None, None


def _convert_node(cnode: dict[str, Any]) -> dict[str, Any] | None:
    """Convert a canvas node to a lattice YAML node. Returns None for skipped nodes."""
    node_type = cnode.get("type", "")
    node_id = _sanitize_node_id(cnode.get("id", ""))

    # Skip groups (except _lattice_meta, handled separately) and links
    if node_type in ("group", "link"):
        return None
    if cnode.get("id") == "_lattice_meta":
        return None

    if node_type == "file":
        return _convert_file_node(cnode)
    elif node_type == "text":
        return _convert_text_node(cnode)

    # Unknown type — treat as process
    return {
        "id": node_id,
        "type": "process",
        "description": str(cnode.get("text", "")),
    }


def _convert_file_node(cnode: dict[str, Any]) -> dict[str, Any]:
    """Convert a canvas file node to a lattice YAML node."""
    node_id = _sanitize_node_id(cnode["id"])
    file_path = cnode.get("file", "")

    # Infer type from path prefix
    if "what/modules/" in file_path or "/modules/" in file_path:
        node_type = "module"
    elif "what/datasets/" in file_path or "/datasets/" in file_path:
        node_type = "dataset"
    else:
        node_type = "module"  # Default fallback per interop spec

    # Strip .md extension for ref
    ref = file_path
    if ref.endswith(".md"):
        ref = ref[:-3]

    result: dict[str, Any] = {
        "id": node_id,
        "type": node_type,
        "ref": ref,
    }
    return result


def _convert_text_node(cnode: dict[str, Any]) -> dict[str, Any]:
    """Convert a canvas text node to a lattice YAML node."""
    node_id = _sanitize_node_id(cnode["id"])
    text = cnode.get("text", "")

    # Check for reasoning convention
    if REASONING_PREFIX_PATTERN.match(text):
        # Strip the "## Reasoning:" prefix to get prompt
        prompt = re.sub(r"^##\s*Reasoning:\s*", "", text, flags=re.IGNORECASE).strip()
        return {
            "id": node_id,
            "type": "reasoning",
            "prompt": prompt,
        }

    # Default: process node
    # Strip "## node_id\n\n" header if present (round-trip artifact)
    description = text
    header_pattern = re.compile(rf"^##\s*{re.escape(node_id)}\s*\n+", re.IGNORECASE)
    description = header_pattern.sub("", description).strip()

    return {
        "id": node_id,
        "type": "process",
        "description": description,
    }


def _convert_edge(cedge: dict[str, Any]) -> dict[str, Any]:
    """Convert a canvas edge to a lattice YAML edge."""
    source = _sanitize_node_id(cedge.get("fromNode", ""))
    target = _sanitize_node_id(cedge.get("toNode", ""))
    label = cedge.get("label", "")

    result: dict[str, Any] = {
        "from": source,
        "to": target,
    }

    # Strip condition suffix if present (round-trip artifact)
    condition = None
    if label:
        match = re.match(r"^(.+?)\s*\(if:\s*(.+?)\)\s*$", label)
        if match:
            label = match.group(1).strip()
            condition = match.group(2).strip()
        elif label.startswith("(if:"):
            match = re.match(r"^\(if:\s*(.+?)\)\s*$", label)
            if match:
                condition = match.group(1).strip()
                label = ""

    if label:
        result["label"] = label
    if condition:
        result["condition"] = condition

    return result


def canvas_file_to_lattice(
    canvas_path: str | Path,
    yaml_path: str | Path,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Convert an Obsidian .canvas file to a .lattice.yaml file.

    Args:
        canvas_path: Path to input .canvas file.
        yaml_path: Path to output .lattice.yaml file.
        **kwargs: Passed to canvas_to_lattice() for default metadata.

    Returns:
        The lattice dictionary that was written.

    Raises:
        FileNotFoundError: If canvas_path does not exist.
    """
    canvas_path = Path(canvas_path)
    yaml_path = Path(yaml_path)

    with open(canvas_path) as f:
        data = json.load(f)

    lattice = canvas_to_lattice(data, **kwargs)

    with open(yaml_path, "w") as f:
        yaml.dump(lattice, f, default_flow_style=False, sort_keys=False, width=120)

    return lattice
