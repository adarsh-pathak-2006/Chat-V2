#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files (needed for WhiteNoise)
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate
