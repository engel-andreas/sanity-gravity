# Ollama provider layer
# Installs Ollama server for local LLM inference.
# Models are stored in /workspace/models/ollama (mounted at runtime).
ARG BASE_IMAGE=sanity-gravity:_base
FROM ${BASE_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive
ENV OLLAMA_HOST=0.0.0.0:11434
ENV OLLAMA_MODELS=/workspace/models/ollama

# Install Ollama (requires zstd for extraction)
RUN apt-get update && apt-get install -y --no-install-recommends zstd && \
    rm -rf /var/lib/apt/lists/* && \
    curl -fsSL https://ollama.com/install.sh | sh

# Create models directory
RUN mkdir -p /workspace/models/ollama

# Add supervisord config for ollama
COPY supervisord-ollama.conf /etc/supervisor/conf.d/ollama.conf

LABEL sanity.gravity.provider="ollama"
LABEL sanity.gravity.provider.port="11434"
LABEL sanity.gravity.provider.env="OLLAMA_BASE_URL,OPENAI_BASE_URL"
