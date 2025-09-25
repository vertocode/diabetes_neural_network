# Diabetes Prediction Streamlit App

## How to run Streamlit

### Method 1: Automatic script (Recommended)
```bash
./run_streamlit.sh
```

### Method 2: Manual command
```bash
pyenv activate diabetes && streamlit run streamlit_app.py
```

## How to stop Streamlit

### Method 1: Automatic script
```bash
./stop_streamlit.sh
```

### Method 2: Manual command
```bash
# Press Ctrl+C in the terminal where Streamlit is running
# OR
lsof -ti:8501 | xargs kill -9
```

## What the scripts do

### `run_streamlit.sh`:
- Activates the `diabetes` virtual environment
- Checks if port 8501 is free
- Kills processes using port 8501
- Verifies that necessary files exist
- Starts Streamlit automatically
- Opens in browser at http://localhost:8501

### `stop_streamlit.sh`:
- Stops all Streamlit processes
- Frees port 8501
- Forces stop if necessary

## Requirements

- Python 3.11 with pyenv
- `diabetes` virtual environment configured
- `notebooks/model.h5` file present
- Dependencies installed in virtual environment

## Access

After running the script, access:
- **Local**: http://localhost:8501
- **Network**: http://192.168.0.104:8501 (or your local IP)

## File structure

```
diabetes-neural-network/
├── streamlit_app.py          # Main application
├── run_streamlit.sh          # Start script
├── stop_streamlit.sh         # Stop script
├── requirements.txt          # Dependencies
├── .streamlit/
│   └── config.toml          # Configuration
└── notebooks/
    └── model.h5             # Trained model
```

## Troubleshooting

### If port is in use error:
```bash
./stop_streamlit.sh
./run_streamlit.sh
```

### If model not found error:
Check if the `notebooks/model.h5` file exists

### If virtual environment error:
```bash
pyenv activate diabetes
pip install -r requirements.txt
```

## Features

- Direct loading of `model.h5`
- Intuitive interface for data input
- Real-time prediction
- Risk factors analysis
- Interactive visualizations
- Responsive design
