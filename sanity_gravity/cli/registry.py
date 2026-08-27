"""Lazy plugin registry + legacy dimension projections + tag parser.

The legacy ``AGENTS`` / ``CONNECTORS`` / ``DESKTOPS`` dicts are derived
from the manifest-driven registry and exposed here for back-compat with
tests and verbs that grew up reading them. ``parse_tag`` performs
constraint validation via the capability solver, mapping the technical
"missing capability" error back to the user-friendly
"requires a GUI desktop" phrasing.
"""
from __future__ import annotations

import os
from collections.abc import Collection

from sanity_gravity.domain.capability import CapabilityConflictError
from sanity_gravity.domain.capability import solve as _capability_solve
from sanity_gravity.domain.tags import DEFAULT_BASE_IMAGE, Tag
from sanity_gravity.plugins.registry import default_registry as _default_registry


PLUGINS_DIR = "plugins"
DEFAULT_TAG = "ag-xfce-kasm"
AGENT_SEPARATOR = "_"
PROVIDER_SEPARATOR = "_"


def _repo_root() -> str:
    """Return the repository root (3 dirs up from this file).

    This file lives at ``<repo>/sanity_gravity/cli/registry.py``.
    """
    return os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )


def get_registry():
    """Lazy accessor: load manifests from ``plugins/`` once per process."""
    return _default_registry(os.path.join(_repo_root(), PLUGINS_DIR))


def _legacy_dim_dicts(reg):
    """Project the registry into the legacy ``{slug: {name, ...}}`` shape."""
    bases: dict[str, dict] = {}
    for slug, m in reg.base_images.items():
        bases[slug] = {
            "name": m.name,
            "tier": m.tier,
        }
    agents: dict[str, dict] = {}
    for slug, m in reg.agents.items():
        agents[slug] = {
            "name": m.name,
            "requires_gui": "display" in m.requires,
            "tier": m.tier,
        }
    ides: dict[str, dict] = {}
    for slug, m in reg.ides.items():
        ides[slug] = {
            "name": m.name,
            "requires_gui": "display" in m.requires,
            "tier": m.tier,
        }
    connectors: dict[str, dict] = {}
    for slug, m in reg.connectors.items():
        connectors[slug] = {
            "name": m.name,
            "requires_gui": "display" in m.requires,
            "tier": m.tier,
        }
    desktops: dict[str, dict] = {}
    for slug, m in reg.desktops.items():
        desktops[slug] = {
            "name": m.name,
            "has_gui": "display" in m.provides,
            "tier": m.tier,
        }
    providers: dict[str, dict] = {}
    for slug, m in reg.providers.items():
        providers[slug] = {
            "name": m.name,
            "host_ports": {p.label: p.default for p in m.ports},
            "tier": m.tier,
        }
    return bases, agents, ides, connectors, desktops, providers


def parse_tag(tag):
    """Parse a dimension tag into ``(base_image, agent, desktop, connector)``.

    Accepts both ``agent-desktop-connector`` (default base) and
    ``base_image-agent-desktop-connector`` forms. The default base is
    always valid even before a matching ``base-image`` plugin exists;
    non-default base slugs must be registered.

    Validation goes through the manifest-driven registry: unknown slugs
    raise ``ValueError`` with the legacy ``Unknown <kind>`` message, and
    capability conflicts raise ``ValueError`` with a 'requires a GUI
    desktop' phrasing kept for legacy tests / users (the underlying
    solver is generic and supports arbitrary capabilities).
    """
    parts = tag.split("-")
    if len(parts) == 4:
        base_image, agent, desktop, connector = parts
    elif len(parts) == 3:
        base_image, agent, desktop, connector = DEFAULT_BASE_IMAGE, *parts
    else:
        raise ValueError(
            f"Invalid tag format '{tag}'. Expected "
            "{base_image-}agent-desktop-connector "
            "(e.g. ag-xfce-kasm or debian-ag-xfce-kasm)"
        )
    reg = get_registry()
    if base_image != DEFAULT_BASE_IMAGE and base_image not in reg.base_images:
        raise ValueError(
            f"Unknown base image '{base_image}'. "
            f"Valid: {', '.join(reg.base_images.keys())}"
        )
    if agent not in reg.layer_slugs():
        raise ValueError(
            f"Unknown agent '{agent}'. "
            f"Valid: {', '.join(reg.layer_slugs())}"
        )
    if desktop not in reg.desktops:
        raise ValueError(
            f"Unknown desktop '{desktop}'. Valid: {', '.join(reg.desktops.keys())}"
        )
    if connector not in reg.connectors:
        raise ValueError(
            f"Unknown connector '{connector}'. "
            f"Valid: {', '.join(reg.connectors.keys())}"
        )

    parsed = Tag(agent=agent, desktop=desktop, connector=connector, base_image=base_image)
    try:
        _capability_solve(parsed, reg)
    except CapabilityConflictError as exc:
        if "display" in exc.missing:
            connector_m = reg.connectors[connector]
            agent_m = reg.get_layer(agent)
            if "display" in connector_m.requires:
                raise ValueError(
                    f"Connector '{connector}' requires a GUI desktop, "
                    f"but '{desktop}' is headless"
                ) from exc
            if "display" in agent_m.requires:
                raise ValueError(
                    f"Agent '{agent}' requires a GUI desktop, "
                    f"but '{desktop}' is headless"
                ) from exc
        raise ValueError(str(exc)) from exc
    return base_image, agent, desktop, connector


def construct_tag(
    base_image: str | None = None,
    agents: list[str] | None = None,
    desktop: str | None = None,
    connector: str | None = None,
    providers: list[str] | None = None,
) -> str:
    """Build a tag string from explicit component lists.

    Naming convention::

        {base-}agent1[-agent2]-desktop-connector[-provider1[-provider2]]

    - ``base_image`` is elided when it equals ``DEFAULT_BASE_IMAGE``.
    - Multiple agents are joined with ``AGENT_SEPARATOR`` (``_``).
    - Multiple providers are joined with ``PROVIDER_SEPARATOR`` (``_``).
    - Components are validated against the registry.

    Examples::

        construct_tag(agents=["ag"], desktop="xfce", connector="kasm")
        # → "ag-xfce-kasm"

        construct_tag(agents=["ag", "cc"], desktop="xfce", connector="kasm")
        # → "ag_cc-xfce-kasm"

        construct_tag(agents=["ag"], desktop="xfce", connector="kasm",
                       providers=["ollama"])
        # → "ag-xfce-kasm-ollama"

        construct_tag(base_image="debian", agents=["ag"], desktop="xfce",
                       connector="kasm", providers=["ollama", "lm-studio"])
        # → "debian-ag-xfce-kasm-ollama_lmstudio"
    """
    if not agents or not desktop or not connector:
        raise ValueError("agents, desktop, and connector are required")
    if len(agents) < 1:
        raise ValueError("at least one agent is required")

    reg = get_registry()

    base = base_image or DEFAULT_BASE_IMAGE
    if base != DEFAULT_BASE_IMAGE and base not in reg.base_images:
        raise ValueError(
            f"Unknown base image '{base}'. "
            f"Valid: {', '.join(reg.base_images.keys())}"
        )
    for a in agents:
        if a not in reg.layer_slugs():
            raise ValueError(
                f"Unknown agent '{a}'. Valid: {', '.join(reg.layer_slugs())}"
            )
    if desktop not in reg.desktops:
        raise ValueError(
            f"Unknown desktop '{desktop}'. "
            f"Valid: {', '.join(reg.desktops.keys())}"
        )
    if connector not in reg.connectors:
        raise ValueError(
            f"Unknown connector '{connector}'. "
            f"Valid: {', '.join(reg.connectors.keys())}"
        )
    for p in (providers or []):
        if p not in reg.providers:
            raise ValueError(
                f"Unknown provider '{p}'. "
                f"Valid: {', '.join(reg.providers.keys())}"
            )

    parts: list[str] = []
    if base != DEFAULT_BASE_IMAGE:
        parts.append(base)
    parts.append(AGENT_SEPARATOR.join(agents))
    parts.append(desktop)
    parts.append(connector)
    if providers:
        parts.append(PROVIDER_SEPARATOR.join(providers))
    return "-".join(parts)


def parse_composite_tag(tag: str) -> dict[str, list[str]]:
    """Parse a composite tag into its component dimensions.

    Returns a dict with keys ``base_image``, ``agents``, ``desktop``,
    ``connector``, ``providers`` — each value is a list of slugs.

    This is the inverse of :func:`construct_tag` for tags built by the
    new explicit-flag system. Tags built by the legacy ``parse_tag``
    format (``{base-}agent-desktop-connector``) are also accepted —
    agents will be a single-element list.

    Raises ``ValueError`` if a dimension can't be identified (e.g. the
    tag contains parts that match neither providers nor the registry).
    """
    reg = get_registry()
    parts = tag.split("-")

    result: dict[str, list[str]] = {
        "base_image": [],
        "agents": [],
        "desktop": [],
        "connector": [],
        "providers": [],
    }

    if not parts:
        raise ValueError(f"Empty tag: {tag!r}")

    # Identify providers from the end (they're appended after connector)
    remaining = list(parts)
    providers: list[str] = []
    while remaining:
        candidate = remaining[-1]
        # Check if this is a compound provider slug (underscore-separated)
        provider_slugs = candidate.split(PROVIDER_SEPARATOR)
        if all(p in reg.providers for p in provider_slugs):
            providers = provider_slugs + providers
            remaining.pop()
        elif candidate in reg.providers:
            providers = [candidate] + providers
            remaining.pop()
        else:
            break
    result["providers"] = providers

    # The last part of remaining is the connector
    if not remaining:
        raise ValueError(f"Could not identify connector in tag: {tag!r}")
    connector = remaining.pop()
    result["connector"] = [connector]

    # Second-to-last is the desktop
    if not remaining:
        raise ValueError(f"Could not identify desktop in tag: {tag!r}")
    desktop = remaining.pop()
    result["desktop"] = [desktop]

    # First part might be a non-default base image
    if remaining and remaining[0] in reg.base_images and remaining[0] != DEFAULT_BASE_IMAGE:
        result["base_image"] = [remaining.pop(0)]

    # Everything remaining is agent(s), potentially underscore-separated
    if remaining:
        agent_str = remaining[0]
        agent_slugs = agent_str.split(AGENT_SEPARATOR)
        result["agents"] = agent_slugs

    # Validate all parts
    if result["base_image"] and result["base_image"][0] not in reg.base_images:
        raise ValueError(f"Unknown base image '{result['base_image'][0]}'")
    for a in result["agents"]:
        if a not in reg.layer_slugs():
            raise ValueError(f"Unknown agent '{a}'")
    if result["desktop"][0] not in reg.desktops:
        raise ValueError(f"Unknown desktop '{result['desktop'][0]}'")
    if result["connector"][0] not in reg.connectors:
        raise ValueError(f"Unknown connector '{result['connector'][0]}'")

    return result


def is_composite_tag(tag: str) -> bool:
    """Check if a tag uses the new composite format (multi-agent or providers)."""
    try:
        parts = parse_composite_tag(tag)
        return len(parts["agents"]) > 1 or len(parts["providers"]) > 0
    except ValueError:
        return False


def generate_valid_tags(tiers: Collection[str] | None = None) -> list[str]:
    """Return all tag combinations whose plugins satisfy capabilities.

    ``tiers`` optionally restricts the result to tags whose tier is in
    the given set (see :meth:`PluginRegistry.valid_tags`).
    """
    return [str(t) for t in get_registry().valid_tags(tiers=tiers)]


def tag_tier(tag: str) -> str:
    """Tier of a well-formed ``{base_image-}agent-desktop-connector`` string.

    See :meth:`PluginRegistry.tag_tier` - the most restrictive tier
    among the tag's plugins wins.
    """
    base_image, agent, desktop, connector = parse_tag(tag)
    return get_registry().tag_tier(
        Tag(agent=agent, desktop=desktop, connector=connector, base_image=base_image)
    )


def deprecation_warning(tag: str) -> str | None:
    """Warning text for a deprecated tag, or ``None`` for other tiers.

    Kept here (next to the tier data) so build/up print the same
    message; the verbs decide how to surface it.

    Composite tags (multi-agent or provider-based) are always treated
    as non-deprecated since they are user-defined at build time.
    """
    if is_composite_tag(tag):
        return None
    if tag_tier(tag) != "deprecated":
        return None
    return (
        f"Tag '{tag}' uses a deprecated plugin: it is excluded from CI "
        "and no longer published to GHCR. Local build/up keep working, "
        "but expect no further updates."
    )


# Legacy module-level views. Computed once at import time; they stay
# stable across a process because the manifest set is filesystem-bound.
BASES, AGENTS, IDES, CONNECTORS, DESKTOPS, PROVIDERS = _legacy_dim_dicts(get_registry())
VALID_TAGS = generate_valid_tags()
# The CI build/verify and release publish matrix: official tier only.
# Community/deprecated tags stay in VALID_TAGS (parse + lifecycle) but
# leave every CI enumeration (``list --json`` / ``build all``).
OFFICIAL_TAGS = generate_valid_tags(tiers=("official",))
