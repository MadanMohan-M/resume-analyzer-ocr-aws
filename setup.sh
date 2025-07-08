#!/bin/bash

# Grant root permissions
echo "Installing system dependencies..."
apt-get update -y && apt-get install -y tesseract-ocr poppler-utils

# Start the Streamlit app
streamlit run app.py --server.port=$PORT
