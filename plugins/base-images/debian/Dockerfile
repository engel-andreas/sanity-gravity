# Pinned: debian:12 (bookworm 12.15) as of 2026-08-05
# Multi-arch manifest list digest so amd64/arm64 builds resolve the
# correct platform image. Default is unused unless building directly;
# the CLI always passes --build-arg BASE_IMAGE=<parent>.
ARG BASE_IMAGE=debian:12@sha256:813017f3d62be4b5891a7acca6a01bdcd4b8513daa81b1ab99d3a50385b26931
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
