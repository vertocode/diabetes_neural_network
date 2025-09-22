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

def start_api():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    os.chdir("app")
    subprocess.run([sys.executable, "run.py"])

def start_streamlit():
    """Start the Streamlit app"""
    print("⏳ Waiting for API to start...")
    time.sleep(5)  # Wait for API to start
    print("🎨 Starting Streamlit app...")
    os.chdir("..")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])

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
