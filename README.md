# Diabetes Prediction Neural Network

A professional neural network system for diabetes prediction with a FastAPI backend and Streamlit frontend.

## Project Structure

```
diabetes-neural-network/
├── app/                          # FastAPI backend
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/        # API endpoints
│   ├── core/                     # Configuration
│   ├── models/                   # Pydantic models
│   ├── services/                 # Business logic
│   ├── requirements.txt          # API dependencies
│   └── run.py                    # API runner
├── notebooks/                    # Jupyter notebooks
│   ├── baseline_model.ipynb      # Baseline model (89.57% recall)
│   ├── deeper_model.ipynb        # Best model (96.92% recall) ⭐
│   └── model_2025_09_21.ipynb    # Additional experiments
├── streamlit_app.py              # Streamlit frontend
├── streamlit_requirements.txt    # Frontend dependencies
└── start_services.py             # Start both services
```

## Quick Start

### Option 1: Start Both Services (Recommended)
```bash
# Install dependencies
pip install -r app/requirements.txt
pip install -r streamlit_requirements.txt

# Start both API and Streamlit
python start_services.py
```

### Option 2: Start Services Separately

#### Start API Server
```bash
cd app
pip install -r requirements.txt
python run.py
```

#### Start Streamlit App (in another terminal)
```bash
pip install -r streamlit_requirements.txt
streamlit run streamlit_app.py
```

## Access Points

- **Streamlit App**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/api/v1/health

## Model Performance

| Model | Architecture | Recall | File |
|-------|-------------|--------|------|
| **Best Model** | 5-layer deep network | **96.92%** | `deeper_model.ipynb` ⭐ |
| Baseline | 2-layer simple | 89.57% | `baseline_model.ipynb` |
| Experiments | Various architectures | ~68% | `model_2025_09_21.ipynb` |

## API Endpoints

### Health Check
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed health with model status

### Predictions
- `POST /api/v1/predict` - Single patient prediction
- `POST /api/v1/predict/batch` - Batch predictions (max 100)
- `GET /api/v1/model/info` - Model information

### Example API Usage

```python
import requests

# Single prediction
response = requests.post("http://localhost:8000/api/v1/predict", json={
    "gender": 1,
    "age": 45.0,
    "hypertension": 0,
    "heart_disease": 0,
    "bmi": 25.5,
    "hba1c_level": 5.2,
    "blood_glucose_level": 120.0,
    "is_smoker": 0
})

print(response.json())
# Output: {"prediction": 0, "probability": 0.15, "confidence": "High"}
```

## 📊 Features

### API Features
- ✅ RESTful API with FastAPI
- ✅ Input validation with Pydantic
- ✅ Automatic API documentation
- ✅ Health monitoring endpoints
- ✅ Batch processing support
- ✅ CORS enabled for frontend integration

### Frontend Features
- ✅ Interactive Streamlit interface
- ✅ Real-time predictions
- ✅ Risk factor analysis
- ✅ Visual feedback and charts
- ✅ Professional UI/UX design

## 🛠️ Development

### Adding New Features
1. **API**: Add endpoints in `app/api/v1/endpoints/`
2. **Models**: Update schemas in `app/models/schemas.py`
3. **Services**: Add business logic in `app/services/`
4. **Frontend**: Modify `streamlit_app.py`

### Model Training
The best performing model is in `notebooks/deeper_model.ipynb` with:
- 5-layer architecture (10→64→32→16→1)
- Focal loss for imbalanced data
- 96.92% recall performance

## Notes

- The API uses a placeholder model architecture for demonstration
- In production, load the actual trained model weights
- Configure CORS origins appropriately for production
- Add proper authentication and rate limiting for production use

## Disclaimer

This tool is for educational and research purposes only. Always consult healthcare professionals for medical advice and diagnosis.
