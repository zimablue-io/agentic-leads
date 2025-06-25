#!/usr/bin/env python3
"""Quick start script for the Website Prospector PoC."""

import asyncio
import os
import sys
from pathlib import Path


def setup_environment():
    """Set up the environment for the PoC."""
    print("🚀 Website Prospector PoC - Quick Start")
    print("=" * 50)
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found!")
        print("\nPlease set your OpenAI API key:")
        print("1. Get an API key from: https://platform.openai.com/api-keys")
        print("2. Set it in your environment:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("\nOr copy env.example to .env and edit it:")
        print("   cp env.example .env")
        print("   # Edit .env with your API key")
        return False
    
    print("✅ OpenAI API key found")
    
    # Check Python version
    if sys.version_info < (3, 11):
        print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} detected")
        print("Python 3.11+ is required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True


async def run_quick_demo():
    """Run a quick demonstration of the workflow."""
    print("\n🎯 Running Quick Demo")
    print("=" * 30)
    
    try:
        from main import run_prospect_workflow
        
        print("Testing with 1 local business prospect...")
        await run_prospect_workflow(
            audience_name="local_business",
            location="San Francisco",
            max_prospects=1  # Just one for quick testing
        )
        
        print("\n🎉 Demo completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Run setup first: python setup.py")
        return False
    
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify your OpenAI API key is valid")
        print("3. Run the test script: python test_poc.py")
        return False


async def main():
    """Main quick start function."""
    
    # Check basic setup
    if not setup_environment():
        print("\n❌ Environment setup failed")
        sys.exit(1)
    
    # Ask user what they want to do
    print("\n🤔 What would you like to do?")
    print("1. Run quick demo (1 prospect)")
    print("2. Run full test (multiple prospects)")
    print("3. Run setup validation")
    print("4. Exit")
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    
    if choice == "1":
        success = await run_quick_demo()
        
    elif choice == "2":
        try:
            from main import run_prospect_workflow
            await run_prospect_workflow(
                audience_name="local_business",
                location="San Francisco",
                max_prospects=3
            )
            success = True
        except Exception as e:
            print(f"❌ Full test failed: {e}")
            success = False
    
    elif choice == "3":
        print("\n🧪 Running validation tests...")
        from test_poc import main as test_main
        success = await test_main()
    
    elif choice == "4":
        print("👋 Goodbye!")
        sys.exit(0)
    
    else:
        print("❌ Invalid choice")
        success = False
    
    if success:
        print("\n✨ Success! Your PoC is working.")
        print("\nNext steps:")
        print("• Modify audience configs in website_prospector/config/audience_configs.py")
        print("• Adjust analysis weights in main.py")
        print("• View traces in OpenAI Dashboard")
        print("• Scale to production with database integration")
    else:
        print("\n⚠️  Something went wrong. Check the error messages above.")
        print("For help, see README.md or run: python test_poc.py")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
        sys.exit(0) 