"""
Run the FastAPI application
"""
import uvicorn
import sys
import os
from pathlib import Path

# Add the parent directory to Python path so we can import app
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
