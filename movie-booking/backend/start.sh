#!/bin/sh
echo "Running database migrations..."
python -m alembic upgrade head

echo "Seeding database..."
python -m scripts.seed

echo "Starting Uvicorn server..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}