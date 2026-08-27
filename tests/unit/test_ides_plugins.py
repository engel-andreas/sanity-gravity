"""Unit tests for the ``ides`` plugin kind (vscodium, vscode).

IDEs are the categorical counterpart of agents: they install on top of
the desktop (same build layer, same slot in the dimension tag) but are
indexed under ``plugins/ides/`` with ``kind = "ides"``. These tests
cover manifest validation, registry discovery (via the dedicated ides
bucket), agent-slot resolution through :meth:`get_layer`, and the
capability / tier enumeration. No Docker is involved -- the
container-side install is a plain apt/curl step guarded by the pinned
version + SHA256 checksums in each Dockerfile.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from sanity_gravity.domain.capability import (  # noqa: E402
    CapabilityConflictError,
    solve,
)
from sanity_gravity.domain.tags import Tag  # noqa: E402
from sanity_gravity.plugins.registry import (  # noqa: E402
    PluginRegistry,
    default_registry,
    reset_default_registry,
)

PLUGINS_DIR = _REPO_ROOT / "plugins"

# A GUI IDE pairs with every GUI desktop/connector combination that
# itself satisfies the display rule: xfce, cinnamon, lxqt or openbox
# x {kasm, ssh, vnc}.
def ide_variants(slug: str) -> list[Tag]:
    """A GUI IDE pairs with every GUI desktop/connector combination that
    itself satisfies the display rule: xfce, cinnamon, lxqt or openbox
    x {kasm, ssh, vnc}."""
    return [
        Tag(slug, "xfce", "kasm"),
        Tag(slug, "xfce", "ssh"),
        Tag(slug, "xfce", "vnc"),
        Tag(slug, "cinnamon", "kasm"),
        Tag(slug, "cinnamon", "ssh"),
        Tag(slug, "cinnamon", "vnc"),
        Tag(slug, "lxqt", "kasm"),
        Tag(slug, "lxqt", "ssh"),
        Tag(slug, "lxqt", "vnc"),
        Tag(slug, "openbox", "kasm"),
        Tag(slug, "openbox", "ssh"),
        Tag(slug, "openbox", "vnc"),
    ]


IDE_VALID_TAGS = [
    tag for slug in ("codium", "vscode") for tag in ide_variants(slug)
]


@pytest.fixture(scope="module")
def reg() -> PluginRegistry:
    """Cold-load the builtin registry from the on-disk plugin tree."""
    reset_default_registry()
    return default_registry(PLUGINS_DIR)


# -- discovery ----------------------------------------------------------


@pytest.mark.parametrize("slug", ["codium", "vscode"])
def test_ide_is_discovered_in_ides_bucket(slug, reg):
    """ides plugins live under ``plugins/ides/``, not ``plugins/agents/``."""
    assert slug in reg.ides
    assert slug not in reg.agents


@pytest.mark.parametrize("slug", ["codium", "vscode"])
def test_ides_are_agent_slot_layers(slug, reg):
    """get_layer / layer_slugs expose IDEs where tags address the slot."""
    m = reg.get_layer(slug)
    assert m.slug == slug
    assert slug in reg.layer_slugs()


@pytest.mark.parametrize("slug", ["codium", "vscode"])
def test_ide_manifest_identity(slug, reg):
    m = reg.ides[slug]
    assert m.kind == "ides"
    assert m.api_version == "1"
    assert m.tier == "official"
    assert m.dockerfile == "Dockerfile"


def test_vscodium_manifest_name(reg):
    assert reg.ides["codium"].slug == "codium"
    assert reg.ides["codium"].name == "vscodium"


def test_vscode_manifest_name(reg):
    assert reg.ides["vscode"].slug == "vscode"
    assert reg.ides["vscode"].name == "vscode"


# -- capabilities -------------------------------------------------------


@pytest.mark.parametrize("slug", ["codium", "vscode"])
def test_ide_requires_display(slug, reg):
    """Both IDEs are GUI apps: they need a display and provide nothing."""
    m = reg.ides[slug]
    assert m.provides == ()
    assert m.requires == ("display",)


@pytest.mark.parametrize("slug", ["codium", "vscode"])
def test_ide_injects_no_host_env(slug, reg):
    """The sandbox must not auto-leak host secrets: IDEs declare no env."""
    assert reg.ides[slug].environment == ()


# -- tier ---------------------------------------------------------------


@pytest.mark.parametrize("slug", ["codium", "vscode"])
def test_ide_enters_the_official_matrix(slug):
    """All twelve {slug}-* tags must reach OFFICIAL_TAGS (the `list --json`
    source CI enumerates its matrices from)."""
    from sanity_gravity.cli.registry import OFFICIAL_TAGS, tag_tier

    ide_tags = [t for t in OFFICIAL_TAGS if t.startswith(f"{slug}-")]
    assert len(ide_tags) == 12
    for t in ide_tags:
        assert tag_tier(t) == "official"


# -- capability solving -------------------------------------------------


@pytest.mark.parametrize("tag", IDE_VALID_TAGS, ids=lambda t: str(t))
def test_ide_valid_tags_pass(tag, reg):
    assert solve(tag, reg) == tag


def test_ide_appears_in_valid_tags(reg):
    assert set(IDE_VALID_TAGS).issubset(set(reg.valid_tags()))


@pytest.mark.parametrize(
    "tag", [Tag("codium", "none", "kasm"), Tag("vscode", "none", "vnc")]
)
def test_ide_headless_tags_fail(tag, reg):
    """The desktop apps cannot run headless: every none-* combo fails on
    the missing display."""
    with pytest.raises(CapabilityConflictError) as excinfo:
        solve(tag, reg)
    assert excinfo.value.missing == frozenset({"display"})