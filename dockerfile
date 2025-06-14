# Dockerfile
FROM python:3.13-slim

# Set environment variables for better Python and pip performance
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0

# Set working directory
WORKDIR /app

# Install system dependencies and cleanup in the same layer
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        openssl \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Generate RSA keys and JWKS at build time
RUN mkdir -p keys \
    && openssl genrsa -out keys/private.pem 2048 \
    && openssl rsa -in keys/private.pem -pubout -out keys/public.pem \
    && python -c "from config import Config; Config.generate_jwks()"

# Create non-root user for security
RUN useradd -m appuser \
    && chown -R appuser:appuser /app \
    && chmod -R 500 /app \
    && chmod -R 600 /app/keys/private.pem
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/.well-known/openid-configuration || exit 1

# Start the server with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "app:app"]
# Use the following command to build the Docker image
# docker build -t flask-app .   
# Use the following command to run the Docker container
# docker run -p 5000:5000 flask-app
