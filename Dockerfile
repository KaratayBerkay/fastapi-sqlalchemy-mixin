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
COPY api.env /application/api.env
COPY postgres.env /application/postgres.env
COPY api_config.py /application/api_config.py
COPY db_config.py /application/db_config.py
COPY alembic /application/alembic
COPY alembic.ini /application/alembic.ini

# Run the application using the configured uvicorn server
CMD ["poetry", "run", "python", "app.py"]
