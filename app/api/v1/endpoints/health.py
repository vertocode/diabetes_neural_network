"""
Health check endpoints
"""
from fastapi import APIRouter, Depends
from app.models.schemas import HealthResponse
from app.services.model_service import ModelService

router = APIRouter()

def get_model_service() -> ModelService:
    """Dependency to get model service"""
    from app.main import model_service
    if model_service is None:
        raise Exception("Model service not initialized")
    return model_service

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Diabetes Prediction API is running",
        version="1.0.0"
    )

@router.get("/health/detailed")
async def detailed_health_check(model_service: ModelService = Depends(get_model_service)):
    """Detailed health check including model status"""
    model_info = model_service.get_model_info()
    
    return {
        "status": "healthy" if model_info["status"] == "loaded" else "degraded",
        "message": "Diabetes Prediction API is running",
        "version": "1.0.0",
        "model": model_info,
        "timestamp": "2024-01-01T00:00:00Z"  # In production, use actual timestamp
    }
