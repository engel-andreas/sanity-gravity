# Default is unused; always overridden by --build-arg. Set to suppress Docker warning.
ARG BASE_IMAGE=ubuntu:24.04
FROM ${BASE_IMAGE}

# Gemini CLI Agent Layer
# Installs Node.js LTS and Google Gemini CLI

# Install Node.js 22 LTS via NodeSource
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get autoremove -y && \
    rm -rf /usr/share/doc/* /usr/share/info/* /usr/share/lintian/* /usr/share/man/* \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Gemini CLI globally, then patch npm's bundled picomatch (CVE-2026-33671)
RUN npm install -g @google/gemini-cli && \
    cd /usr/lib/node_modules/npm/node_modules/picomatch && \
    npm pack picomatch@4.0.4 && tar xzf picomatch-4.0.4.tgz --strip-components=1 && rm picomatch-4.0.4.tgz && \
    npm cache clean --force

# The entrypoint hook in rootfs/ mirrors workspace skills into Gemini CLI's
# global skill directory (~/.gemini/skills/) via symlinks.
# Note: Gemini CLI is transitioning to Antigravity CLI (agy) as of June 2026.
COPY rootfs/ /
