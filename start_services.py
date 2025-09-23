#!/usr/bin/env python3
"""
Script to start both API and Streamlit services
"""
import subprocess
import sys
import time
import threading
import os
from pathlib import Path

def get_python_executable():
    """Get the correct Python executable (prefer venv if available)"""
    # Check for different possible venv locations
    possible_venvs = [
        Path("venv/bin/python"),
        Path(".venv/bin/python"),
        Path("env/bin/python"),
        Path(".env/bin/python")
    ]
    
    for venv_python in possible_venvs:
        if venv_python.exists():
            print(f"Using virtual environment: {venv_python}")
            return str(venv_python)
    
    print("Using system Python (no virtual environment found)")
    return sys.executable

def get_streamlit_executable():
    """Get the correct Python executable for Streamlit (prefer venv if available)"""
    # Check for different possible venv locations
    possible_venvs = [
        Path("venv/bin/python"),
        Path(".venv/bin/python"),
        Path("env/bin/python"),
        Path(".env/bin/python")
    ]
    
    for venv_python in possible_venvs:
        if venv_python.exists():
            print(f"Using virtual environment for Streamlit: {venv_python}")
            return str(venv_python)
    
    print("Using system Python for Streamlit (no virtual environment found)")
    return sys.executable

def start_api():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    python_exe = get_python_executable()
    # Run from the project root, not from inside app directory
    subprocess.run([python_exe, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

def start_streamlit():
    """Start the Streamlit app"""
    print("⏳ Waiting for API to start...")
    time.sleep(5)  # Wait for API to start
    print("🎨 Starting Streamlit app...")
    # Don't change directory - stay in project root
    python_exe = get_streamlit_executable()
    subprocess.run([python_exe, "-m", "streamlit", "run", "streamlit_app.py"])

def main():
    """Main function to start both services"""
    print("🏥 Starting Diabetes Prediction System...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Start API in a separate thread
    api_thread = threading.Thread(target=start_api, daemon=True)
    api_thread.start()
    
    # Start Streamlit in the main thread
    start_streamlit()

if __name__ == "__main__":
    main()
