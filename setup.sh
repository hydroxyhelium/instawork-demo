#!/bin/bash

# Install dependencies from requirements.txt
pip3 install -r instawork/requirements.txt

# Navigate to the instawork directory
cd instawork

# Apply database migrations
python3 manage.py migrate

# Run the development server
python3 manage.py runserver