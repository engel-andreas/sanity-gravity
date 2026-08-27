#!/bin/bash

# VSCodium: Additional agent-specific setup
# Skills synchronization is handled by the central sync-agent-resources script.
# This hook only handles agent-specific tasks that don't fit the central framework.
#
# Persist the OpenCode autoupdate opt-out where SSH sessions can see it.
# The binary lives in root-owned /usr/local/bin, so self-update could
# never succeed for the sandbox user and would only add startup noise.
# The documented config-file switch covers every entry path (VSCodium
# terminal, SSH, GUI-launched opencode). Seed-once: the file belongs to
# the user and may be edited later (providers, theme, ...), so an
# existing config is left untouched.

CONFIG_DIR="/home/$USER_NAME/.config/opencode"
CONFIG_FILE="$CONFIG_DIR/opencode.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Seeding OpenCode user config (autoupdate disabled)..."
    mkdir -p "$CONFIG_DIR"
    cat > "$CONFIG_FILE" <<EOF
{
  "\$schema": "https://opencode.ai/config.json",
  "autoupdate": false
}
EOF
    # Hooks run after the entrypoint's recursive home chown, so anything
    # created here must fix its own ownership.
    chown "$HOST_UID":"$HOST_GID" \
        "/home/$USER_NAME/.config" "$CONFIG_DIR" "$CONFIG_FILE"
fi