# Pinned: debian:13-slim (trixie 13.6) as of 2026-08-31
# Slim drops man pages, docs, and the apt package lists for a ~40MB
# smaller base image; findutils/coreutils/etc. (priority "important")
# are still present, so entrypoint/cleanup scripts keep working.
# Multi-arch manifest list digest so amd64/arm64 builds resolve the
# correct platform image. Default is unused unless building directly;
# the CLI always passes --build-arg BASE_IMAGE=<parent>.
ARG BASE_IMAGE=debian:13-slim@sha256:d7e12182ce18b85b93007c1dedf31f2d29e01ccf3182cc4017c709b6259bc132
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
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-deu \
    && apt-get autoremove -y && \
    rm -rf /usr/share/doc/* /usr/share/info/* /usr/share/lintian/* /usr/share/man/* \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Node.js 24 LTS via NodeSource (matches plugins/agents/gc pattern)
# Needed as the container runtime for Node-based MCP servers (e.g. ZVG portal).
RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get autoremove -y && \
    rm -rf /usr/share/doc/* /usr/share/info/* /usr/share/lintian/* /usr/share/man/* \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Setup Locales - keep only en_US.UTF-8 and drop the full locale archive,
# the i18n source data, and all non-English gettext catalogs. LC_ALL=C.UTF-8
# stays valid because glibc >= 2.35 provides C.UTF-8 as a builtin locale.
RUN locale-gen en_US.UTF-8 && \
    rm -rf /usr/lib/locale/locale-archive && \
    localedef -i en_US -f UTF-8 en_US.UTF-8 && \
    rm -rf /usr/share/i18n/charmaps /usr/share/i18n/locales && \
    find /usr/share/locale -mindepth 1 -maxdepth 1 \
        ! -name 'en_US*' ! -name 'locale.alias' ! -name 'C*' -exec rm -rf {} +

# Setup SSH Config
RUN mkdir -p /var/run/sshd && \
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
