"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import numpy as np

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    message: str
    version: str

class PredictionRequest(BaseModel):
    """Diabetes prediction request model"""
    gender: int = Field(..., description="Gender (0=Female, 1=Male)", ge=0, le=1)
    age: float = Field(..., description="Age in years", ge=0, le=120)
    hypertension: int = Field(..., description="Hypertension (0=No, 1=Yes)", ge=0, le=1)
    heart_disease: int = Field(..., description="Heart disease (0=No, 1=Yes)", ge=0, le=1)
    bmi: float = Field(..., description="Body Mass Index", ge=10, le=100)
    hba1c_level: float = Field(..., description="HbA1c level", ge=0, le=20)
    blood_glucose_level: float = Field(..., description="Blood glucose level", ge=0, le=500)
    is_smoker: int = Field(..., description="Smoking status (0=No, 1=Yes)", ge=0, le=1)
    
    @validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 120:
            raise ValueError('Age must be between 0 and 120')
        return v
    
    @validator('bmi')
    def validate_bmi(cls, v):
        if v < 10 or v > 100:
            raise ValueError('BMI must be between 10 and 100')
        return v

class PredictionResponse(BaseModel):
    """Diabetes prediction response model"""
    prediction: int = Field(..., description="Predicted diabetes status (0=No, 1=Yes)")
    probability: float = Field(..., description="Probability of diabetes (0-1)")
    confidence: str = Field(..., description="Confidence level (Low/Medium/High)")
    
class BatchPredictionRequest(BaseModel):
    """Batch prediction request model"""
    patients: List[PredictionRequest] = Field(..., description="List of patients for prediction")

class BatchPredictionResponse(BaseModel):
    """Batch prediction response model"""
    predictions: List[PredictionResponse] = Field(..., description="List of predictions")
    total_patients: int = Field(..., description="Total number of patients processed")
