#!/bin/bash

# Quick start script for the application

echo "🚀 Starting GenAI Live Environment Assistant..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo "Please edit .env and add your OPENAI_API_KEY"
fi

# Run Streamlit
streamlit run app.py
