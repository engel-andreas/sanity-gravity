ARG BASE_IMAGE=sanity-gravity:_base
FROM ${BASE_IMAGE}

# Install Cinnamon Desktop and Core Utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    # --- Cinnamon Core & Session ---
    cinnamon-core \
    cinnamon-screensaver \
    # --- Core Utilities (replaces XFCE-Tools) ---
    nemo \
    gnome-terminal \
    gnome-system-monitor \
    gnome-screenshot \
    file-roller \
    # --- Shared X11, DBus & System Utilities ---
    dbus \
    dbus-x11 \
    x11-utils \
    x11-xserver-utils \
    x11-apps \
    xdotool \
    mesa-utils \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# Register standard desktop session launcher contract
RUN echo '#!/bin/sh\nexec cinnamon-session' > /usr/local/bin/desktop-session \
    && chmod +x /usr/local/bin/desktop-session

