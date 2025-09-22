"""
Application configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Model Configuration
    MODEL_PATH: str = "models/diabetes_model.h5"
    SCALER_PATH: str = "models/scaler.pkl"
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = ["http://localhost:8501", "http://127.0.0.1:8501"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
