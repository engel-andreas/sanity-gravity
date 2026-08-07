#!/bin/bash
set -e

# Ensure environment variables
export USER=${USER}
export HOME=${HOME}

# Generate SSL certificate if missing (moved from Dockerfile for per-container uniqueness)
if [ ! -f /etc/ssl/certs/ssl-cert-snakeoil.pem ]; then
    sudo make-ssl-cert generate-default-snakeoil --force-overwrite
fi

# Cleanup locks
rm -f /tmp/.X1-lock /tmp/.X11-unix/X1

# ------------------------------------------------------------------
# Chrome Cleanup Strategy (For Snapshot Support)
# ------------------------------------------------------------------
# Source the shared cleanup script
if [ -f "/usr/local/bin/chrome-cleanup.sh" ]; then
    source /usr/local/bin/chrome-cleanup.sh
else
    echo "Warning: chrome-cleanup.sh not found!"
fi

# Setup VNC Directory
mkdir -p $HOME/.vnc

# Setup Password
# KasmVNC vncpasswd requires username and double entry
echo -e "${HOST_PASSWORD}\n${HOST_PASSWORD}\n" | vncpasswd -u $USER -w
# chmod 600 $HOME/.vnc/passwd

# Setup xstartup for Desktop Session
cat > $HOME/.vnc/xstartup <<EOF
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
exec /usr/local/bin/desktop-session
EOF
chmod +x $HOME/.vnc/xstartup

echo "Starting KasmVNC on port 8444..."
# Start KasmVNC
exec /usr/bin/vncserver :1 \
    -depth 24 \
    -geometry 1920x1080 \
    -websocketPort 8444 \
    -httpd /usr/share/kasmvnc/www \
    -fg

