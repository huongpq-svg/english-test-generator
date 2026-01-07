#!/bin/bash
# Use the same python environment as run_backend.sh
# Ensure dependencies are installed (redundant but safe)
pip install uvicorn sqlalchemy

# Set PYTHONPATH to include src
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

# Run inspection using 'python', which maps to the working Anaconda env
python inspect_db.py
