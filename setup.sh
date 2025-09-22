#!/bin/bash

echo "🏥 Setting up Diabetes Prediction System..."
echo "============================================="

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install API dependencies
echo "📚 Installing API dependencies..."
pip install -r app/requirements.txt

# Install Streamlit dependencies
echo "🎨 Installing Streamlit dependencies..."
pip install -r streamlit_requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the system:"
echo "   python start_services.py"
echo ""
echo "🌐 Access points:"
echo "   - Streamlit App: http://localhost:8501"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
