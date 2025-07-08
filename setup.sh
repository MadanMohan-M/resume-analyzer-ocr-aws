#!/bin/bash

echo "🔧 Installing Poppler and Tesseract..."
apt-get update && apt-get install -y poppler-utils tesseract-ocr

echo "✅ Installation completed."
