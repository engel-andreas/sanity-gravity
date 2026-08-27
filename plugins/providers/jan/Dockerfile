# Jan.ai provider layer (requires Xvfb for headless operation)
# Jan.ai is a desktop application that requires a virtual display.
# Models are stored in /workspace/models/jan (mounted at runtime).
ARG BASE_IMAGE=sanity-gravity:_base
FROM ${BASE_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive
ENV JAN_HOST=0.0.0.0:1337

# Install dependencies for Jan.ai AppImage
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    xvfb \
    libfuse2 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libgbm1 \
    && rm -rf /var/lib/apt/lists/*

# Download and install Jan.ai AppImage
RUN curl -fsSL -o /tmp/jan.AppImage https://github.com/janhq/jan/releases/latest/download/jan-linux-x86_64.AppImage \
    && chmod +x /tmp/jan.AppImage \
    && mkdir -p /opt/jan \
    && cd /opt/jan && /tmp/jan.AppImage --appimage-extract \
    && rm /tmp/jan.AppImage

# Create models directory
RUN mkdir -p /workspace/models/jan

# Add supervisord config for jan
COPY supervisord-jan.conf /etc/supervisor/conf.d/jan.conf

LABEL sanity.gravity.provider="jan"
LABEL sanity.gravity.provider.port="1337"
LABEL sanity.gravity.provider.env="JAN_BASE_URL,OPENAI_BASE_URL"
