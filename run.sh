#!/bin/bash

# Create and activate virtual environment
python3 -m venv venv
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the script
python server.py $1
