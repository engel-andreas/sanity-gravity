# GPT4All provider layer
# Installs GPT4All for local LLM inference.
# Models are stored in /workspace/models/gpt4all (mounted at runtime).
ARG BASE_IMAGE=sanity-gravity:_base
FROM ${BASE_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive
ENV GPT4ALL_HOST=0.0.0.0:4891

# Install Python and pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Install GPT4All
RUN pip3 install --no-cache-dir gpt4all

# Create models directory
RUN mkdir -p /workspace/models/gpt4all

# Add supervisord config for gpt4all
COPY supervisord-gpt4all.conf /etc/supervisor/conf.d/gpt4all.conf

LABEL sanity.gravity.provider="gpt4all"
LABEL sanity.gravity.provider.port="4891"
LABEL sanity.gravity.provider.env="GPT4ALL_BASE_URL,OPENAI_BASE_URL"
