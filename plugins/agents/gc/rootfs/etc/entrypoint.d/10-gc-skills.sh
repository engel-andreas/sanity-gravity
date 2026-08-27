#!/bin/bash

# Gemini CLI: Additional agent-specific setup
# Skills synchronization is handled by the central sync-agent-resources script.
# This hook only handles agent-specific tasks that don't fit the central framework.
#
# Note: Gemini CLI is being transitioned to Antigravity CLI (agy) as of
# June 2026. This hook remains for backward compatibility.

# Ensure .gemini directory exists for agent-specific configs
mkdir -p "/home/$USER_NAME/.gemini"

exit 0
