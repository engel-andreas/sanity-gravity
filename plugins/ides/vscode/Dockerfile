# Default is unused; always overridden by --build-arg. Set to a
# display-bearing intermediate (the codium / ag plugins use the same
# default) so a direct `docker build` of this plugin still produces a
# runnable desktop layer.
ARG BASE_IMAGE=sanity-gravity:_base-xfce
FROM ${BASE_IMAGE}

# VS Code IDE Layer
# Installs Microsoft VS Code (code) from the pinned packages.microsoft.com
# .deb (amd64 + arm64) in a single layer. The .deb is installed via
# apt (not dpkg -i) so its Electron Depends (libgtk-3-0, libnss3,
# libsecret-1-0, libasound2, ...) resolve from the base repos. The ALSA
# lib is pulled explicitly (same rationale as the od / codium plugins):
# Electron hard-requires libasound.so.2 at launch, and the package name
# is distro-specific - Ubuntu 24.04 (noble) and Debian 13 (trixie) ship
# libasound2t64, Debian 12 (bookworm) still ships libasound2. The build
# probes the local package index to pick the right name.
# The .deb is version-pinned; bump ARG VSCODE_VERSION / VSCODE_BUILD
# and both SHA256 sums together (the build-suffix is per-arch and
# differs from the version string).
#
# No agent CLI is bundled here: the IDE layer only provides the editor.
# OpenCode (or any other agent) comes from its own agent layer composed
# alongside this plugin.
#
# The VS Code chrome-sandbox SUID bit is only set by postinst when user
# namespaces are unavailable (container-safe), so the .desktop launchers
# get the Chromium sandbox opt-out appended - same contract as the od,
# ag, and codium layers: the app runs as the unprivileged sandbox user.
ARG VSCODE_VERSION=1.135.0
RUN arch="$(dpkg --print-architecture)" && \
    case "$arch" in \
        amd64) build="1787669172"; \
               sha="e8101720f0a48f8e6ae5a4112d10ffea5f13d298e7d0a7012b4e36eebc53022c" ;; \
        arm64) build="1787669187"; \
               sha="20f1717805ed723c8846e14df3280c6132a663ff71e32068aaa70f3e4c8b1ca4" ;; \
        *) echo "unsupported architecture: $arch" >&2; exit 1 ;; \
    esac && \
    curl -fsSL \
        "https://packages.microsoft.com/repos/code/pool/main/c/code/code_${VSCODE_VERSION}-${build}_${arch}.deb" \
        -o /tmp/vscode.deb && \
    echo "${sha}  /tmp/vscode.deb" | sha256sum -c - && \
    apt-get update && \
    if apt-cache show libasound2 >/dev/null 2>&1; then ALSA_PKG="libasound2"; else ALSA_PKG="libasound2t64"; fi && \
    apt-get install -y --no-install-recommends "${ALSA_PKG}" /tmp/vscode.deb && \
    rm /tmp/vscode.deb && \
    for f in /usr/share/applications/code.desktop \
             /usr/share/applications/code-url-handler.desktop; do \
        if [ -f "$f" ]; then \
            sed -i 's|^Exec=.*|Exec=/usr/bin/code --no-sandbox --disable-dev-shm-usage %F|' "$f"; \
        fi; \
    done && \
    apt-get autoremove -y && \
    rm -rf /usr/share/doc/* /usr/share/info/* /usr/share/lintian/* /usr/share/man/* \
    && apt-get clean && rm -rf /var/lib/apt/lists/*