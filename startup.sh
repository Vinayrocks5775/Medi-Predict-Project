#!/bin/bash
echo "Launching Streamlit app on Azure..."
streamlit run app.py --server.enableCORS false --server.port 8000 --server.address 0.0.0.0

