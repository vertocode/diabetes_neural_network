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

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Option 1: Start Both Services (Recommended)

#### 1. Create and activate a virtual environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

#### 2. Install dependencies
```bash
# Install API dependencies
pip install -r app/requirements.txt

# Install Streamlit dependencies
pip install -r streamlit_requirements.txt
```

#### 3. Start both services
```bash
python start_services.py
```

### Option 2: Using the setup script
```bash
# Make setup script executable (macOS/Linux)
chmod +x setup.sh

# Run setup script (creates venv and installs dependencies)
./setup.sh

# Start services
python start_services.py
```

### Option 3: Start Services Separately

#### Start API Server
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

cd app
pip install -r requirements.txt
python run.py
```

#### Start Streamlit App (in another terminal)
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

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

### Best Practices
- **Always use virtual environments** to isolate project dependencies
- **Keep dependencies up to date** and pin versions in requirements.txt
- **Test API endpoints** using the interactive docs at http://localhost:8000/docs
- **Follow PEP 8** coding standards for Python code
- **Use type hints** for better code documentation and IDE support

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
