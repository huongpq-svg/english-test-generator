#!/bin/bash
# Install dependencies if needed (comment out if managed manually)
pip install fastapi uvicorn sqlalchemy requests

# Add src to PYTHONPATH so imports like 'from database' work
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

# Seed the database
python src/seed.py

# Run the API
echo "Starting API on http://localhost:8000..."
uvicorn src.api:app --reload --port 8000
