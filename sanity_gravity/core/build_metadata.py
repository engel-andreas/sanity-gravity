"""Build metadata: records component dimensions for composite tags.

When ``build`` is invoked with explicit flags (``--base``, ``--agents``,
etc.) rather than a legacy ``--variant`` tag, it writes a JSON metadata
file into ``config/builds/<tag>/meta.json``. This file records the
selected components so that ``up`` and ``list`` can reconstruct the
compose configuration without needing to parse the tag string.

The metadata file also stores ``providers`` (which are not part of the
image but affect the runtime compose overlay) and an optional ``name``
field for user-assigned build names.

Layout::

    config/
      builds/
        ag_cc-xfce-kasm-ollama/
          meta.json
        mein-sandbox/           # named build (alias)
          meta.json
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


METADATA_DIR = os.path.join("config", "builds")


def build_metadata_path(tag: str) -> str:
    """Return the path to the metadata file for a given tag."""
    return os.path.join(METADATA_DIR, tag, "meta.json")


def write_build_metadata(
    tag: str,
    *,
    base_image: str,
    agents: list[str],
    desktop: str,
    connector: str,
    providers: list[str] | None = None,
    name: str | None = None,
    source_flags: dict[str, Any] | None = None,
) -> str:
    """Write build metadata for a composite tag.

    ``name`` is an optional user-assigned build name. When set, a
    second metadata file is written under ``config/builds/<name>/``
    that points back to the real tag, so ``up --variant <name>``
    resolves to the correct image.

    Returns the path to the written file.
    """
    data: dict[str, Any] = {
        "tag": tag,
        "base_image": base_image,
        "agents": agents,
        "desktop": desktop,
        "connector": connector,
        "providers": providers or [],
    }
    if name:
        data["name"] = name
    if source_flags:
        data["source_flags"] = source_flags

    path = build_metadata_path(tag)
    parent = os.path.dirname(path)
    os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=2)

    # Write an alias entry so the name resolves back to the tag.
    if name and name != tag:
        alias_data: dict[str, Any] = {
            "tag": tag,
            "name": name,
            "alias": True,
        }
        alias_path = build_metadata_path(name)
        alias_parent = os.path.dirname(alias_path)
        os.makedirs(alias_parent, exist_ok=True)
        with open(alias_path, "w", encoding="utf-8") as fp:
            json.dump(alias_data, fp, indent=2)

    return path


def read_build_metadata(tag: str) -> dict[str, Any] | None:
    """Read build metadata for a tag, or ``None`` if not found.

    Handles both real metadata files and name-alias files: if the
    entry is an alias (``"alias": true``), follows it to the real tag.
    """
    path = build_metadata_path(tag)
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    # Follow alias: read the real tag's metadata instead.
    if data.get("alias") and "tag" in data:
        return read_build_metadata(data["tag"])
    return data


def resolve_build_name(name: str) -> str | None:
    """Resolve a user-assigned build name to the real composite tag.

    Returns the tag string if a metadata entry exists for ``name``,
    or ``None`` if not found. For alias entries, returns the target
    tag (not the alias itself).
    """
    meta = read_build_metadata(name)
    if meta is None:
        return None
    return meta.get("tag")


def list_built_entries() -> list[dict[str, Any]]:
    """List all built entries (tags + named aliases) with their metadata.

    Returns a list of dicts sorted by name/tag, each containing:
    ``tag``, ``name`` (if set), ``base_image``, ``agents``, ``desktop``,
    ``connector``, ``providers``.
    """
    if not os.path.isdir(METADATA_DIR):
        return []
    entries: list[dict[str, Any]] = []
    seen_tags: set[str] = set()
    for entry in sorted(os.listdir(METADATA_DIR)):
        meta = read_build_metadata(entry)
        if meta is None:
            continue
        tag = meta.get("tag", entry)
        if tag in seen_tags:
            continue  # skip aliases pointing to already-listed tags
        seen_tags.add(tag)
        entries.append(meta)
    return entries


def list_built_tags() -> list[str]:
    """List all tags that have build metadata (tags only, no aliases)."""
    if not os.path.isdir(METADATA_DIR):
        return []
    tags: list[str] = []
    seen: set[str] = set()
    for entry in sorted(os.listdir(METADATA_DIR)):
        meta = read_build_metadata(entry)
        if meta is None:
            continue
        tag = meta.get("tag", entry)
        if tag not in seen:
            seen.add(tag)
            tags.append(tag)
    return tags
