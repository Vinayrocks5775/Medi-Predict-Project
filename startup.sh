#!/bin/bash
echo "Creating venv and installing dependencies..."
python3.10 -m venv antenv
source antenv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Launching app..."
streamlit run app.py --server.port 8000 --server.address 0.0.0.0

