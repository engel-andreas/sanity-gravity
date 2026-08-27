#!/bin/bash

# Antigravity CLI: Additional agent-specific setup
# Skills synchronization is handled by the central sync-agent-resources script.
# This hook only handles agent-specific tasks that don't fit the central framework.
# See: antigravity.google/docs/cli/plugins

# Ensure .gemini/antigravity-cli directory exists for agent-specific configs
mkdir -p "/home/$USER_NAME/.gemini/antigravity-cli"

exit 0
