#!/bin/bash

# Create virtual environment only if it doesn't exist
if [ ! -d "antenv" ]; then
  python3.11 -m venv antenv
fi

# Activate the virtual environment
source antenv/bin/activate

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Run the Streamlit app on port 8000 (required by Azure)
exec streamlit run app.py --server.port 8000 --server.address 0.0.0.0
