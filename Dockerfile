# ===============================
# Stage 1: Build dependencies
# ===============================
FROM python:3.11-slim AS builder

# Install build dependencies temporarily
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /install

COPY requirements.txt .

# Install Python packages into /install directory
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ===============================
# Stage 2: Runtime image
# ===============================
FROM python:3.11-slim

# Create app directory
WORKDIR /app

# Copy installed Python packages from builder stage
COPY --from=builder /install /usr/local

# Copy application files
COPY . .

# Remove Python cache files to reduce size
RUN find /usr/local -type d -name "__pycache__" -exec rm -r {} + || true \
    && find /usr/local -type f -name "*.pyc" -delete || true

# Expose Dash port
EXPOSE 8050

# Fly.io will use this command
CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]
