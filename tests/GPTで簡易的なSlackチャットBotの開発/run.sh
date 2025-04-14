#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Load environment variables
export $(cat .env | xargs)

# Run the lambda function with the event.json file
python lambda_function.py lambda_handler event.json
