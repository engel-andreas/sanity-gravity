# LM Studio provider layer (llmster - headless mode)
# Installs LM Studio's headless daemon for local LLM inference.
# Models are stored in /workspace/models/lmstudio (mounted at runtime).
ARG BASE_IMAGE=sanity-gravity:_base
FROM ${BASE_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive
ENV LM_STUDIO_HOST=0.0.0.0:1234

# Install dependencies for llmster
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libatomic1 \
    && rm -rf /var/lib/apt/lists/*

# Install llmster (LM Studio headless daemon)
RUN curl -fsSL https://lmstudio.ai/install.sh | bash

# Add lms to PATH
ENV PATH="/root/.lmstudio/bin:${PATH}"

# Create models directory
RUN mkdir -p /workspace/models/lmstudio

# Add supervisord config for lmstudio
COPY supervisord-lmstudio.conf /etc/supervisor/conf.d/lmstudio.conf

LABEL sanity.gravity.provider="lmstudio"
LABEL sanity.gravity.provider.port="1234"
LABEL sanity.gravity.provider.env="LM_STUDIO_BASE_URL,OPENAI_BASE_URL"
