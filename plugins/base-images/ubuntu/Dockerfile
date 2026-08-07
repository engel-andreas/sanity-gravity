# Pinned: ubuntu:24.04 as of 2026-03-30
# The default is unused unless building directly; the CLI always passes
# --build-arg BASE_IMAGE=<parent>. Kept as a default so bare builds
# (tests, ad-hoc `docker build -f plugins/base-images/ubuntu/Dockerfile sandbox`) work.
# Build context is sandbox/ because `COPY rootfs /` pulls from the shared
# sandbox/rootfs tree (see hooks/build._build_context_for).
ARG BASE_IMAGE=ubuntu:24.04@sha256:186072bba1b2f436cbb91ef2567abca677337cfc786c86e107d25b7072feef0c
FROM ${BASE_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8

# Install Core Dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    supervisor \
    sudo \
    vim-tiny \
    curl \
    wget \
    git \
    zsh \
    net-tools \
    locales \
    tzdata \
    ca-certificates \
    openssh-server \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Setup Locales
RUN locale-gen en_US.UTF-8

# Setup SSH Config
RUN mkdir /var/run/sshd && \
    echo 'PermitRootLogin no' >> /etc/ssh/sshd_config && \
    echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config

# Copy Rootfs (Configuration & Scripts)
# Copying the entire rootfs initially
COPY rootfs /

# Setup Entrypoint & Scripts
RUN mkdir -p /etc/entrypoint.d /etc/shutdown.d && \
    chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
