"""
FastAPI application for Diabetes Prediction Neural Network
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from app.api.v1.endpoints import prediction, health
from app.core.config import settings
from app.services.model_service import ModelService

# Global model service instance
model_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global model_service
    # Startup
    print("Loading diabetes prediction model...")
    model_service = ModelService()
    await model_service.load_model()
    print("Model loaded successfully!")
    
    yield
    
    # Shutdown
    print("Shutting down application...")

# Create FastAPI app
app = FastAPI(
    title="Diabetes Prediction API",
    description="A neural network API for diabetes prediction based on health metrics",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(prediction.router, prefix="/api/v1", tags=["prediction"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Diabetes Prediction API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
