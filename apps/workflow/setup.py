#!/usr/bin/env python3
"""Setup script for the website prospector workflow."""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Main setup function."""
    print("🚀 Setting up Website Prospector Workflow")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 or higher is required")
        sys.exit(1)
    
    print("✅ Python 3.11 detected")
    
    # Check if uv is available
    if not run_command("which uv", "Checking for uv"):
        print("❌ uv not found. Please install uv first:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)
    
    # Install dependencies using uv
    if not run_command("uv sync", "Installing Python dependencies"):
        sys.exit(1)
    
    # Install Playwright browsers
    if not run_command("uv run playwright install", "Installing Playwright browsers"):
        print("⚠️  Playwright browser installation failed, but continuing...")
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY not found in environment")
        print("📝 Please set your OpenAI API key:")
        print("   1. Get an API key from: https://platform.openai.com/api-keys")
        print("   2. Copy env.example to .env: cp env.example .env")
        print("   3. Edit .env and add your API key")
        print("   4. Load it: source .env")
    else:
        print("✅ OPENAI_API_KEY found")
    
    print("\n🎉 Setup complete!")
    print("📋 Next steps:")
    print("   1. Set your OpenAI API key (if not already done)")
    print("   2. Run: uv run python test_poc.py")
    print("   3. Run: uv run python quick_start.py")
    print("   4. Run: uv run python main.py")


if __name__ == "__main__":
    main() 