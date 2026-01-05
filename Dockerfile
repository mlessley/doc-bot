# ==========================================
# STAGE 1: Base (Shared across all envs)
# ==========================================
FROM python:3.11-slim AS base

# Install uv (The modern way: copy the binary directly)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables for uv and Python
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    WORKDIR=/workspace

WORKDIR $WORKDIR

# ==========================================
# STAGE 2: Development / DevX
# ==========================================
FROM base AS development

# Install dev tools
RUN apt-get update && apt-get install -y \
    sudo git curl zsh build-essential \
    && rm -rf /var/lib/apt/lists/*

# Setup 'devx' user (UID 1000 for WSL2 parity)
ARG USERNAME=devx
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Setup Zsh (Portfolio touch)
RUN chsh -s /bin/zsh $USERNAME
USER $USERNAME

# Setup the virtual environment path for uv
ENV VIRTUAL_ENV=$WORKDIR/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Development-only behavior: Keep the container alive for VS Code
CMD ["sleep", "infinity"]


# ==========================================
# STAGE 3: Production (Drafted/Disabled)
# ==========================================
# This stage is essentially "invisible" during development.
# When you eventually run `docker build --target production`, 
# it will skip the Zsh/sudo/devx layers above.

# FROM base AS production
# 
# # Create a minimal, locked-down user
# RUN useradd -m appuser
# USER appuser
# 
# # Copy only the lockfiles first for caching
# COPY pyproject.toml uv.lock ./
# RUN uv sync --frozen --no-dev
# 
# # Copy the actual source code
# COPY ./src ./src
# 
# # Production entrypoint
# CMD ["python", "src/main.py"]