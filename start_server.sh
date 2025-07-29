#!/bin/bash

# Activate virtual environment
source automotive_news_env/bin/activate

# Start the FastAPI server
echo "Starting Automotive News Aggregator..."
echo "The application will be available at http://localhost:8000"
echo "Press Ctrl+C to stop the server"

python3 app.py