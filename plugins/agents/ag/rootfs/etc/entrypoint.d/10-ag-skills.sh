#!/bin/bash

# Antigravity IDE: Additional agent-specific setup
# Skills synchronization is handled by the central sync-agent-resources script.
# This hook only handles agent-specific tasks that don't fit the central framework.

# Ensure .gemini/config directory exists for agent-specific configs
mkdir -p "/home/$USER_NAME/.gemini/config"

exit 0
