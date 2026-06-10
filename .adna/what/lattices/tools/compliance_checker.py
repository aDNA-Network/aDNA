#!/usr/bin/env python3
"""aDNA Compliance Checker — scores vault objects across 10 compliance dimensions.

Validates objects against the aDNA Universal Standard v2.2 and produces
YAML scorecards and Markdown reports.

Usage:
    python compliance_checker.py <vault_path>                          # Score all objects
    python compliance_checker.py <vault_path> --type skill             # Filter by type
    python compliance_checker.py <vault_path> --file what/modules/x.md # Single file
    python compliance_checker.py <vault_path> --output yaml --verbose  # YAML only, verbose
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

try:
    from .lattice_validate import check_federation_readiness, validate_lattice_file
except ImportError:
    from lattice_validate import check_federation_readiness, validate_lattice_file


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DISCOVERY_MAP: dict[str, list[str]] = {
    "module": ["what/modules/**/*.md"],
    "dataset": ["what/datasets/**/*.md"],
    "lattice": [
        "what/lattices/**/*.md",
        "what/lattices/**/*.lattice.yaml",
        "how/campaigns/**/*.lattice.yaml",
    ],
    "skill": ["how/skills/skill_*.md"],
    "context": ["what/context/**/*.md"],
    "hardware": ["what/hardware/hardware_*.md"],
    "manifest": ["how/campaigns/**/.campaign.yaml"],
}

EXCLUDE_NAMES = {"AGENTS.md", "README.md", "CLAUDE.md", "STATE.md"}
EXCLUDE_PREFIXES = ("template_",)
SKIP_DIRS = {".obsidian", ".claude", ".git", "node_modules"}
# Subdirectories excluded from specific discovery categories
SKIP_SUBDIRS: dict[str, set[str]] = {
    "lattice": {"skills"},  # companion lattice defs, counted under skills
}

# Valid frontmatter type values per discovery category.
# None = accept any type starting with the key string.
VALID_FM_TYPES: dict[str, set[str] | None] = {
    "module": {"module"},
    "dataset": {"dataset"},
    "lattice": {"lattice"},
    "skill": {"skill"},
    "context": None,  # accepts type starting with "context"
    "hardware": {"hardware"},
    "manifest": None,  # YAML files, no frontmatter type check
}

CANONICAL_IO_TYPES = frozenset(
    {
        "sequence",
        "structure_3d",
        "embedding",
        "annotation",
        "alignment",
        "parameters",
        "metrics",
        "text",
        "image",
        "audio",
        "video",
        "tabular",
        "graph",
        "binary",
        "document",
        "code",
        "config",
        "notification",
        "status",
    }
)

REQUIRED_FM_FIELDS = {"type", "created", "updated", "status", "tags", "last_edited_by"}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+")

ALL_DIMS = [f"d{i:02d}" for i in range(1, 11)]
DIM_NAMES = {
    "d01": "triad",
    "d02": "governance",
    "d03": "frontmatter",
    "d04": "fair",
    "d05": "type_vocab",
    "d06": "versioning",
    "d07": "federation",
    "d08": "registration",
    "d09": "companion",
    "d10": "reproducibility",
}

# N/A dimensions per type (scored as 3 in totals)
NA_MAP: dict[str, list[str]] = {
    "module": [],
    "dataset": ["d02", "d08"],
    "lattice": ["d02", "d08"],
    "skill": ["d05", "d06", "d09", "d10"],
    "context": ["d04", "d05", "d06", "d07", "d08", "d09", "d10"],
    "hardware": ["d02", "d04", "d05", "d08", "d09"],
    "manifest": ["d02", "d04", "d05", "d06", "d07", "d08", "d09", "d10"],
}

FEDERATION_CRITICAL = {"module", "dataset", "lattice"}

# Path prefix -> object type (for --file mode)
TYPE_FROM_PREFIX: dict[str, str] = {
    "what/modules/": "module",
    "what/datasets/": "dataset",
    "what/lattices/": "lattice",
    "how/skills/": "skill",
    "what/context/": "context",
    "what/hardware/": "hardware",
}


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------


@dataclass
class ComplianceResult:
    """Compliance score for a single vault object."""

    path: str
    object_type: str
    scores: dict[str, int] = field(default_factory=dict)
    na_dims: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    total: int = 0
    max_total: int = 30
    pct: float = 0.0
    tier: int = 3


# ---------------------------------------------------------------------------
# Frontmatter Parser
# ---------------------------------------------------------------------------


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter from a markdown file.

    Returns (frontmatter_dict, body_text). On failure returns ({}, "").
    """
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return {}, ""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        fm = yaml.safe_load(parts[1])
        return (fm if isinstance(fm, dict) else {}), parts[2]
    except yaml.YAMLError:
        return {}, content


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------


def discover_objects(
    vault_path: Path,
    type_filter: str | None = None,
) -> list[tuple[Path, str]]:
    """Discover vault objects via glob patterns.

    Returns sorted list of (path, object_type) tuples.
    """
    targets = (
        {type_filter: DISCOVERY_MAP[type_filter]}
        if type_filter and type_filter in DISCOVERY_MAP
        else DISCOVERY_MAP
    )

    seen: set[Path] = set()
    results: list[tuple[Path, str]] = []

    for obj_type, patterns in targets.items():
        for pattern in patterns:
            for path in sorted(vault_path.glob(pattern)):
                if path.name in EXCLUDE_NAMES:
                    continue
                if path.name.startswith(EXCLUDE_PREFIXES):
                    continue

                try:
                    rel_parts = path.relative_to(vault_path).parts
                except ValueError:
                    continue
                if any(part in SKIP_DIRS for part in rel_parts):
                    continue
                # Type-specific subdirectory exclusions
                type_skips = SKIP_SUBDIRS.get(obj_type)
                if type_skips and any(part in type_skips for part in rel_parts):
                    continue

                resolved = path.resolve()
                if resolved in seen:
                    continue
                seen.add(resolved)

                # For MD files (non-manifest), verify frontmatter and type
                if path.suffix == ".md" and obj_type != "manifest":
                    fm, _ = parse_frontmatter(path)
                    if not fm:
                        continue
                    # Validate frontmatter type matches expected category
                    fm_type = str(fm.get("type", ""))
                    valid = VALID_FM_TYPES.get(obj_type)
                    if valid is not None:
                        if fm_type not in valid:
                            continue
                    elif obj_type == "context":
                        if not fm_type.startswith("context"):
                            continue

                results.append((path, obj_type))

    return sorted(results, key=lambda x: str(x[0]))


# ---------------------------------------------------------------------------
# Scoring Infrastructure
# ---------------------------------------------------------------------------


def compute_tier(total: int, scores: dict[str, int], object_type: str) -> int:
    """Classify object into compliance tier (1=critical, 2=gaps, 3=compliant)."""
    if total < 15:
        return 1
    if total >= 23:
        return 3
    return 2


def identify_gaps(
    object_type: str,
    scores: dict[str, int],
    fm: dict[str, Any],
) -> list[str]:
    """Map dimension deficiencies to gap IDs.

    Gap ID Registry (G-001 to G-014):
      G-001 — (retired, merged into D1 triad scoring)
      G-002 — Lattice missing companion YAML
      G-003 — Skill missing lattice_type field
      G-004 — Dataset missing companion YAML
      G-005 — (retired, covered by D3 frontmatter scoring)
      G-006 — (retired, covered by D4 FAIR scoring)
      G-007 — Skill missing skill_type field
      G-008 — Campaign manifest missing required fields
      G-009 — Module missing version field (D6=0)
      G-010 — Module missing companion YAML
      G-011 — Context missing status field
      G-012 — Skill missing FAIR metadata (D4=0)
      G-013 — Federation-critical object missing federation metadata (D7=0)
      G-014 — (reserved for hardware migration gaps)
    """
    gaps: list[str] = []

    if object_type == "lattice" and scores.get("d09", 3) < 3:
        gaps.append("G-002")
    if object_type == "skill" and not fm.get("lattice_type"):
        gaps.append("G-003")
    if object_type == "dataset" and scores.get("d09", 3) < 3:
        gaps.append("G-004")
    if object_type == "skill" and not fm.get("skill_type"):
        gaps.append("G-007")
    if object_type == "manifest" and scores.get("d01", 3) < 3:
        gaps.append("G-008")
    if object_type == "module" and scores.get("d06", 3) == 0:
        gaps.append("G-009")
    if object_type == "module" and scores.get("d09", 3) < 3:
        gaps.append("G-010")
    if object_type == "context" and "status" not in fm:
        gaps.append("G-011")
    if object_type == "skill" and scores.get("d04", 3) == 0:
        gaps.append("G-012")
    if object_type in FEDERATION_CRITICAL and scores.get("d07", 3) == 0:
        gaps.append("G-013")

    return sorted(set(gaps))


def build_result(
    path: Path,
    object_type: str,
    scores: dict[str, int],
    vault_path: Path,
    fm: dict[str, Any],
) -> ComplianceResult:
    """Assemble a ComplianceResult from handler scores."""
    na_dims = list(NA_MAP.get(object_type, []))

    # MCP server modules use framework-defined types, not canonical I/O types.
    # Mark D5 (type_vocab) as N/A so they score 3/3 instead of 0-1.
    if object_type == "module" and fm.get("module_type") == "mcp_server":
        if "d05" not in na_dims:
            na_dims.append("d05")

    full_scores: dict[str, int] = {}
    for dim in ALL_DIMS:
        if dim in na_dims:
            full_scores[dim] = 3
        elif dim in scores:
            full_scores[dim] = max(0, min(3, scores[dim]))
        else:
            full_scores[dim] = 0

    total = sum(full_scores.values())
    pct = round((total / 30) * 100, 1)
    tier = compute_tier(total, full_scores, object_type)
    gaps = identify_gaps(object_type, full_scores, fm)

    try:
        rel_path = str(path.relative_to(vault_path))
    except ValueError:
        rel_path = str(path)

    return ComplianceResult(
        path=rel_path,
        object_type=object_type,
        scores=full_scores,
        na_dims=na_dims,
        gaps=gaps,
        total=total,
        max_total=30,
        pct=pct,
        tier=tier,
    )


def compute_aggregate(results: list[ComplianceResult]) -> dict[str, Any]:
    """Compute summary statistics across all results."""
    if not results:
        return {
            "aggregate_score": 0.0,
            "object_count": 0,
            "tier_1_count": 0,
            "tier_2_count": 0,
            "tier_3_count": 0,
            "gaps_active": 0,
        }

    tier_counts = {1: 0, 2: 0, 3: 0}
    all_gaps: set[str] = set()
    for r in results:
        tier_counts[r.tier] += 1
        all_gaps.update(r.gaps)

    return {
        "aggregate_score": round(sum(r.pct for r in results) / len(results), 1),
        "object_count": len(results),
        "tier_1_count": tier_counts[1],
        "tier_2_count": tier_counts[2],
        "tier_3_count": tier_counts[3],
        "gaps_active": len(all_gaps),
    }


def compute_by_type(
    results: list[ComplianceResult],
) -> dict[str, dict[str, Any]]:
    """Compute per-type averages and tier counts."""
    buckets: dict[str, list[ComplianceResult]] = {}
    for r in results:
        buckets.setdefault(r.object_type, []).append(r)

    summary: dict[str, dict[str, Any]] = {}
    for obj_type in sorted(buckets):
        items = buckets[obj_type]
        tiers = {1: 0, 2: 0, 3: 0}
        for r in items:
            tiers[r.tier] += 1
        summary[obj_type] = {
            "count": len(items),
            "avg_score": round(sum(r.total for r in items) / len(items), 1),
            "avg_pct": round(sum(r.pct for r in items) / len(items), 1),
            "tier_1": tiers[1],
            "tier_2": tiers[2],
            "tier_3": tiers[3],
        }
    return summary


def compute_by_dimension(
    results: list[ComplianceResult],
) -> dict[str, dict[str, Any]]:
    """Compute per-dimension averages (applicable objects only)."""
    summary: dict[str, dict[str, Any]] = {}
    for dim in ALL_DIMS:
        applicable = [r.scores[dim] for r in results if dim not in r.na_dims]
        if not applicable:
            continue
        avg = sum(applicable) / len(applicable)
        label = f"{dim}_{DIM_NAMES[dim]}"
        summary[label] = {
            "avg": round(avg, 2),
            "pct": round((avg / 3) * 100, 1),
            "applicable_count": len(applicable),
        }
    return summary


# ---------------------------------------------------------------------------
# Shared Scoring Helpers
# ---------------------------------------------------------------------------


def _check_agents_md(path: Path) -> int:
    """D2 — AGENTS.md existence in parent directory."""
    return 3 if (path.parent / "AGENTS.md").exists() else 0


def _score_frontmatter(fm: dict[str, Any]) -> int:
    """D3 — frontmatter schema completeness."""
    if not fm:
        return 0
    missing = REQUIRED_FM_FIELDS - set(fm.keys())
    if not missing:
        return 3
    if len(missing) <= 2:
        return 2
    if "type" in fm:
        return 1
    return 0


def _score_fair(fm: dict[str, Any]) -> int:
    """D4 — FAIR metadata block. Handles both flat and nested structures."""
    fair = fm.get("fair")
    if not fair or not isinstance(fair, dict):
        return 0

    # Flat: fair.keywords, fair.license
    has_license = bool(fair.get("license"))
    kw = fair.get("keywords", [])
    has_keywords = isinstance(kw, list) and len(kw) > 0

    # Nested: fair.findable.keywords, fair.accessible.license
    if not has_keywords:
        findable = fair.get("findable")
        if isinstance(findable, dict):
            kw = findable.get("keywords", [])
            has_keywords = isinstance(kw, list) and len(kw) > 0
    if not has_license:
        accessible = fair.get("accessible")
        if isinstance(accessible, dict):
            has_license = bool(accessible.get("license"))

    if has_license and has_keywords:
        return 3
    if has_license or has_keywords:
        return 2
    return 1


def _score_type_vocab(fm: dict[str, Any]) -> int:
    """D5 — I/O type vocabulary compliance."""
    # Check frontmatter inputs/outputs first
    inputs = fm.get("inputs", [])
    outputs = fm.get("outputs", [])
    if inputs or outputs:
        all_types: list[str] = []
        for io_list in (inputs, outputs):
            if isinstance(io_list, list):
                for item in io_list:
                    if isinstance(item, dict) and "type" in item:
                        all_types.append(str(item["type"]))
                    elif isinstance(item, str):
                        all_types.append(item)
        if not all_types:
            return 1
        canonical = sum(1 for t in all_types if t in CANONICAL_IO_TYPES)
        if canonical == len(all_types):
            return 3
        if canonical > 0:
            return 2
        return 1

    # Check fair.interoperable for format/schema (indicates type awareness)
    fair = fm.get("fair")
    if isinstance(fair, dict):
        interop = fair.get("interoperable")
        if isinstance(interop, dict) and (interop.get("format") or interop.get("schema")):
            return 2

    return 0


def _score_version(fm: dict[str, Any]) -> int:
    """D6 — version field (SemVer preferred)."""
    version = fm.get("version")
    if not version:
        for alt in ("context_version", "schema_version"):
            if fm.get(alt):
                return 1
        return 0
    return 3 if SEMVER_RE.match(str(version)) else 2


def _score_federation_md(fm: dict[str, Any]) -> int:
    """D7 — federation readiness from frontmatter.

    Note: This scores D7 for MD-based objects (modules, datasets, skills, hardware)
    using frontmatter federation fields (discoverable, source_instance). Lattice YAML
    files use a separate path via check_federation_readiness() in handle_lattice_yaml(),
    which checks the 6 federation readiness criteria from lattice_federation.md §4.1.
    This dual-path is intentional — MD objects have simpler federation metadata.
    """
    fed = fm.get("federation")
    if not fed or not isinstance(fed, dict):
        return 0
    discoverable = fed.get("discoverable")
    source = fed.get("source_instance")
    if discoverable and source:
        return 3
    if discoverable:
        return 2
    return 1


def _validate_companion_yaml(companion_path: Path, companion_type: str = "") -> bool:
    """Check that a companion YAML file is parseable and has type-specific required fields."""
    try:
        with open(companion_path) as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict) or len(data) == 0:
            return False
        # Type-specific required field checks
        if companion_type == "module":
            return bool(data.get("name") or data.get("module"))
        if companion_type == "dataset":
            return bool(data.get("name") or data.get("dataset"))
        return True
    except (OSError, yaml.YAMLError):
        return False


def _score_companion(path: Path, object_type: str) -> int:
    """D9 — companion file existence and content validation."""
    stem = path.stem
    parent = path.parent

    if object_type == "module":
        cp = parent / f"{stem}.module.yaml"
        if not cp.exists():
            return 0
        return 3 if _validate_companion_yaml(cp, "module") else 2
    if object_type == "dataset":
        cp = parent / f"{stem}.dataset.yaml"
        if not cp.exists():
            return 0
        return 3 if _validate_companion_yaml(cp, "dataset") else 2
    if object_type == "lattice":
        if path.suffix == ".md":
            cp = parent / f"{stem}.lattice.yaml"
            if not cp.exists():
                return 0
            return 3 if _validate_companion_yaml(cp, "lattice") else 2
        # YAML lattice — .md wrapper optional, score 2 if missing
        md_name = path.name.replace(".lattice.yaml", ".md")
        return 3 if (parent / md_name).exists() else 2
    return 0


def _score_execution(fm: dict[str, Any]) -> int:
    """D10 — reproducibility / execution metadata."""
    execution = fm.get("execution")
    if execution and isinstance(execution, dict):
        fields = {"mode", "runtime", "tier"}
        present = fields & set(execution.keys())
        if len(present) == 3:
            return 3
        if present:
            return 2
        return 1
    # Check loose execution-related fields
    exec_fields = ["runtime", "entrypoint", "gpu_required", "memory_mb", "container"]
    present = sum(1 for f in exec_fields if fm.get(f) is not None)
    if present >= 2:
        return 2
    if present >= 1:
        return 1
    # Check dataset-specific reproducibility fields
    repro_fields = ["format", "schema_version", "lineage", "storage"]
    repro = sum(1 for f in repro_fields if fm.get(f) is not None)
    if repro >= 1:
        return 1
    return 0


# ---------------------------------------------------------------------------
# Type Handlers
# ---------------------------------------------------------------------------


def handle_module(
    path: Path, fm: dict[str, Any], body: str, vault_path: Path
) -> dict[str, int]:
    """Score a module across all 10 dimensions."""
    return {
        "d01": 3 if fm.get("type") == "module" else (2 if fm.get("type") else 0),
        "d02": _check_agents_md(path),
        "d03": _score_frontmatter(fm),
        "d04": _score_fair(fm),
        "d05": _score_type_vocab(fm),
        "d06": _score_version(fm),
        "d07": _score_federation_md(fm),
        "d08": 3 if fm.get("type") == "module" else (1 if fm.get("type") else 0),
        "d09": _score_companion(path, "module"),
        "d10": _score_execution(fm),
    }


def handle_dataset(
    path: Path, fm: dict[str, Any], body: str, vault_path: Path
) -> dict[str, int]:
    """Score a dataset (including targets) on applicable dimensions."""
    t = fm.get("type", "")
    return {
        "d01": 3 if t in ("dataset", "target") else (2 if t else 0),
        "d03": _score_frontmatter(fm),
        "d04": _score_fair(fm),
        "d05": _score_type_vocab(fm),
        "d06": _score_version(fm),
        "d07": _score_federation_md(fm),
        "d09": _score_companion(path, "dataset"),
        "d10": _score_execution(fm),
    }


def handle_lattice_md(
    path: Path, fm: dict[str, Any], body: str, vault_path: Path
) -> dict[str, int]:
    """Score a lattice markdown wrapper on applicable dimensions."""
    return {
        "d01": 3 if fm.get("type") == "lattice" else (2 if fm.get("type") else 0),
        "d03": _score_frontmatter(fm),
        "d04": _score_fair(fm),
        "d05": _score_type_vocab(fm),
        "d06": _score_version(fm),
        "d07": _score_federation_md(fm),
        "d09": _score_companion(path, "lattice"),
        "d10": _score_execution(fm),
    }


def handle_lattice_yaml(path: Path, vault_path: Path) -> dict[str, int]:
    """Score a lattice YAML file, wrapping lattice_validate.py."""
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
    except (OSError, yaml.YAMLError):
        return {d: 0 for d in ("d01", "d03", "d04", "d05", "d06", "d07", "d09", "d10")}

    if not isinstance(data, dict) or "lattice" not in data:
        return {d: 0 for d in ("d01", "d03", "d04", "d05", "d06", "d07", "d09", "d10")}

    lattice = data.get("lattice", {})
    if not isinstance(lattice, dict):
        lattice = {}

    scores: dict[str, int] = {}

    # D1 — Valid lattice structure (via lattice_validate.py)
    try:
        vresult = validate_lattice_file(path)
        scores["d01"] = 3 if vresult.valid else (1 if lattice else 0)
    except Exception:
        scores["d01"] = 1 if lattice else 0

    # D3 — Schema completeness (required lattice fields)
    required = {"name", "version", "description", "execution", "nodes", "edges", "fair"}
    present = required & set(lattice.keys())
    missing_count = len(required - present)
    if missing_count == 0:
        scores["d03"] = 3
    elif missing_count <= 2:
        scores["d03"] = 2
    elif present:
        scores["d03"] = 1
    else:
        scores["d03"] = 0

    # D4 — FAIR metadata
    fair = lattice.get("fair")
    if isinstance(fair, dict):
        has_lic = bool(fair.get("license"))
        kw = fair.get("keywords", [])
        has_kw = isinstance(kw, list) and len(kw) > 0
        scores["d04"] = 3 if (has_lic and has_kw) else (2 if (has_lic or has_kw) else 1)
    else:
        scores["d04"] = 0

    # D5 — Type vocabulary (node type annotations)
    nodes = lattice.get("nodes", [])
    if isinstance(nodes, list) and nodes:
        has_types = all(
            isinstance(n, dict) and "type" in n for n in nodes if isinstance(n, dict)
        )
        scores["d05"] = 3 if has_types else 1
    else:
        scores["d05"] = 0

    # D6 — Versioning
    v = lattice.get("version")
    if v and SEMVER_RE.match(str(v)):
        scores["d06"] = 3
    elif v:
        scores["d06"] = 2
    else:
        scores["d06"] = 0

    # D7 — Federation readiness (via lattice_validate.py)
    try:
        fed_result = check_federation_readiness(data)
        if fed_result.valid:
            scores["d07"] = 3
        elif len(fed_result.errors) <= 2:
            scores["d07"] = 2
        elif len(fed_result.errors) <= 4:
            scores["d07"] = 1
        else:
            scores["d07"] = 0
    except Exception:
        fed = lattice.get("federation")
        if isinstance(fed, dict) and fed.get("discoverable"):
            scores["d07"] = 2
        elif isinstance(fed, dict):
            scores["d07"] = 1
        else:
            scores["d07"] = 0

    # D9 — Companion (.md wrapper)
    scores["d09"] = _score_companion(path, "lattice")

    # D10 — Execution block
    execution = lattice.get("execution")
    if isinstance(execution, dict):
        fields = {"mode", "runtime", "tier"} & set(execution.keys())
        scores["d10"] = 3 if len(fields) == 3 else (2 if fields else 1)
    else:
        scores["d10"] = 0

    return scores


def handle_skill(
    path: Path, fm: dict[str, Any], body: str, vault_path: Path
) -> dict[str, int]:
    """Score a skill on applicable dimensions."""
    lt = fm.get("lattice_type")
    return {
        "d01": 3 if fm.get("type") == "skill" else (2 if fm.get("type") else 0),
        "d02": _check_agents_md(path),
        "d03": _score_frontmatter(fm),
        "d04": _score_fair(fm),
        "d07": _score_federation_md(fm),
        "d08": 3 if lt == "skill" else (2 if lt else 0),
    }


def handle_context(
    path: Path, fm: dict[str, Any], body: str, vault_path: Path
) -> dict[str, int]:
    """Score a context file on applicable dimensions."""
    return {
        "d01": 3 if fm.get("type") == "context" else (2 if fm.get("type") else 0),
        "d02": _check_agents_md(path),
        "d03": _score_frontmatter(fm),
    }


def handle_hardware(
    path: Path, fm: dict[str, Any], body: str, vault_path: Path
) -> dict[str, int]:
    """Score hardware on applicable dimensions."""
    return {
        "d01": 3 if fm.get("type") == "hardware" else (2 if fm.get("type") else 0),
        "d03": _score_frontmatter(fm),
        "d06": _score_version(fm),
        "d07": _score_federation_md(fm),
        "d10": _score_execution(fm),
    }


def handle_manifest(path: Path, vault_path: Path) -> dict[str, int]:
    """Score a .campaign.yaml manifest on applicable dimensions."""
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
    except (OSError, yaml.YAMLError):
        return {"d01": 0, "d03": 0}

    if not isinstance(data, dict):
        return {"d01": 0, "d03": 0}

    # D1 — has campaign_id
    d01 = 3 if data.get("campaign_id") else (2 if data.get("name") else 0)

    # D3 — required manifest fields
    required = {"campaign_id", "phase_count", "mission_count", "status"}
    missing = len(required - set(data.keys()))
    if missing == 0:
        d03 = 3
    elif missing <= 2:
        d03 = 2
    elif required & set(data.keys()):
        d03 = 1
    else:
        d03 = 0

    return {"d01": d01, "d03": d03}


# Handler dispatch for MD-based objects
HANDLERS: dict[str, Any] = {
    "module": handle_module,
    "dataset": handle_dataset,
    "skill": handle_skill,
    "context": handle_context,
    "hardware": handle_hardware,
}


# ---------------------------------------------------------------------------
# Output Formatters
# ---------------------------------------------------------------------------


def format_scorecard_yaml(
    summary: dict[str, Any],
    by_type: dict[str, Any],
    by_dim: dict[str, Any],
    results: list[ComplianceResult],
    vault_path: Path,
) -> str:
    """Format results as a YAML scorecard."""
    scorecard = {
        "meta": {
            "generated": datetime.now(timezone.utc).isoformat(),
            "vault": vault_path.name,
            "standard_version": "2.2",
            "schema_version": "1.0",
            "object_count": summary["object_count"],
        },
        "summary": {k: v for k, v in summary.items()},
        "by_type": by_type,
        "by_dimension": by_dim,
        "objects": [
            {
                "path": r.path,
                "type": r.object_type,
                "total": r.total,
                "pct": r.pct,
                "tier": r.tier,
                "scores": dict(r.scores),
                "gaps": r.gaps,
            }
            for r in sorted(results, key=lambda r: (r.tier, -r.pct))
        ],
    }
    return yaml.dump(
        scorecard, default_flow_style=False, sort_keys=False, allow_unicode=True
    )


def format_report_md(
    summary: dict[str, Any],
    by_type: dict[str, Any],
    by_dim: dict[str, Any],
    results: list[ComplianceResult],
) -> str:
    """Format results as a Markdown report."""
    lines = [
        "# aDNA Compliance Report",
        "",
        f"**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Objects scanned**: {summary['object_count']}",
        f"**Aggregate score**: {summary['aggregate_score']}%",
        "",
        "| Tier | Count | Description |",
        "|-----:|------:|-------------|",
        f"| 1 | {summary['tier_1_count']} | Critical — federation-blocking |",
        f"| 2 | {summary['tier_2_count']} | Standard gaps |",
        f"| 3 | {summary['tier_3_count']} | Compliant |",
        "",
        f"**Active gap categories**: {summary['gaps_active']}",
        "",
        "## By Type",
        "",
        "| Type | Count | Avg Score | Avg % | T1 | T2 | T3 |",
        "|------|------:|----------:|------:|---:|---:|---:|",
    ]
    for t, info in sorted(by_type.items()):
        lines.append(
            f"| {t} | {info['count']} | {info['avg_score']}/30 "
            f"| {info['avg_pct']}% | {info['tier_1']} | {info['tier_2']} | {info['tier_3']} |"
        )

    lines += [
        "",
        "## By Dimension",
        "",
        "| Dimension | Avg | % | Objects |",
        "|-----------|----:|--:|--------:|",
    ]
    for dim_label, info in by_dim.items():
        lines.append(
            f"| {dim_label} | {info['avg']}/3 "
            f"| {info['pct']}% | {info['applicable_count']} |"
        )

    # Tier 1 objects
    tier1 = [r for r in results if r.tier == 1]
    if tier1:
        lines += ["", "## Tier 1 Objects (Critical)", ""]
        for r in sorted(tier1, key=lambda x: x.pct):
            gap_str = ", ".join(r.gaps) if r.gaps else "none"
            lines.append(
                f"- **{r.path}** ({r.object_type}) — "
                f"{r.total}/30 ({r.pct}%) — {gap_str}"
            )

    # Weakest dimensions
    worst = sorted(by_dim.items(), key=lambda x: x[1]["pct"])[:3]
    if worst:
        lines += ["", "## Weakest Dimensions", ""]
        for dim_label, info in worst:
            lines.append(f"- **{dim_label}**: {info['pct']}% (avg {info['avg']}/3)")

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="aDNA Compliance Checker — scores vault objects across 10 dimensions",
    )
    parser.add_argument("vault_path", help="Path to vault root")
    parser.add_argument(
        "--type",
        choices=sorted(DISCOVERY_MAP.keys()),
        help="Filter to specific object type",
    )
    parser.add_argument(
        "--output",
        choices=["yaml", "md", "both"],
        default="both",
        help="Output format (default: both)",
    )
    parser.add_argument(
        "--file", dest="single_file", help="Score a single file (relative to vault)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show per-object scores"
    )
    parser.add_argument(
        "--outdir", default=".", help="Directory for output files (default: cwd)"
    )
    return parser.parse_args(argv)


def _infer_type(path: Path, vault_path: Path) -> str | None:
    """Infer object type from file path."""
    if path.name == ".campaign.yaml":
        return "manifest"

    try:
        rel = str(path.relative_to(vault_path))
    except ValueError:
        return None

    for prefix, obj_type in TYPE_FROM_PREFIX.items():
        if rel.startswith(prefix):
            return obj_type

    # Fallback: check frontmatter
    if path.suffix == ".md":
        fm, _ = parse_frontmatter(path)
        return fm.get("type")
    return None


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    vault = Path(args.vault_path).resolve()

    if not vault.is_dir():
        print(f"Error: '{vault}' is not a directory", file=sys.stderr)
        return 2

    # Discover objects
    if args.single_file:
        fp = Path(args.single_file)
        file_path = (vault / fp) if not fp.is_absolute() else fp
        file_path = file_path.resolve()
        obj_type = _infer_type(file_path, vault)
        if not obj_type:
            print(f"Error: cannot determine type for '{file_path}'", file=sys.stderr)
            return 1
        objects = [(file_path, obj_type)]
    else:
        objects = discover_objects(vault, args.type)

    if args.verbose:
        print(f"Discovered {len(objects)} objects in {vault}")

    # Score each object
    results: list[ComplianceResult] = []
    for path, obj_type in objects:
        fm: dict[str, Any] = {}

        if obj_type == "manifest":
            scores = handle_manifest(path, vault)
        elif obj_type == "lattice" and path.suffix == ".yaml":
            scores = handle_lattice_yaml(path, vault)
        else:
            fm, body = parse_frontmatter(path)
            if not fm:
                if args.verbose:
                    try:
                        print(f"  SKIP (no frontmatter): {path.relative_to(vault)}")
                    except ValueError:
                        print(f"  SKIP (no frontmatter): {path}")
                continue
            handler = HANDLERS.get(obj_type)
            if handler:
                scores = handler(path, fm, body, vault)
            elif obj_type == "lattice":
                scores = handle_lattice_md(path, fm, body, vault)
            else:
                if args.verbose:
                    try:
                        print(
                            f"  SKIP (unknown type '{obj_type}'): "
                            f"{path.relative_to(vault)}"
                        )
                    except ValueError:
                        print(f"  SKIP (unknown type '{obj_type}'): {path}")
                continue

        result = build_result(path, obj_type, scores, vault, fm)
        results.append(result)

        if args.verbose:
            print(f"  {result.path}: {result.total}/30 ({result.pct}%) T{result.tier}")

    # Aggregate
    summary = compute_aggregate(results)
    by_type = compute_by_type(results)
    by_dim = compute_by_dimension(results)

    # Write outputs
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    if args.output in ("yaml", "both"):
        yaml_out = format_scorecard_yaml(summary, by_type, by_dim, results, vault)
        out_path = outdir / "compliance_scorecard.yaml"
        out_path.write_text(yaml_out)
        print(f"Wrote {out_path}")

    if args.output in ("md", "both"):
        md_out = format_report_md(summary, by_type, by_dim, results)
        out_path = outdir / "compliance_report.md"
        out_path.write_text(md_out)
        print(f"Wrote {out_path}")

    # Summary to stdout
    print(f"\n{'=' * 50}")
    print(f"Objects: {summary['object_count']}")
    print(f"Aggregate: {summary['aggregate_score']}%")
    print(
        f"Tiers: {summary['tier_1_count']} T1 | "
        f"{summary['tier_2_count']} T2 | "
        f"{summary['tier_3_count']} T3"
    )
    print(f"Active gaps: {summary['gaps_active']}")
    print(f"{'=' * 50}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
