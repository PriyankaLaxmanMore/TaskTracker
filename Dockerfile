# =========================
# Stage 1: Build + Test
# =========================
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system dependencies (needed for psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better Docker cache)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Run tests
RUN pytest --cov=. --cov-fail-under=80


# =========================
# Stage 2: Runtime
# =========================
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependency for PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home appuser

# Copy installed Python packages
COPY --from=builder /usr/local /usr/local

# Copy only application files
COPY --from=builder /app/main.py .
COPY --from=builder /app/crud.py .
COPY --from=builder /app/database.py .
COPY --from=builder /app/model.py .
COPY --from=builder /app/schemas.py .
COPY --from=builder /app/logger.py .
COPY --from=builder /app/context.py .
COPY --from=builder /app/.env ./

# Change ownership
RUN chown -R appuser:appuser /app

# Run as non-root
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]