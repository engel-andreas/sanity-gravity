# Default is unused; always overridden by --build-arg. Set to suppress Docker warning.
ARG BASE_IMAGE=ubuntu:24.04
FROM ${BASE_IMAGE}

# OpenCode Desktop Agent Layer
# Installs the OpenCode Desktop app (Electron GUI) from the official GitHub
# release .deb. Only the desktop variant ships as .deb (amd64 + arm64); the
# terminal CLI lives in the sibling "oc" plugin. The version is pinned for
# deterministic builds (same rationale as the pinned Codex tarball); bump the
# ARG and both SHA256 sums together.
#
# The .deb is installed via apt (not dpkg -i) so its Depends (libgtk-3-0,
# libnss3, libsecret-1-0, ...) resolve from the base repos. The ALSA lib
# is pulled explicitly: Electron hard-requires libasound.so.2 at launch,
# but the opencode-desktop .deb does not declare it as a Depends, so
# without this the app aborts with "error while loading shared libraries:
# libasound.so.2". The package name is distro-specific: Ubuntu 24.04
# (noble) and Debian 13 (trixie) ship libasound2t64, while Debian 12
# (bookworm) still ships libasound2. The build probes the local package
# index to pick the right name. The
# postinst is
# container-safe: the chrome-sandbox SUID bit is only set when user
# namespaces are unavailable, and the AppArmor profile install is skipped
# when apparmor_parser is absent. It installs the app under /opt/OpenCode as
# binary "ai.opencode.desktop" plus the /usr/bin symlink via
# update-alternatives; there is deliberately no `opencode` command in PATH
# (unlike the oc CLI plugin).
#
# Both .desktop launchers get the Chromium sandbox opt-out appended so the
# app starts as the unprivileged sandbox user from the desktop menu
# (KasmVNC / TigerVNC) -- same contract as the Antigravity agent layer.
# --no-sandbox is required because the app runs under a non-root uid while
# its chrome-sandbox binary is not setuid.
#
# Auto-update is not explicitly disabled in the image: the app is root-owned
# under /opt, so a self-update could never succeed for the sandbox user and
# would only add startup noise. The entrypoint hook in rootfs/ seeds the
# documented config-file opt-out (~/.config/opencode/opencode.json) into the
# home of the user created at boot, exactly like the oc plugin.
ARG OPENCODE_DESKTOP_VERSION=1.18.25
RUN arch="$(dpkg --print-architecture)" && \
    case "$arch" in \
        amd64) asset="opencode-desktop-linux-amd64.deb"; \
               sha="319198179a7f356b962b52a6e1829bdad28683ae549495eb5d84a6a6e2d8212b" ;; \
        arm64) asset="opencode-desktop-linux-arm64.deb"; \
               sha="cddcdad352d78879e34fd936621dc8fd2c9525af95bb96fe53c6043d32c060d6" ;; \
        *) echo "unsupported architecture: $arch" >&2; exit 1 ;; \
    esac && \
    curl -fsSL "https://github.com/anomalyco/opencode/releases/download/v${OPENCODE_DESKTOP_VERSION}/${asset}" \
        -o /tmp/opencode.deb && \
    echo "${sha}  /tmp/opencode.deb" | sha256sum -c - && \
    apt-get update && \
    if apt-cache show libasound2 >/dev/null 2>&1; then ALSA_PKG="libasound2"; else ALSA_PKG="libasound2t64"; fi && \
    apt-get install -y --no-install-recommends "${ALSA_PKG}" /tmp/opencode.deb && \
    rm /tmp/opencode.deb && \
    apt-get autoremove -y && \
    rm -rf /usr/share/doc/* /usr/share/info/* /usr/share/lintian/* /usr/share/man/* \
    && apt-get clean && rm -rf /var/lib/apt/lists/* && \
    for f in /usr/share/applications/opencode-desktop.desktop \
             /usr/share/applications/ai.opencode.desktop.desktop; do \
        if [ -f "$f" ]; then \
            sed -i 's|^Exec=.*|Exec=/opt/OpenCode/ai.opencode.desktop --no-sandbox --disable-dev-shm-usage %U|' "$f"; \
        fi; \
    done && \
    test -x /opt/OpenCode/ai.opencode.desktop

COPY rootfs/ /
