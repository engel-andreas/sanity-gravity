# Modular Tag System

Every Sanity-Gravity image is described by a **4-dimensional tag**:
`{base-image-}agent-desktop-connector`. The base image is the optional
first segment; the default (`ubuntu`) is elided, so plain
`ag-xfce-kasm` is the default-base form and `debian-ag-xfce-kasm` is the
Debian variant of the same stack.

## Dimensions

### Base Images

The OS layer underneath everything else.

| Slug | Name | Notes |
|:-----|:-----|:------|
| `ubuntu` | Ubuntu 24.04 | **Default** — elided from tags; pinned `ubuntu:24.04` via `plugins/base-images/ubuntu/Dockerfile` |
| `debian` | Debian 12 (bookworm) | Pinned `debian:12` via `plugins/base-images/debian/` |

### Agents

The AI tool installed in the sandbox.

| Slug | Name | Requires GUI | What's Installed |
|:-----|:-----|:-------------|:-----------------|
| `ag` | Antigravity IDE | Yes | Antigravity IDE + Google Chrome |
| `agy` | Antigravity CLI | No | Antigravity CLI (official installer) -- Gemini CLI's official successor |
| `cc` | Claude Code | No | Claude Code CLI (official installer) |
| `cx` | OpenAI Codex CLI | No | Codex CLI (static musl `codex` binary, official installer) |
| `gc` | Gemini CLI **(deprecated)** | No | Node.js 22 + `@google/gemini-cli` |
| `oc` | OpenCode | No | OpenCode CLI (single Bun-compiled `opencode` binary, official installer) |
| `od` | OpenCode Desktop | Yes | OpenCode Desktop (Electron GUI app, official .deb for amd64/arm64) |

> **`gc` is deprecated.** Google shut down the Gemini CLI free tier on
> 2026-06-18; it now requires a paid Gemini API key / Code Assist license.
> The plugin and its images are kept for those users, but new users should
> prefer **`agy`** (Antigravity CLI), Google's official replacement.

### Desktops

Whether a graphical desktop environment is included.

| Slug | Name | Has GUI |
|:-----|:-----|:--------|
| `xfce` | XFCE | Yes — full XFCE4 desktop with window manager |
| `cinnamon` | Cinnamon | Yes — Cinnamon desktop environment |
| `lxqt` | LXQt | Yes — LXQt desktop environment |
| `openbox` | Openbox | Yes — lightweight X11 window manager (no panel) |
| `none` | Headless | No — `DISPLAY` is unset, minimal footprint |

### Connectors

How you connect to the running container.

| Slug | Name | Requires GUI | Ports |
|:-----|:-----|:-------------|:------|
| `kasm` | KasmVNC | Yes | `8444` (HTTPS) |
| `vnc` | TigerVNC + noVNC | Yes | `5901` (VNC), `6901` (noVNC HTTP) |
| `ssh` | SSH only | No | `22` (mapped to host `2222`) |

## Constraint Rules

Not all combinations are valid. Two rules are enforced:

1. **GUI connectors require a GUI desktop**: `kasm` and `vnc` can only pair with `xfce`, `cinnamon`, `lxqt`, or `openbox` (not `none`).
2. **GUI agents require a GUI desktop**: `ag` (Antigravity IDE) and `od` (OpenCode Desktop) can only pair with `xfce`, `cinnamon`, `lxqt`, or `openbox` (not `none`).

These rules are enforced by `sanity-cli` at build time and run time.

## All Valid Tags (178)

Listed in the same order as `./sanity-cli list` (default base first,
agents sorted alphabetically). The table shows the **default (ubuntu)**
tags; every tag has a `debian-`-prefixed twin with the same stack
(e.g. `debian-ag-xfce-kasm`). `./sanity-cli list` prints all 178.

| Tag | Agent | Desktop | Connector | Use Case |
|:----|:------|:--------|:----------|:---------|
| **`ag-cinnamon-kasm`** | Antigravity | Cinnamon | KasmVNC | Full IDE sandbox via browser |
| `ag-cinnamon-ssh` | Antigravity | Cinnamon | SSH | Full IDE sandbox, SSH-only access |
| `ag-cinnamon-vnc` | Antigravity | Cinnamon | TigerVNC | Full IDE sandbox via legacy VNC client |
| `ag-lxqt-kasm` | Antigravity | LXQt | KasmVNC | Full IDE sandbox via browser |
| `ag-lxqt-ssh` | Antigravity | LXQt | SSH | Full IDE sandbox, SSH-only access |
| `ag-lxqt-vnc` | Antigravity | LXQt | TigerVNC | Full IDE sandbox via legacy VNC client |
| `ag-openbox-kasm` | Antigravity | Openbox | KasmVNC | Full IDE sandbox via browser |
| `ag-openbox-ssh` | Antigravity | Openbox | SSH | Full IDE sandbox, SSH-only access |
| `ag-openbox-vnc` | Antigravity | Openbox | TigerVNC | Full IDE sandbox via legacy VNC client |
| **`ag-xfce-kasm`** | Antigravity | XFCE | KasmVNC | Full IDE sandbox via browser **(default)** |
| `ag-xfce-ssh` | Antigravity | XFCE | SSH | Full IDE sandbox, SSH-only access |
| `ag-xfce-vnc` | Antigravity | XFCE | TigerVNC | Full IDE sandbox via legacy VNC client |
| `agy-cinnamon-kasm` | Antigravity CLI | Cinnamon | KasmVNC | Antigravity CLI with Cinnamon desktop |
| `agy-cinnamon-ssh` | Antigravity CLI | Cinnamon | SSH | Antigravity CLI with GUI, SSH-only access |
| `agy-cinnamon-vnc` | Antigravity CLI | Cinnamon | TigerVNC | Antigravity CLI with legacy VNC |
| `agy-lxqt-kasm` | Antigravity CLI | LXQt | KasmVNC | Antigravity CLI with LXQt desktop |
| `agy-lxqt-ssh` | Antigravity CLI | LXQt | SSH | Antigravity CLI with GUI, SSH-only access |
| `agy-lxqt-vnc` | Antigravity CLI | LXQt | TigerVNC | Antigravity CLI with legacy VNC |
| `agy-openbox-kasm` | Antigravity CLI | Openbox | KasmVNC | Antigravity CLI with Openbox desktop |
| `agy-openbox-ssh` | Antigravity CLI | Openbox | SSH | Antigravity CLI with GUI, SSH-only access |
| `agy-openbox-vnc` | Antigravity CLI | Openbox | TigerVNC | Antigravity CLI with legacy VNC |
| `agy-none-ssh` | Antigravity CLI | Headless | SSH | Lightweight Antigravity CLI terminal |
| `agy-xfce-kasm` | Antigravity CLI | XFCE | KasmVNC | Antigravity CLI with browser desktop |
| `agy-xfce-ssh` | Antigravity CLI | XFCE | SSH | Antigravity CLI with GUI, SSH-only access |
| `agy-xfce-vnc` | Antigravity CLI | XFCE | TigerVNC | Antigravity CLI with legacy VNC |
| `cc-cinnamon-kasm` | Claude Code | Cinnamon | KasmVNC | Claude Code with Cinnamon desktop |
| `cc-cinnamon-ssh` | Claude Code | Cinnamon | SSH | Claude Code with GUI, SSH-only access |
| `cc-cinnamon-vnc` | Claude Code | Cinnamon | TigerVNC | Claude Code with legacy VNC |
| `cc-lxqt-kasm` | Claude Code | LXQt | KasmVNC | Claude Code with LXQt desktop |
| `cc-lxqt-ssh` | Claude Code | LXQt | SSH | Claude Code with GUI, SSH-only access |
| `cc-lxqt-vnc` | Claude Code | LXQt | TigerVNC | Claude Code with legacy VNC |
| `cc-openbox-kasm` | Claude Code | Openbox | KasmVNC | Claude Code with Openbox desktop |
| `cc-openbox-ssh` | Claude Code | Openbox | SSH | Claude Code with GUI, SSH-only access |
| `cc-openbox-vnc` | Claude Code | Openbox | TigerVNC | Claude Code with legacy VNC |
| `cc-none-ssh` | Claude Code | Headless | SSH | Lightweight Claude Code terminal |
| `cc-xfce-kasm` | Claude Code | XFCE | KasmVNC | Claude Code with browser desktop |
| `cc-xfce-ssh` | Claude Code | XFCE | SSH | Claude Code with GUI, SSH-only access |
| `cc-xfce-vnc` | Claude Code | XFCE | TigerVNC | Claude Code with legacy VNC |
| `cx-cinnamon-kasm` | OpenAI Codex | Cinnamon | KasmVNC | Codex with Cinnamon desktop |
| `cx-cinnamon-ssh` | OpenAI Codex | Cinnamon | SSH | Codex with GUI, SSH-only access |
| `cx-cinnamon-vnc` | OpenAI Codex | Cinnamon | TigerVNC | Codex with legacy VNC |
| `cx-lxqt-kasm` | OpenAI Codex | LXQt | KasmVNC | Codex with LXQt desktop |
| `cx-lxqt-ssh` | OpenAI Codex | LXQt | SSH | Codex with GUI, SSH-only access |
| `cx-lxqt-vnc` | OpenAI Codex | LXQt | TigerVNC | Codex with legacy VNC |
| `cx-openbox-kasm` | OpenAI Codex | Openbox | KasmVNC | Codex with Openbox desktop |
| `cx-openbox-ssh` | OpenAI Codex | Openbox | SSH | Codex with GUI, SSH-only access |
| `cx-openbox-vnc` | OpenAI Codex | Openbox | TigerVNC | Codex with legacy VNC |
| `cx-none-ssh` | OpenAI Codex | Headless | SSH | Lightweight Codex terminal |
| `cx-xfce-kasm` | OpenAI Codex | XFCE | KasmVNC | Codex with browser desktop |
| `cx-xfce-ssh` | OpenAI Codex | XFCE | SSH | Codex with GUI, SSH-only access |
| `cx-xfce-vnc` | OpenAI Codex | XFCE | TigerVNC | Codex with legacy VNC |
| `gc-cinnamon-kasm` | Gemini CLI | Cinnamon | KasmVNC | Gemini with Cinnamon desktop |
| `gc-cinnamon-ssh` | Gemini CLI | Cinnamon | SSH | Gemini with GUI, SSH-only access |
| `gc-cinnamon-vnc` | Gemini CLI | Cinnamon | TigerVNC | Gemini with legacy VNC |
| `gc-lxqt-kasm` | Gemini CLI | LXQt | KasmVNC | Gemini with LXQt desktop |
| `gc-lxqt-ssh` | Gemini CLI | LXQt | SSH | Gemini with GUI, SSH-only access |
| `gc-lxqt-vnc` | Gemini CLI | LXQt | TigerVNC | Gemini with legacy VNC |
| `gc-openbox-kasm` | Gemini CLI | Openbox | KasmVNC | Gemini with Openbox desktop |
| `gc-openbox-ssh` | Gemini CLI | Openbox | SSH | Gemini with GUI, SSH-only access |
| `gc-openbox-vnc` | Gemini CLI | Openbox | TigerVNC | Gemini with legacy VNC |
| `gc-none-ssh` | Gemini CLI | Headless | SSH | Lightweight Gemini terminal |
| `gc-xfce-kasm` | Gemini CLI | XFCE | KasmVNC | Gemini with browser desktop |
| `gc-xfce-ssh` | Gemini CLI | XFCE | SSH | Gemini with GUI, SSH-only access |
| `gc-xfce-vnc` | Gemini CLI | XFCE | TigerVNC | Gemini with legacy VNC |
| `oc-cinnamon-kasm` | OpenCode | Cinnamon | KasmVNC | OpenCode with Cinnamon desktop |
| `oc-cinnamon-ssh` | OpenCode | Cinnamon | SSH | OpenCode with GUI, SSH-only access |
| `oc-cinnamon-vnc` | OpenCode | Cinnamon | TigerVNC | OpenCode with legacy VNC |
| `oc-lxqt-kasm` | OpenCode | LXQt | KasmVNC | OpenCode with LXQt desktop |
| `oc-lxqt-ssh` | OpenCode | LXQt | SSH | OpenCode with GUI, SSH-only access |
| `oc-lxqt-vnc` | OpenCode | LXQt | TigerVNC | OpenCode with legacy VNC |
| `oc-openbox-kasm` | OpenCode | Openbox | KasmVNC | OpenCode with Openbox desktop |
| `oc-openbox-ssh` | OpenCode | Openbox | SSH | OpenCode with GUI, SSH-only access |
| `oc-openbox-vnc` | OpenCode | Openbox | TigerVNC | OpenCode with legacy VNC |
| `oc-none-ssh` | OpenCode | Headless | SSH | Lightweight OpenCode terminal |
| `oc-xfce-kasm` | OpenCode | XFCE | KasmVNC | OpenCode with browser desktop |
| `oc-xfce-ssh` | OpenCode | XFCE | SSH | OpenCode with GUI, SSH-only access |
| `oc-xfce-vnc` | OpenCode | XFCE | TigerVNC | OpenCode with legacy VNC |
| `od-cinnamon-kasm` | OpenCode Desktop | Cinnamon | KasmVNC | OpenCode Desktop with Cinnamon desktop |
| `od-cinnamon-ssh` | OpenCode Desktop | Cinnamon | SSH | OpenCode Desktop with GUI, SSH-only access |
| `od-cinnamon-vnc` | OpenCode Desktop | Cinnamon | TigerVNC | OpenCode Desktop with legacy VNC |
| `od-lxqt-kasm` | OpenCode Desktop | LXQt | KasmVNC | OpenCode Desktop with LXQt desktop |
| `od-lxqt-ssh` | OpenCode Desktop | LXQt | SSH | OpenCode Desktop with GUI, SSH-only access |
| `od-lxqt-vnc` | OpenCode Desktop | LXQt | TigerVNC | OpenCode Desktop with legacy VNC |
| `od-openbox-kasm` | OpenCode Desktop | Openbox | KasmVNC | OpenCode Desktop with Openbox desktop |
| `od-openbox-ssh` | OpenCode Desktop | Openbox | SSH | OpenCode Desktop with GUI, SSH-only access |
| `od-openbox-vnc` | OpenCode Desktop | Openbox | TigerVNC | OpenCode Desktop with legacy VNC |
| `od-xfce-kasm` | OpenCode Desktop | XFCE | KasmVNC | OpenCode Desktop with browser desktop |
| `od-xfce-ssh` | OpenCode Desktop | XFCE | SSH | OpenCode Desktop with GUI, SSH-only access |
| `od-xfce-vnc` | OpenCode Desktop | XFCE | TigerVNC | OpenCode Desktop with legacy VNC |

## Discovery Commands

```bash
# List all valid tags with dimension info
./sanity-cli list

# Output as JSON array (for CI matrix)
./sanity-cli list --json
```
