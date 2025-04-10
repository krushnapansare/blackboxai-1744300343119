#!/bin/bash
# Install dependencies
pip install -r requirements.txt gunicorn

# Start Gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 wsgi:app
