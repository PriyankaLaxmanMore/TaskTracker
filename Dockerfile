# =========================
# Stage 1: Build + Test
# =========================
FROM python:3.12-slim AS builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run tests in build stage (CI-quality enforcement)
# RUN pytest --cov=. --cov-fail-under=80


# =========================
# Stage 2: Runtime (lean image)
# =========================
FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN useradd -m appuser

# Copy only required artifacts
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

# Fix permissions
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]