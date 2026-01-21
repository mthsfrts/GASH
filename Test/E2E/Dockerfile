# Dockerfile for GASH E2E Tests
# Provides isolated environment for running end-to-end tests

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional test dependencies
RUN pip install --no-cache-dir \
    pytest-docker \
    pytest-timeout \
    psutil

# Copy application code
COPY . .

# Set Python path to include project root
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create directory for test outputs
RUN mkdir -p /app/test-results

# Default command: run E2E tests
CMD ["pytest", "Test/E2E/", "-v", "--tb=short", "--junitxml=/app/test-results/e2e-results.xml"]
