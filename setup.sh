#!/bin/bash
# Setup script for Xt-EHR T7.2 Imaging Reports Analysis
# ====================================================

echo "Setting up Xt-EHR T7.2 Imaging Reports Analysis environment..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    source .venv/Scripts/activate
else
    # Unix/macOS
    source .venv/bin/activate
fi

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install core requirements
echo "Installing core dependencies..."
pip install -r requirements.txt

# Optional: Install development dependencies
read -p "Install development dependencies? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing development dependencies..."
    pip install -r requirements-dev.txt
fi

echo "Setup complete!"
echo ""
echo "To start the application:"
echo "1. Activate the virtual environment:"
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "   .venv\\Scripts\\activate"
else
    echo "   source .venv/bin/activate"
fi
echo "2. Run the Flask application:"
echo "   cd flask_app"
echo "   python app.py"
echo ""
echo "The application will be available at http://localhost:5000"