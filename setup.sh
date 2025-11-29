#!/bin/bash
# Setup script for WSL/Linux
# Supports both venv (traditional) and uv (modern, faster)

echo "🔧 Setting up NeuroFocus Smart Tank MCP Server..."

# Ensure uv is in PATH (for zsh/bash compatibility)
export PATH="$HOME/.local/bin:$PATH"

# Check if uv is installed (preferred method)
if command -v uv &> /dev/null; then
    echo "✅ Found uv - using fast setup method"
    echo "📦 Creating virtual environment with uv..."
    uv venv
    
    echo "🔌 Activating virtual environment..."
    source .venv/bin/activate
    
    echo "📥 Installing dependencies (this will be fast!)..."
    uv pip install -r requirements.txt
    
    VENV_PATH=".venv"
else
    echo "ℹ️  uv not found - using traditional venv method"
    echo "💡 Tip: Install uv for faster setup: curl -LsSf https://astral.sh/uv/install.sh | sh"
    
    # Check if Python 3 is installed
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
        exit 1
    fi
    
    # Check Python version
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    echo "✅ Found Python $PYTHON_VERSION"
    
    # Create virtual environment
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    
    # Activate virtual environment
    echo "🔌 Activating virtual environment..."
    source venv/bin/activate
    
    # Upgrade pip
    echo "⬆️  Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    
    VENV_PATH="venv"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
if [ "$VENV_PATH" = ".venv" ]; then
    echo "  source .venv/bin/activate"
else
    echo "  source venv/bin/activate"
fi
echo ""
echo "To run the server:"
echo "  python src/main.py"
echo ""

