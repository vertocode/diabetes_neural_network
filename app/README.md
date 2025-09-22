# Diabetes Prediction API

A professional FastAPI-based neural network API for diabetes prediction based on health metrics.

## Features

- **Neural Network Model**: 5-layer deep neural network with 96.92% recall
- **RESTful API**: Clean, documented endpoints
- **Input Validation**: Pydantic models for request/response validation
- **Batch Processing**: Support for single and batch predictions
- **Health Monitoring**: Health check endpoints
- **CORS Support**: Ready for frontend integration

## API Endpoints

### Health Check
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed health check with model status

### Predictions
- `POST /api/v1/predict` - Single patient prediction
- `POST /api/v1/predict/batch` - Batch predictions (up to 100 patients)
- `GET /api/v1/model/info` - Model information

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Input Format

```json
{
  "gender": 1,
  "age": 45.0,
  "hypertension": 0,
  "heart_disease": 0,
  "bmi": 25.5,
  "hba1c_level": 5.2,
  "blood_glucose_level": 120.0,
  "is_smoker": 0
}
```

## Response Format

```json
{
  "prediction": 0,
  "probability": 0.15,
  "confidence": "High"
}
```

## Model Architecture

- **Input Layer**: 8 features
- **Hidden Layers**: 10 → 64 → 32 → 16 neurons
- **Output Layer**: 1 neuron (sigmoid activation)
- **Optimizer**: Adam
- **Loss Function**: Binary Crossentropy
- **Performance**: 96.92% recall
