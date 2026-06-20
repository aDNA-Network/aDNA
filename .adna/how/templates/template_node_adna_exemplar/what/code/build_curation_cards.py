#!/usr/bin/env python3
"""build_curation_cards.py — M22 per-vault curation card extractor.

Information-architecture twin of the visual M20/M21 tracks. Reads, never writes,
upstream sources; emits one curation card per live vault as a .yaml (single
editable source of truth) + a rendered human-readable .md.

Source-of-truth discipline (per who/curation/curation_schema.yaml):
  - inventory_vaults.yaml      → name, class→archetype, persona, path, governance,
                                 note→description_one_line, health→current_status,
                                 last_active_campaign (regex campaign_* from note)
  - what/vault_cards/the_*.md  → display_name, persona_archetype, img_path,
                                 github_url, manifest_path, state_path, body→paragraph
  - <Vault>/MANIFEST.md        → fair.{license,creators,keywords}, created→origin_date,
                                 federation.{shareable,discoverable,version_policy}
  - <Vault>/STATE.md           → last_mission_closed (frontmatter; null if absent)
  - on-disk probes             → image_path (vault card), persona_portrait

Nothing is invented. operator_note is empty by default (the only editorial field).

Usage:
    python3 what/code/build_curation_cards.py            # all 31 live vaults
    python3 what/code/build_curation_cards.py --only RareHarness.aDNA SiteForge.aDNA
    python3 what/code/build_curation_cards.py --check    # validate-only, no write
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

# ── Paths (vault-relative; resolved from this file's location) ────────────────
NODE_VAULT = Path(__file__).resolve().parents[2]          # Home.aDNA/
WORKSPACE = NODE_VAULT.parent                              # ~/aDNA/
INVENTORY = NODE_VAULT / "what" / "inventory" / "inventory_vaults.yaml"
VAULT_CARDS_DIR = NODE_VAULT / "what" / "vault_cards"      # the_*.md companion notes
ASSETS_CARDS = NODE_VAULT / "who" / "assets" / "vault_cards"
ASSETS_PORTRAITS = NODE_VAULT / "who" / "assets" / "portraits"
ASSETS_SIGILS = NODE_VAULT / "who" / "assets" / "sigils"
ASSETS_EMBLEMS = NODE_VAULT / "who" / "assets" / "emblems"
ASSETS_CRESTS = NODE_VAULT / "who" / "assets" / "crests"
OUT_DIR = NODE_VAULT / "who" / "curation"
SCHEMA = OUT_DIR / "curation_schema.yaml"

# ── Derivation maps (mirror curation_schema.yaml) ─────────────────────────────
CLASS_TO_ARCHETYPE = {
    "forge": "Forge",
    "framework": "Framework",
    "framework_candidate": "Framework",
    "platform": "Platform",
    "org_vault": "Org-Vault",
    "standard_dev": "Org-Vault",
    "org_graph": "Org-Graph",
    "network": "Network",
    "coordination": "Coordination",
    "node_operational": "Other",
    "document": "Domain",
    "knowledge_graph": "Domain",
    "tooling": "Domain",
    "workspace": "Domain",
}
HEALTH_TO_STATUS = {
    "active": "active",
    "genesis": "genesis",
    "genesis_stub": "genesis",
    "pending": "genesis",
    "production": "production",
    "superseded": "superseded",
    "archived": "archived",
}
EXCLUDE = {"ComicForge.aDNA"}  # superseded/archived; skipped by M20 image set

# M20-era vault-card images that predate later renames/casing. The image exists
# on disk under a prior name; map it to the current inventory vault_name so the
# card wires the real asset instead of dropping to null.
# 2026-05-31 (Hestia readiness pass): LatticeHome.aDNA.jpg renamed -> Home.aDNA.jpg, so the
# Home.aDNA vault-card image resolves directly. science_stanley was casing-corrected to
# ScienceStanley.aDNA in the inventory, so its image (ScienceStanley.aDNA.jpg) also resolves
# directly; the legacy alias below is now inert but kept harmless.
VAULT_CARD_IMAGE_ALIASES = {
    "science_stanley.aDNA": "ScienceStanley.aDNA.jpg",  # inert post-casing-fix (kept harmless)
}

REQUIRED_FIELDS = [
    "vault_name", "display_name", "archetype", "description_one_line",
    "description_paragraph", "source", "federation", "current_status",
    "key_links",
]


# ── Frontmatter helpers ───────────────────────────────────────────────────────
def read_frontmatter(path: Path) -> dict:
    """Parse the leading YAML frontmatter block of a markdown file. {} on failure."""
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        # Some companion notes / manifests open directly with frontmatter keys.
        block = text
    else:
        parts = text.split("---", 2)
        if len(parts) < 3:
            return {}
        block = parts[1]
    try:
        data = yaml.safe_load(block)
        return data if isinstance(data, dict) else {}
    except yaml.YAMLError:
        # Fall back to a tolerant single-line scalar grep for known-flat keys.
        out = {}
        for line in block.splitlines():
            m = re.match(r"^([a-z_]+):\s*(.+)$", line)
            if m:
                out[m.group(1)] = m.group(2).strip().strip("'\"")
        return out


def read_body(path: Path) -> str:
    """Return the markdown body (after frontmatter)."""
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2]
    return text


def first_sentence(text: str, limit: int) -> str:
    text = " ".join((text or "").split())
    if not text:
        return ""
    # Split on sentence end; keep first.
    m = re.search(r"(.+?[.!?])(\s|$)", text)
    s = m.group(1) if m else text
    if len(s) > limit:
        s = s[: limit - 1].rstrip() + "…"
    return s


def clamp(text: str, limit: int) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def extract_focus_paragraph(body: str) -> str:
    """Prefer the '## Current Focus' section text; else the italic tagline."""
    m = re.search(r"##\s+Current Focus\s*\n+(.+?)(\n#|\Z)", body, re.S)
    if m:
        return " ".join(m.group(1).split())
    # italic tagline directly under the H1 title
    m = re.search(r"^\*(.+?)\*\s*$", body, re.M)
    if m:
        return m.group(1).strip()
    return ""


def campaign_from_note(note: str) -> str | None:
    """Derive last_active_campaign from the inventory note (uniform upstream)."""
    if not note:
        return None
    m = re.search(r"(campaign_[a-z0-9_]+)", note)
    if not m:
        return None
    slug = m.group(1)
    # Grab a short phase/status tail if present right after the slug.
    tail = re.search(re.escape(slug) + r"\s+([^.;]{0,60})", note)
    if tail and tail.group(1).strip():
        return f"{slug} — {tail.group(1).strip()}"
    return slug


def truncate_mission(val) -> str | None:
    if val is None:
        return None
    s = str(val)
    return first_sentence(s, 120) or None


# M2.4: per-vault home-page icon resolution (emblem > persona sigil > category crest).
ARCHETYPE_TO_CREST = {
    "Forge": "forge", "Framework": "framework", "Platform": "platform",
    "Org-Vault": "org_vault", "Org-Graph": "org_graph", "Network": "network",
    "Coordination": "coordination", "Other": "node_tooling", "Domain": "node_tooling",
}


def resolve_icon(vault_name: str, persona, archetype: str) -> str | None:
    """Home-page vault icon: topic emblem first, then persona sigil, then category crest.
    Persona may be a composite string (e.g. 'stanley (platform) / panacea ...') — the
    first whitespace token is tried as a fallback so such vaults still resolve a sigil."""
    if (ASSETS_EMBLEMS / f"{vault_name}.png").exists():
        return f"who/assets/emblems/{vault_name}.png"
    if persona:
        cands = [persona] + ([persona.split()[0]] if persona.split() else [])
        for cand in cands:
            if (ASSETS_SIGILS / f"{cand}.png").exists():
                return f"who/assets/sigils/{cand}.png"
    slug = ARCHETYPE_TO_CREST.get(archetype)
    if slug and (ASSETS_CRESTS / f"{slug}.png").exists():
        return f"who/assets/crests/{slug}.png"
    return None


# ── Core build ────────────────────────────────────────────────────────────────
def build_card(entry: dict) -> dict:
    vault_name = entry["name"]
    vault_dir = WORKSPACE / vault_name
    cls = entry.get("class", "")
    persona = entry.get("persona")
    note = entry.get("note", "")

    # the_<Vault>.md companion note (M20-generated; uniform v0.2 frontmatter)
    the_path = VAULT_CARDS_DIR / f"the_{vault_name}.md"
    the_fm = read_frontmatter(the_path)
    the_body = read_body(the_path)

    # <Vault>/MANIFEST.md frontmatter (fair + federation where present)
    manifest_fm = read_frontmatter(vault_dir / "MANIFEST.md")
    fair = manifest_fm.get("fair", {}) if isinstance(manifest_fm.get("fair"), dict) else {}
    fed = manifest_fm.get("federation", {}) if isinstance(manifest_fm.get("federation"), dict) else {}

    # <Vault>/STATE.md last_mission_closed
    state_fm = read_frontmatter(vault_dir / "STATE.md")
    last_mission = truncate_mission(state_fm.get("last_mission_closed"))

    # archetype + status
    archetype = CLASS_TO_ARCHETYPE.get(cls, "Other")
    status = HEALTH_TO_STATUS.get(entry.get("health", ""), "genesis")
    if entry.get("superseded_by"):
        status = "superseded"

    # display name
    display_name = (
        the_fm.get("display_name")
        or entry.get("display_name")
        or vault_name.replace(".aDNA", "")
    )

    # descriptions
    one_line = clamp(first_sentence(note, 140), 140) or display_name
    focus = extract_focus_paragraph(the_body)
    paragraph = clamp(focus, 800) if focus else clamp(note, 800) or one_line

    # provenance
    repo = (the_fm.get("github_url") or "").strip() or "local-only"
    license_ = fair.get("license", "private")
    creators = fair.get("creators") or ["stanley"]
    if isinstance(creators, str):
        creators = [creators]
    keywords = fair.get("keywords") or []
    origin = str(
        fair.get("created")
        or manifest_fm.get("created")
        or the_fm.get("created")
        or ""
    ) or None

    # federation (default node-private)
    federation = {
        "shareable": bool(fed.get("shareable", False)),
        "discoverable": bool(fed.get("discoverable", False)),
        "version_policy": fed.get("version_policy"),
    }

    # image probes (on-disk truth; alias-aware for pre-rename/casing drift)
    card_img = ASSETS_CARDS / f"{vault_name}.jpg"
    if card_img.exists():
        image_path = f"who/assets/vault_cards/{vault_name}.jpg"
    elif vault_name in VAULT_CARD_IMAGE_ALIASES and (ASSETS_CARDS / VAULT_CARD_IMAGE_ALIASES[vault_name]).exists():
        image_path = f"who/assets/vault_cards/{VAULT_CARD_IMAGE_ALIASES[vault_name]}"
    else:
        image_path = None
    persona_portrait = None
    if persona:
        port = ASSETS_PORTRAITS / f"portrait_{persona}.jpg"
        if port.exists():
            persona_portrait = f"who/assets/portraits/portrait_{persona}.jpg"
        elif (ASSETS_SIGILS / f"{persona}.png").exists():
            # M25.5: a neon-heraldic sigil fills the persona slot when no painterly portrait exists
            # (gallery gap-fill for personas that postdate the M21 portrait set).
            persona_portrait = f"who/assets/sigils/{persona}.png"

    # key links
    governance = entry.get("governance") or the_fm.get("governance") or f"{vault_name}/CLAUDE.md"
    key_links = [{"label": "CLAUDE.md", "target_path": governance}]
    if the_fm.get("manifest_path"):
        key_links.append({"label": "MANIFEST.md", "target_path": the_fm["manifest_path"]})
    elif (vault_dir / "MANIFEST.md").exists():
        key_links.append({"label": "MANIFEST.md", "target_path": f"{vault_name}/MANIFEST.md"})
    if the_fm.get("state_path"):
        key_links.append({"label": "STATE.md", "target_path": the_fm["state_path"]})
    elif (vault_dir / "STATE.md").exists():
        key_links.append({"label": "STATE.md", "target_path": f"{vault_name}/STATE.md"})

    return {
        "type": "curation_card",
        "schema_version": "0.1",
        "vault_name": vault_name,
        "display_name": display_name,
        "archetype": archetype,
        "persona": persona,
        "description_one_line": one_line,
        "description_paragraph": paragraph,
        "source": {
            "repo": repo,
            "license": license_,
            "creators": creators,
            "keywords": keywords,
            "origin_date": origin,
        },
        "federation": federation,
        "current_status": status,
        "last_active_campaign": campaign_from_note(note),
        "last_mission_closed": last_mission,
        "key_links": key_links,
        "image_path": image_path,
        "icon_path": resolve_icon(vault_name, persona, archetype),
        "persona_portrait": persona_portrait,
        "operator_note": "",
        "_provenance": {
            "inventory": "what/inventory/inventory_vaults.yaml",
            "companion_note": f"what/vault_cards/the_{vault_name}.md" if the_path.exists() else None,
            "manifest": f"{vault_name}/MANIFEST.md" if (vault_dir / "MANIFEST.md").exists() else None,
            "state": f"{vault_name}/STATE.md" if (vault_dir / "STATE.md").exists() else None,
            "generated_by": "what/code/build_curation_cards.py",
        },
    }


def validate(card: dict) -> list[str]:
    errs = []
    for f in REQUIRED_FIELDS:
        if card.get(f) in (None, "", [], {}):
            errs.append(f"missing required field: {f}")
    if card["archetype"] not in CLASS_TO_ARCHETYPE.values() and card["archetype"] != "Other":
        errs.append(f"bad archetype: {card['archetype']}")
    if card["current_status"] not in {"genesis", "active", "production", "superseded", "archived"}:
        errs.append(f"bad current_status: {card['current_status']}")
    if len(card["description_one_line"]) > 140:
        errs.append("description_one_line > 140")
    if len(card["description_paragraph"]) > 800:
        errs.append("description_paragraph > 800")
    return errs


# ── Rendering (.md from .yaml) ────────────────────────────────────────────────
def render_md(card: dict) -> str:
    c = card
    persona = c["persona"] or "—"
    fm = {
        "type": "curation_card",
        "schema_version": "0.1",
        "vault": c["vault_name"],
        "display_name": c["display_name"],
        "archetype": c["archetype"],
        "persona": c["persona"],
        "current_status": c["current_status"],
        "description_one_line": c["description_one_line"],
        "image_path": c["image_path"],
        "icon_path": c["icon_path"],
        "persona_portrait": c["persona_portrait"],
        "last_active_campaign": c["last_active_campaign"],
        "tags": ["curation_card", "node_adna", f"archetype_{c['archetype'].lower().replace('-', '_')}"],
        "updated": "2026-05-31",
        "last_edited_by": "agent_stanley",
    }
    front = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()

    links = "\n".join(f"- [{l['label']}](../../../{l['target_path']})" for l in c["key_links"])
    src = c["source"]
    creators = ", ".join(src["creators"]) if src["creators"] else "—"
    kw = ", ".join(src["keywords"][:8]) if src["keywords"] else "—"
    op = c["operator_note"] or "*(none yet — editorial layer, opt-in)*"

    body = f"""# {c['display_name']}

> **{c['archetype']}**  ·  Persona **{persona}**  ·  Status **{c['current_status']}**

{c['description_paragraph']}

## At a glance

- **Pitch**: {c['description_one_line']}
- **Last active campaign**: {c['last_active_campaign'] or '—'}
- **Last mission closed**: {c['last_mission_closed'] or '—'}

## Provenance

- **Source**: {src['repo']}
- **License**: {src['license']}
- **Creators**: {creators}
- **Origin**: {src['origin_date'] or '—'}
- **Keywords**: {kw}
- **Federation**: shareable={c['federation']['shareable']} · discoverable={c['federation']['discoverable']} · policy={c['federation']['version_policy'] or '—'}

## Visual

- Vault card: `{c['image_path'] or '—'}`
- Persona portrait: `{c['persona_portrait'] or '—'}`

## Key links

{links}

## Operator note

{op}
"""
    return f"---\n{front}\n---\n\n{body}"


# ── Driver ────────────────────────────────────────────────────────────────────
def load_vaults() -> list[dict]:
    data = yaml.safe_load(INVENTORY.read_text(encoding="utf-8"))
    return [v for v in data.get("vaults", []) if v.get("name") not in EXCLUDE]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="restrict to these vault names")
    ap.add_argument("--check", action="store_true", help="validate only, no write")
    args = ap.parse_args()

    vaults = load_vaults()
    if args.only:
        sel = set(args.only)
        vaults = [v for v in vaults if v["name"] in sel]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    n_ok, n_err, n_written = 0, 0, 0
    for entry in vaults:
        card = build_card(entry)
        errs = validate(card)
        status = "OK " if not errs else "ERR"
        flags = []
        if not card["image_path"]:
            flags.append("no-card-img")
        if card["persona"] and not card["persona_portrait"]:
            flags.append("no-portrait")
        if not card["last_mission_closed"]:
            flags.append("no-last-mission")
        flagstr = (" [" + ",".join(flags) + "]") if flags else ""
        print(f"  {status} {card['vault_name']:<24} {card['archetype']:<12} {card['current_status']:<11}{flagstr}")
        if errs:
            n_err += 1
            for e in errs:
                print(f"       ! {e}")
            continue
        n_ok += 1
        if not args.check:
            slug = card["vault_name"]  # already includes .aDNA
            (OUT_DIR / f"curation_{slug}.yaml").write_text(
                yaml.safe_dump(card, sort_keys=False, allow_unicode=True), encoding="utf-8"
            )
            (OUT_DIR / f"curation_{slug}.md").write_text(render_md(card), encoding="utf-8")
            n_written += 1

    print(f"\n  vaults={len(vaults)} ok={n_ok} err={n_err} written={n_written} (×2 files)")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
