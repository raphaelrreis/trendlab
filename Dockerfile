# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install system build dependencies
RUN apt-get update && apt-get install -y build-essential curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - 
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files
COPY pyproject.toml .

# Install dependencies (no dev, no root package yet)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --only main

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies (if any specific libs needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY trendlab /app/trendlab
COPY README.md /app/

# Setup directories for persistence
RUN mkdir -p /app/data /app/reports

# Environment variables
ENV PYTHONPATH=/app
ENV DATA_DIR=/app/data
ENV REPORT_DIR=/app/reports

# Create non-root user
RUN useradd -m trendlab && chown -R trendlab:trendlab /app
USER trendlab

# Expose API port
EXPOSE 8080

# Default command
CMD ["uvicorn", "trendlab.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
