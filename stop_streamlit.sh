#!/bin/bash

# Script to stop Streamlit
# Kills all Streamlit processes and frees port 8501

echo "Stopping Streamlit..."

# Kill Streamlit processes
echo "Looking for Streamlit processes..."
pkill -f streamlit

# Kill processes on port 8501
echo "Freeing port 8501..."
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null ; then
    lsof -ti:8501 | xargs kill -9
    echo "Port 8501 freed."
else
    echo "Port 8501 was already free."
fi

# Check if there are still processes
sleep 1
if pgrep -f streamlit > /dev/null; then
    echo "Streamlit processes still running. Force stopping..."
    pkill -9 -f streamlit
    sleep 1
fi

echo "Streamlit stopped successfully!"
