#!/bin/bash

echo "🚀 Setting up Website Prospector Workflow"
echo "=========================================="

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check if we're in the workflow directory
if [[ ! -f "pyproject.toml" ]]; then
    echo "❌ pyproject.toml not found. Please run this from the apps/workflow directory"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [[ ! -d ".venv" ]]; then
    echo "📦 Creating virtual environment..."
    uv venv
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
uv sync

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
uv run playwright install

# Check if OpenAI API key is set
if [[ -z "$OPENAI_API_KEY" ]]; then
    echo "⚠️  OPENAI_API_KEY not found in environment"
    echo "📝 Please set it by:"
    echo "   1. Copy env.example to .env: cp env.example .env"
    echo "   2. Edit .env and add your API key"
    echo "   3. Load it: source .env (or export OPENAI_API_KEY='your-key-here')"
else
    echo "✅ OPENAI_API_KEY found"
fi

echo ""
echo "🎉 Setup complete! You can now run:"
echo "   source .venv/bin/activate"
echo "   uv run python quick_start.py"
echo "   uv run python test_poc.py"
echo "   uv run python main.py" 