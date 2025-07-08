#!/bin/bash

apt-get update
apt-get install -y poppler-utils tesseract-ocr

streamlit run app.py --server.port=$PORT
