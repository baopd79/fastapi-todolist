# syntax=docker/dockerfile:1.7
# ============================================
# Stage 1: Builder — install dependencies
# ============================================
FROM python:3.12-slim AS builder

# Install uv (Astral's Python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Environment for uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

# Copy only dependency files first (for layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies into /app/.venv
# --no-install-project: don't install our app code yet (we'll mount it)
# --no-dev: skip dev dependencies (pytest, ruff, mypy)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# ============================================
# Stage 2: Runtime — minimal image to run app
# ============================================
FROM python:3.12-slim AS runtime

# Install runtime system deps only (no build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (security best practice)
RUN groupadd --system app && useradd --system --gid app --no-create-home app

WORKDIR /app

# Copy virtualenv from builder stage
COPY --from=builder --chown=app:app /app/.venv /app/.venv

# Copy application code
COPY --chown=app:app ./app ./app

# Use the venv's Python by default
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Switch to non-root user
USER app

# Expose port (documentation only, doesn't actually publish)
EXPOSE 8000

# Default command (overridable in compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]