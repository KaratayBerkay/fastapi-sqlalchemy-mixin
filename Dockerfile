FROM python:3.12-slim

WORKDIR /application

# Set Python path to include app directory
ENV PYTHONPATH=/application \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies and Poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir poetry

# Copy Poetry configuration
COPY pyproject.toml ./pyproject.toml

# Configure Poetry and install dependencies with optimizations
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --only main \
    && pip cache purge \
    && rm -rf ~/.cache/pypoetry

# Copy application code
COPY application /application

# Run the application using the configured uvicorn server
CMD ["poetry", "run", "python", "app.py"]
