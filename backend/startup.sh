#!/bin/bash
# Startup script for Azure App Service deployment

# Number of worker processes (adjust based on App Service tier)
# Formula: (2 x NUM_CORES) + 1
# For Basic/Standard tier: use 2-4 workers
WORKERS=${GUNICORN_WORKERS:-2}

# Timeout for worker processes (seconds)
TIMEOUT=${GUNICORN_TIMEOUT:-120}

# Bind address (Azure expects 0.0.0.0:8000)
BIND=${GUNICORN_BIND:-0.0.0.0:8000}

# Log level
LOG_LEVEL=${GUNICORN_LOG_LEVEL:-info}

echo "Starting Gunicorn with Uvicorn workers..."
echo "Workers: $WORKERS"
echo "Timeout: $TIMEOUT"
echo "Bind: $BIND"
echo "Log Level: $LOG_LEVEL"

# Start Gunicorn with Uvicorn worker class
# This combines Gunicorn's process management with Uvicorn's async performance
exec gunicorn main:app \
    --workers $WORKERS \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind $BIND \
    --timeout $TIMEOUT \
    --log-level $LOG_LEVEL \
    --access-logfile - \
    --error-logfile - \
    --capture-output
