## Stage 1: Build Stage
# Python Image
FROM python:3.12-slim AS builder

# Set enviroment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /home/app/web

# Install system dependecies for GDAL and Postgresql
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    gdal-bin \
    libgdal-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# install the python dependencies 
RUN pip install --upgrade pip 
COPY django_project/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

## Stage 2: Production Stage
FROM python:3.12-slim

# Install runtime dependencies for GDAL and PostgreSQL
RUN apt-get update && apt-get install -y \
        libgdal-dev \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# create non-root user in production to prevent security issues
RUN useradd -m -r appuser && \
    mkdir -p    /home/app/web/staticfiles /home/app/web/media /home/app/web/logs && \
    chown -R appuser:appuser /home/app/web

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# set the working directory
WORKDIR /home/app/web

# copy application code
COPY --chown=appuser:appuser django_project/ .

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV GUNICORN_WORKERS=3
ENV GUNICORN_PORT=8000

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Make entry file executable
COPY --chown=appuser:appuser infrastructure/docker/django/entrypoint.prod.sh .
RUN chmod +x entrypoint.prod.sh 

# health check (install curl first)
# RUN apt-get update && apt-get install -y curl \
#     && apt-get clean && rm -rf /var/lib/apt/lists/*

# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \ 
#                 CMD curl -f http://localhost:8000/health/ || exit 1

# Start the application using Gunicorn
CMD ["./entrypoint.prod.sh"]

    

