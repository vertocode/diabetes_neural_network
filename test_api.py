#!/usr/bin/env python3
"""
Simple test script for the API
"""
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🏥 Starting Diabetes Prediction API...")
    print("=" * 50)
    print("API will be available at: http://127.0.0.1:8000")
    print("API Documentation: http://127.0.0.1:8000/docs")
    print("Health Check: http://127.0.0.1:8000/api/v1/health")
    print("=" * 50)
    
    try:
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="info",
            reload=False
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down API...")
    except Exception as e:
        print(f"❌ Error starting API: {e}")
