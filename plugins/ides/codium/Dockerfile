# Default is unused; always overridden by --build-arg. Set to a
# display-bearing intermediate (the ag plugin uses the same default)
# so a direct `docker build` of this plugin still produces a runnable
# desktop layer.
ARG BASE_IMAGE=sanity-gravity:_base-xfce
FROM ${BASE_IMAGE}

# Vendored OpenCode extension (Open VSX) for offline, reproducible
# installs: upstream sst-dev/opencode-v2 v0.1.1, vsix sha256
# d756bc25a8ac84dcb2e979137a1eacdfa79f76dd6d48d61c94e764825c7cc77d
# (https://open-vsx.org/api/sst-dev/opencode-v2/0.1.1/file/...).
COPY extensions/ /tmp/codium-ext/

# VSCodium IDE Layer
# Installs VSCodium (VSCodium/vscodium) from the pinned GitHub release
# .deb (amd64 + arm64) in a single layer. The .deb is installed via
# apt (not dpkg -i) so its Electron Depends (libgtk-3-0, libnss3,
# libsecret-1-0, libasound2, ...) resolve from the base repos. The ALSA
# lib is pulled explicitly (same rationale as the od plugin): Electron
# hard-requires libasound.so.2 at launch, and the package name is
# distro-specific - Ubuntu 24.04 (noble) renamed it to libasound2t64,
# Debian 12 (bookworm) still ships libasound2.
#
# No agent CLI is bundled here: the IDE layer only provides the editor.
# OpenCode (or any other agent) comes from its own agent layer composed
# alongside this plugin.
#
# The OpenCode extension (sst-dev.opencode-v2) is installed from the
# vendored .vsix via the headless `codium --install-extension` path, so
# both the editor and its bundled extension land in one RUN. The .vsix
# is submitted to `sha256sum` (same contract as the pinned .deb above).
# The extension only renders its UI; the opencode CLI is still required
# at runtime and is provided by the oc agent layer, not the IDE.
#
# Extensions are written by the CLI into the root HOME
# (/root/.vscode-oss/extensions) because the image builds as root, so
# the entrypoint hook in rootfs/ seeds them into the home of the user
# created at boot. Without that copy the sandbox user would see a bare
# editor with no extensions.
#
# The VSCodium chrome-sandbox SUID bit is only set by postinst when user
# namespaces are unavailable (container-safe), so the .desktop launchers
# get the Chromium sandbox opt-out appended - same contract as the od and
# ag agent layers: the app runs as the unprivileged sandbox user.
ARG VSCODIUM_VERSION=1.126.04524
RUN arch="$(dpkg --print-architecture)" && \
    case "$arch" in \
        amd64) asset="codium_${VSCODIUM_VERSION}_amd64.deb"; \
               sha="b4edf5dd785826fb9539918e715671580395441ee15f090413fd6f89e1c617c7" ;; \
        arm64) asset="codium_${VSCODIUM_VERSION}_arm64.deb"; \
               sha="a019ba332b3ffb68dc58afc633ad686ce2074e81af08b6382eed698c5631ee5d" ;; \
        *) echo "unsupported architecture: $arch" >&2; exit 1 ;; \
    esac && \
    curl -fsSL "https://github.com/VSCodium/vscodium/releases/download/${VSCODIUM_VERSION}/${asset}" \
        -o /tmp/codium.deb && \
    echo "${sha}  /tmp/codium.deb" | sha256sum -c - && \
    apt-get update && \
    if grep -q "ID=debian" /etc/os-release; then ALSA_PKG="libasound2"; else ALSA_PKG="libasound2t64"; fi && \
    apt-get install -y --no-install-recommends "${ALSA_PKG}" /tmp/codium.deb && \
    rm /tmp/codium.deb && \
    echo "d756bc25a8ac84dcb2e979137a1eacdfa79f76dd6d48d61c94e764825c7cc77d  /tmp/codium-ext/sst-dev.opencode-v2-0.1.1.vsix" | sha256sum -c - && \
    codium --install-extension /tmp/codium-ext/sst-dev.opencode-v2-0.1.1.vsix && \
    rm -rf /tmp/codium-ext && \
    for f in /usr/share/applications/codium.desktop \
             /usr/share/applications/codium-url-handler.desktop; do \
        if [ -f "$f" ]; then \
            sed -i 's|^Exec=.*|Exec=/usr/bin/codium --no-sandbox --disable-dev-shm-usage %F|' "$f"; \
        fi; \
    done && \
    apt-get autoremove -y && \
    rm -rf /usr/share/doc/* /usr/share/info/* /usr/share/lintian/* /usr/share/man/* \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY rootfs/ /