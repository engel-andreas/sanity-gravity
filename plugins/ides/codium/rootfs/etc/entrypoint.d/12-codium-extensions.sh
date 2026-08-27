#!/bin/bash

# VSCodium: seed the baked-in OpenCode extension into the sandbox user's
# extension dir.
# The Dockerfile installs sst-dev.opencode-v2 while HOME=/root (the image
# builds as root), so VSCodium records it under
# /root/.vscode-oss/extensions. The GUI runs as the user created at boot
# with HOME=/home/$USER_NAME, so without a copy the extension would be
# invisible to them. Seed-once: the dir belongs to the user and may be
# edited later (the user can update or remove the extension inside the
# IDE), so an already-present copy is left untouched.

SRC="/root/.vscode-oss/extensions"
DST="/home/$USER_NAME/.vscode-oss/extensions"

if [ ! -d "$SRC" ] || ! compgen -G "$SRC"/sst-dev.opencode-v2-* > /dev/null; then
    # No extension was baked into the image; nothing to seed.
    exit 0
fi

if compgen -G "$DST"/sst-dev.opencode-v2-* > /dev/null; then
    echo "OpenCode extension already present — leaving untouched"
    exit 0
fi

echo "Seeding OpenCode extension into $DST..."
mkdir -p "$DST"
cp -r "$SRC"/sst-dev.opencode-v2-* "$DST"/
# Hooks run after the entrypoint's recursive home chown, so anything
# created here must fix its own ownership.
chown "$HOST_UID":"$HOST_GID" "/home/$USER_NAME/.vscode-oss" "$DST"