#!/bin/bash

# Central resource synchronization hook
# Runs before agent-specific hooks to ensure all resources are available

if [[ -x /usr/local/bin/sync-agent-resources ]]; then
    echo "Running centralized resource synchronization..."
    /usr/local/bin/sync-agent-resources
fi

exit 0
