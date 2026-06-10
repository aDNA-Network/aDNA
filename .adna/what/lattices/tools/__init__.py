"""
Lattice YAML Tools.

Provides validation, compliance checking, and bidirectional conversion
between .lattice.yaml and Obsidian .canvas formats.

Tools:
    - lattice_validate: Validate .lattice.yaml against schema
    - compliance_checker: Score vault objects across 10 compliance dimensions
    - lattice2canvas: Convert .lattice.yaml → .canvas JSON
    - canvas2lattice: Convert .canvas JSON → .lattice.yaml
"""

from .canvas2lattice import (
    canvas_file_to_lattice,
    canvas_to_lattice,
)
from .compliance_checker import (
    ComplianceResult,
    discover_objects,
    parse_frontmatter,
)
from .lattice2canvas import (
    lattice_file_to_canvas,
    lattice_to_canvas,
)
from .lattice_validate import (
    LatticeValidationResult,
    validate_lattice,
    validate_lattice_file,
)

__all__ = [
    "validate_lattice",
    "validate_lattice_file",
    "LatticeValidationResult",
    "ComplianceResult",
    "discover_objects",
    "parse_frontmatter",
    "lattice_to_canvas",
    "lattice_file_to_canvas",
    "canvas_to_lattice",
    "canvas_file_to_lattice",
]
