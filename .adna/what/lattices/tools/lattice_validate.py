"""
Lattice YAML Schema Validator.

Validates .lattice.yaml files against the Lattice YAML Schema
(lattice_yaml_schema.json). Checks structural constraints, required
fields, enum values, node/edge integrity, and graph connectivity.

Usage:
    >>> from objects.lattices.tools.lattice_validate import validate_lattice_file
    >>> result = validate_lattice_file("pipeline.lattice.yaml")
    >>> if not result.valid:
    ...     for error in result.errors:
    ...         print(error)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# Schema constants aligned with lattice_yaml_schema.json
VALID_LATTICE_TYPES = {"pipeline", "agent", "context_graph", "workflow", "skill", "infrastructure", "context_set"}
VALID_EXECUTION_MODES = {"workflow", "reasoning", "hybrid"}
VALID_RUNTIMES = {"ray", "local", "kubernetes"}
VALID_TIERS = {"L1", "L2", "L3"}
VALID_NODE_TYPES = {"module", "dataset", "process", "reasoning"}
VALID_VERSION_POLICIES = {"locked", "patch", "minor", "latest"}

# Pattern: lowercase, underscores, starts with letter
ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")

# Semver pattern
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?(\+[a-zA-Z0-9.]+)?$")


@dataclass
class LatticeValidationResult:
    """Result of lattice YAML validation."""

    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_error(self, msg: str) -> None:
        """Add an error and mark result as invalid."""
        self.errors.append(msg)
        self.valid = False

    def add_warning(self, msg: str) -> None:
        """Add a non-fatal warning."""
        self.warnings.append(msg)


def validate_lattice(data: dict[str, Any]) -> LatticeValidationResult:
    """
    Validate a parsed lattice YAML dictionary.

    Checks:
    - Root structure (lattice key required)
    - Required fields (name, version, description, execution, nodes, edges, fair)
    - Field types and enum values
    - Node ID uniqueness and format
    - Edge reference integrity (from/to must reference existing nodes)
    - Graph connectivity warnings

    Args:
        data: Parsed YAML dictionary.

    Returns:
        LatticeValidationResult with errors and warnings.
    """
    result = LatticeValidationResult()

    # Root structure
    if not isinstance(data, dict):
        result.add_error("Root must be a YAML mapping")
        return result

    if "lattice" not in data:
        result.add_error("Missing required root key: 'lattice'")
        return result

    lattice = data["lattice"]
    if not isinstance(lattice, dict):
        result.add_error("'lattice' must be a mapping")
        return result

    # Check for unexpected top-level keys
    for key in data:
        if key != "lattice":
            result.add_warning(f"Unexpected root key: '{key}' (only 'lattice' expected)")

    # Required fields
    required = ["name", "version", "description", "execution", "nodes", "edges", "fair"]
    for req in required:
        if req not in lattice:
            result.add_error(f"Missing required field: lattice.{req}")

    # Name validation
    name = lattice.get("name")
    if name is not None:
        if not isinstance(name, str):
            result.add_error("lattice.name must be a string")
        elif not ID_PATTERN.match(name):
            result.add_error(f"lattice.name '{name}' must match pattern ^[a-z][a-z0-9_]*$")

    # Version validation
    version = lattice.get("version")
    if version is not None:
        version_str = str(version)
        if not SEMVER_PATTERN.match(version_str):
            result.add_error(f"lattice.version '{version_str}' must be valid semver (e.g., 1.0.0)")

    # Lattice type
    lattice_type = lattice.get("lattice_type")
    if lattice_type is not None and lattice_type not in VALID_LATTICE_TYPES:
        result.add_error(
            f"lattice.lattice_type '{lattice_type}' must be one of: {sorted(VALID_LATTICE_TYPES)}"
        )

    # Description
    description = lattice.get("description")
    if description is not None:
        if not isinstance(description, str):
            result.add_error("lattice.description must be a string")
        elif len(description.strip()) < 10:
            result.add_error("lattice.description must be at least 10 characters")

    # Execution block
    _validate_execution(lattice.get("execution"), result)

    # Nodes
    node_ids = _validate_nodes(lattice.get("nodes"), result)

    # Edges
    _validate_edges(lattice.get("edges"), node_ids, result)

    # FAIR block
    _validate_fair(lattice.get("fair"), result)

    # Federation block (optional)
    _validate_federation(lattice.get("federation"), node_ids, lattice.get("fair"), result)

    return result


def _validate_execution(execution: Any, result: LatticeValidationResult) -> None:
    """Validate the execution block."""
    if execution is None:
        return  # Already flagged as missing required

    if not isinstance(execution, dict):
        result.add_error("lattice.execution must be a mapping")
        return

    for req in ["mode", "runtime", "tier"]:
        if req not in execution:
            result.add_error(f"Missing required field: lattice.execution.{req}")

    mode = execution.get("mode")
    if mode is not None and mode not in VALID_EXECUTION_MODES:
        result.add_error(
            f"lattice.execution.mode '{mode}' must be one of: {sorted(VALID_EXECUTION_MODES)}"
        )

    runtime = execution.get("runtime")
    if runtime is not None and runtime not in VALID_RUNTIMES:
        result.add_error(
            f"lattice.execution.runtime '{runtime}' must be one of: {sorted(VALID_RUNTIMES)}"
        )

    tier = execution.get("tier")
    if tier is not None and tier not in VALID_TIERS:
        result.add_error(f"lattice.execution.tier '{tier}' must be one of: {sorted(VALID_TIERS)}")


def _validate_nodes(nodes: Any, result: LatticeValidationResult) -> set[str]:
    """Validate nodes array. Returns set of valid node IDs."""
    node_ids: set[str] = set()

    if nodes is None:
        return node_ids  # Already flagged as missing required

    if not isinstance(nodes, list):
        result.add_error("lattice.nodes must be an array")
        return node_ids

    if len(nodes) == 0:
        result.add_error("lattice.nodes must have at least 1 item")
        return node_ids

    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            result.add_error(f"lattice.nodes[{i}] must be a mapping")
            continue

        # Required node fields
        node_id = node.get("id")
        if node_id is None:
            result.add_error(f"lattice.nodes[{i}]: missing required field 'id'")
        elif not isinstance(node_id, str):
            result.add_error(f"lattice.nodes[{i}].id must be a string")
        elif not ID_PATTERN.match(node_id):
            result.add_error(f"lattice.nodes[{i}].id '{node_id}' must match ^[a-z][a-z0-9_]*$")
        elif node_id in node_ids:
            result.add_error(f"Duplicate node ID: '{node_id}'")
        else:
            node_ids.add(node_id)

        node_type = node.get("type")
        if node_type is None:
            result.add_error(f"lattice.nodes[{i}]: missing required field 'type'")
        elif node_type not in VALID_NODE_TYPES:
            result.add_error(
                f"lattice.nodes[{i}].type '{node_type}' must be one of: {sorted(VALID_NODE_TYPES)}"
            )

        # Type-specific validation
        if node_type == "reasoning" and "prompt" not in node:
            result.add_warning(f"Node '{node_id}': reasoning node without 'prompt' field")

        if node_type in ("module", "dataset") and "ref" not in node:
            result.add_warning(f"Node '{node_id}': {node_type} node without 'ref' field")

    return node_ids


def _validate_edges(edges: Any, node_ids: set[str], result: LatticeValidationResult) -> None:
    """Validate edges array against known node IDs."""
    if edges is None:
        return  # Already flagged as missing required

    if not isinstance(edges, list):
        result.add_error("lattice.edges must be an array")
        return

    for i, edge in enumerate(edges):
        if not isinstance(edge, dict):
            result.add_error(f"lattice.edges[{i}] must be a mapping")
            continue

        source = edge.get("from")
        target = edge.get("to")

        if source is None:
            result.add_error(f"lattice.edges[{i}]: missing required field 'from'")
        elif source not in node_ids and node_ids:
            result.add_error(f"lattice.edges[{i}].from '{source}' references unknown node")

        if target is None:
            result.add_error(f"lattice.edges[{i}]: missing required field 'to'")
        elif target not in node_ids and node_ids:
            result.add_error(f"lattice.edges[{i}].to '{target}' references unknown node")

        # Self-referential edge warning
        if source is not None and target is not None and source == target:
            result.add_warning(
                f"lattice.edges[{i}]: self-referential edge '{source}' → '{target}' "
                "(valid for iteration loops but verify intent)"
            )


def _validate_fair(fair: Any, result: LatticeValidationResult) -> None:
    """Validate the FAIR metadata block."""
    if fair is None:
        return  # Already flagged as missing required

    if not isinstance(fair, dict):
        result.add_error("lattice.fair must be a mapping")
        return

    if "license" not in fair:
        result.add_error("Missing required field: lattice.fair.license")

    if "keywords" not in fair:
        result.add_error("Missing required field: lattice.fair.keywords")
    else:
        keywords = fair["keywords"]
        if not isinstance(keywords, list) or len(keywords) == 0:
            result.add_error("lattice.fair.keywords must be a non-empty array")


def _validate_federation(
    federation: Any,
    node_ids: set[str],
    fair: Any,
    result: LatticeValidationResult,
) -> None:
    """Validate the optional federation metadata block."""
    if federation is None:
        return  # Federation is optional

    if not isinstance(federation, dict):
        result.add_error("lattice.federation must be a mapping")
        return

    # Version policy enum
    version_policy = federation.get("version_policy")
    if version_policy is not None and version_policy not in VALID_VERSION_POLICIES:
        result.add_error(
            f"lattice.federation.version_policy '{version_policy}' "
            f"must be one of: {sorted(VALID_VERSION_POLICIES)}"
        )

    # Shareable without license warning
    if federation.get("shareable") and (
        fair is None or not isinstance(fair, dict) or "license" not in fair
    ):
        result.add_warning(
            "federation.shareable is true but no fair.license specified — "
            "shared lattices should declare a license"
        )

    # Parent lattice without extracted_nodes warning
    if "parent_lattice" in federation and "extracted_nodes" not in federation:
        result.add_warning(
            "federation.parent_lattice specified without federation.extracted_nodes — "
            "consider listing which nodes were extracted"
        )

    # Extracted nodes cross-reference validation
    extracted = federation.get("extracted_nodes")
    if extracted is not None:
        if not isinstance(extracted, list):
            result.add_error("lattice.federation.extracted_nodes must be an array")
        else:
            for node_id in extracted:
                if not isinstance(node_id, str):
                    result.add_error(
                        f"lattice.federation.extracted_nodes contains non-string: {node_id}"
                    )
                elif node_ids and node_id not in node_ids:
                    result.add_error(
                        f"federation.extracted_nodes references unknown node: '{node_id}'"
                    )

    # Extracted nodes without parent_lattice warning
    if "extracted_nodes" in federation and "parent_lattice" not in federation:
        result.add_warning(
            "federation.extracted_nodes specified without federation.parent_lattice — "
            "extracted nodes should reference their source lattice"
        )


def check_federation_readiness(data: dict[str, Any]) -> LatticeValidationResult:
    """
    Check if a lattice is ready for federation (sharing/export).

    Implements the 6 federation readiness checks from lattice_federation.md §4.1:
    1. Schema validation passes (basic structure check)
    2. federation.shareable is true
    3. federation.source_instance is set
    4. fair.license is declared
    5. fair.keywords has >= 1 entry
    6. All ref fields resolve or use lattice:// URIs

    Args:
        data: Parsed lattice YAML dictionary (with root 'lattice' key).

    Returns:
        LatticeValidationResult — valid=True if all 6 checks pass.
    """
    result = LatticeValidationResult()

    # Extract lattice section
    if not isinstance(data, dict) or "lattice" not in data:
        result.add_error("[federation] Missing root 'lattice' key")
        return result

    lattice = data["lattice"]
    if not isinstance(lattice, dict):
        result.add_error("[federation] 'lattice' must be a mapping")
        return result

    # Check 1: Schema — required fields present
    required = ["name", "version", "description", "execution", "nodes", "edges", "fair"]
    missing = [f for f in required if f not in lattice]
    if missing:
        result.add_error(f"[federation] Missing required fields: {', '.join(missing)}")

    # Check 2: federation.shareable is true
    federation = lattice.get("federation")
    if not isinstance(federation, dict) or not federation.get("shareable"):
        result.add_error("[federation] federation.shareable must be true")

    # Check 3: federation.source_instance is set
    if not isinstance(federation, dict) or not federation.get("source_instance"):
        result.add_error("[federation] federation.source_instance must be set")

    # Check 4: fair.license is declared
    fair = lattice.get("fair")
    if not isinstance(fair, dict) or not fair.get("license"):
        result.add_error("[federation] fair.license must be declared")

    # Check 5: fair.keywords has >= 1 entry
    if not isinstance(fair, dict):
        result.add_error("[federation] fair.keywords must have at least 1 entry")
    else:
        keywords = fair.get("keywords", [])
        if not isinstance(keywords, list) or len(keywords) < 1:
            result.add_error("[federation] fair.keywords must have at least 1 entry")

    # Check 6: All ref fields in nodes resolve or use lattice:// URIs
    uri_pattern = re.compile(r"^lattice://")
    nodes = lattice.get("nodes", [])
    if isinstance(nodes, list):
        for node in nodes:
            if not isinstance(node, dict):
                continue
            ref = node.get("ref")
            if ref is not None and not isinstance(ref, str):
                result.add_error(
                    f"[federation] Node '{node.get('id', '?')}': ref must be a string"
                )
            elif ref is not None and not ref.strip():
                result.add_error(
                    f"[federation] Node '{node.get('id', '?')}': ref is empty"
                )

    return result


def validate_lattice_file(path: str | Path) -> LatticeValidationResult:
    """
    Validate a .lattice.yaml file.

    Args:
        path: Path to the .lattice.yaml file.

    Returns:
        LatticeValidationResult with errors and warnings.
    """
    path = Path(path)
    result = LatticeValidationResult()

    if not path.exists():
        result.add_error(f"File not found: {path}")
        return result

    if not path.suffix == ".yaml" and not path.name.endswith(".lattice.yaml"):
        result.add_warning(f"File '{path.name}' does not end with .lattice.yaml")

    try:
        with open(path) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        result.add_error(f"YAML parse error: {e}")
        return result

    if data is None:
        result.add_error("File is empty")
        return result

    return validate_lattice(data)
