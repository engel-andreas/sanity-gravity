# Default is unused; always overridden by --build-arg. Set to suppress Docker warning.
ARG BASE_IMAGE=ubuntu:24.04
FROM ${BASE_IMAGE}

# Claude Code Agent Layer
# Installs Anthropic Claude Code CLI via official installer.
#
# The entrypoint hook in rootfs/ mirrors skills found anywhere under the
# mounted workspace into ~/.claude/skills (symlink per skill folder), since
# Claude Code discovers global skills only from that fixed location and has
# no configurable search roots like opencode's skills.paths.

# Install Claude Code (official method) and symlink to global path
RUN curl -fsSL https://claude.ai/install.sh | bash && \
    cp /root/.local/bin/claude /usr/local/bin/claude && \
    chmod 755 /usr/local/bin/claude

COPY rootfs/ /
