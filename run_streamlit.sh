#!/bin/bash

# Script to start Streamlit with direct model loading
# Kills processes on port 8501 if they exist and starts Streamlit

echo "Starting Diabetes Prediction Streamlit App..."

# Activate virtual environment
echo "Activating virtual environment 'diabetes'..."
source ~/.pyenv/versions/diabetes/bin/activate

# Check if port 8501 is in use
echo "Checking port 8501..."
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null ; then
    echo "Port 8501 is in use. Killing processes..."
    lsof -ti:8501 | xargs kill -9
    sleep 2
    echo "Processes on port 8501 terminated."
else
    echo "Port 8501 is free."
fi

# Check if streamlit_app.py file exists
if [ ! -f "streamlit_app.py" ]; then
    echo "File streamlit_app.py not found!"
    echo "   Make sure you are in the correct directory."
    exit 1
fi

# Check if model exists
if [ ! -f "notebooks/model.h5" ]; then
    echo "Model notebooks/model.h5 not found!"
    echo "   Make sure the model is in the correct location."
    exit 1
fi

echo "Files verified successfully."

# Start Streamlit
echo "Starting Streamlit..."
echo "   URL: http://localhost:8501"
echo "   To stop: Ctrl+C"
echo ""

streamlit run streamlit_app.py
