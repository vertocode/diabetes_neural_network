"""
Prediction endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.schemas import (
    PredictionRequest, 
    PredictionResponse, 
    BatchPredictionRequest, 
    BatchPredictionResponse
)
from app.services.model_service import ModelService

router = APIRouter()

def get_model_service() -> ModelService:
    """Dependency to get model service"""
    from app.main import model_service
    if model_service is None:
        raise HTTPException(status_code=503, detail="Model service not available")
    return model_service

@router.post("/predict", response_model=PredictionResponse)
async def predict_diabetes(
    request: PredictionRequest,
    model_service: ModelService = Depends(get_model_service)
):
    """
    Predict diabetes risk for a single patient
    
    - **gender**: Gender (0=Female, 1=Male)
    - **age**: Age in years
    - **hypertension**: Hypertension status (0=No, 1=Yes)
    - **heart_disease**: Heart disease status (0=No, 1=Yes)
    - **bmi**: Body Mass Index
    - **hba1c_level**: HbA1c level
    - **blood_glucose_level**: Blood glucose level
    - **is_smoker**: Smoking status (0=No, 1=Yes)
    """
    try:
        prediction = model_service.predict(request)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_diabetes_batch(
    request: BatchPredictionRequest,
    model_service: ModelService = Depends(get_model_service)
):
    """
    Predict diabetes risk for multiple patients
    
    - **patients**: List of patient data for batch prediction
    """
    try:
        if len(request.patients) > 100:  # Limit batch size
            raise HTTPException(status_code=400, detail="Batch size too large. Maximum 100 patients per request.")
        
        predictions = model_service.predict_batch(request.patients)
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_patients=len(predictions)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")

@router.get("/model/info")
async def get_model_info(model_service: ModelService = Depends(get_model_service)):
    """Get information about the loaded model"""
    try:
        model_info = model_service.get_model_info()
        return model_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}")
