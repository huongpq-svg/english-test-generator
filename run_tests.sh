#!/bin/bash
# Install test dependencies
pip install pytest httpx uvicorn sqlalchemy requests

# Export PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

# Run tests using 'python -m pytest' which uses the active pip env
python -m pytest tests/ -v
