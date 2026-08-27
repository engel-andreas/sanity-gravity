# Default is unused; always overridden by --build-arg. Set to a
# display-bearing intermediate (the ag plugin uses the same default)
# so a direct `docker build` of this plugin still produces a runnable
# desktop layer.
ARG BASE_IMAGE=sanity-gravity:_base-xfce
FROM ${BASE_IMAGE}

# VSCodium + OpenCode CLI Agent Layer
# Installs VSCodium (VSCodium/vscodium) from the pinned GitHub release
# .deb (amd64 + arm64) and the OpenCode CLI via the official installer
# in a single layer, so both land in one RUN. The .deb is installed via
# apt (not dpkg -i) so its Electron Depends (libgtk-3-0, libnss3,
# libsecret-1-0, libasound2, ...) resolve from the base repos. The ALSA
# lib is pulled explicitly (same rationale as the od plugin): Electron
# hard-requires libasound.so.2 at launch, and the package name is
# distro-specific - Ubuntu 24.04 (noble) renamed it to libasound2t64,
# Debian 12 (bookworm) still ships libasound2.
#
# OpenCode uses the same install contract as the oc plugin: the
# installer hardcodes $HOME/.opencode/bin, so the binary is copied onto
# the global PATH and the staging dir removed. --no-modify-path skips
# shell rc edits. `test -f` fails the build loudly if upstream moves the
# target again.
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
    curl -fsSL https://opencode.ai/install | bash -s -- --no-modify-path && \
    test -f /root/.opencode/bin/opencode && \
    cp /root/.opencode/bin/opencode /usr/local/bin/opencode && \
    chmod 755 /usr/local/bin/opencode && \
    rm -rf /root/.opencode && \
    test -x /usr/local/bin/opencode && \
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