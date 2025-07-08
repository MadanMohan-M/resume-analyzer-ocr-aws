#!/bin/bash

echo "🔧 Installing Tesseract OCR and Poppler..."
apt-get update && apt-get install -y tesseract-ocr poppler-utils
