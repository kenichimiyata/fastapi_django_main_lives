#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Create database
python database.py
python database.py create_database

# Run Flask app
python app.py &
