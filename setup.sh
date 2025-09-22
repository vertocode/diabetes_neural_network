#!/bin/bash

echo "🏥 Setting up Diabetes Prediction System..."
echo "============================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment already exists
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Removing old one..."
    rm -rf venv
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Install dependencies using the virtual environment's pip
echo "📚 Installing API dependencies..."
./venv/bin/pip install -r app/requirements.txt

echo "🎨 Installing Streamlit dependencies..."
./venv/bin/pip install -r streamlit_requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🔧 To activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "🚀 To start the system:"
echo "   python start_services.py"
echo ""
echo "🌐 Access points:"
echo "   - Streamlit App: http://localhost:8501"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "💡 Tip: The virtual environment will be activated automatically when you run start_services.py"
