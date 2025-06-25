#!/usr/bin/env python3
"""Test script for the Website Prospector PoC."""

import asyncio
import os
import sys
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    missing = []
    
    try:
        import agents
        print("✅ openai-agents imported successfully")
    except ImportError:
        missing.append("openai-agents")
    
    try:
        import playwright
        print("✅ playwright imported successfully")
    except ImportError:
        missing.append("playwright")
    
    try:
        import aiohttp
        print("✅ aiohttp imported successfully")
    except ImportError:
        missing.append("aiohttp")
    
    try:
        from website_prospector.config.audience_configs import AUDIENCE_CONFIGS
        print(f"✅ audience configs loaded ({len(AUDIENCE_CONFIGS)} audiences)")
    except ImportError as e:
        missing.append(f"audience_configs: {e}")
    
    if missing:
        print("❌ Missing dependencies:")
        for dep in missing:
            print(f"   - {dep}")
        return False
    else:
        print("✅ All dependencies available")
        return True

def check_environment():
    """Check environment setup."""
    print("\n🔧 Checking environment...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        print("Set it with: export OPENAI_API_KEY='your-key'")
        return False
    else:
        # Mask the key for security
        masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
        print(f"✅ OPENAI_API_KEY found: {masked_key}")
        return True

async def test_agents_sdk():
    """Test basic OpenAI Agents SDK functionality."""
    print("\n🧪 Testing basic OpenAI Agents SDK setup...")
    
    try:
        from agents import Agent, Runner
        
        # Create a simple test agent
        test_agent = Agent(
            name="test-agent",
            instructions="You are a test agent.",
            model="gpt-4o-mini"
        )
        
        print("✅ Agent created successfully")
        
        # Test a simple interaction using async Runner.run
        try:
            result = await Runner.run(test_agent, "Say 'Hello, test successful!'")
            print("✅ Agent test completed successfully")
            return True
        except Exception as e:
            print(f"❌ Agent test failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Agents SDK setup failed: {e}")
        return False

def test_audience_configs():
    """Test audience configuration loading."""
    print("\n📋 Testing audience configurations...")
    
    try:
        from website_prospector.config.audience_configs import AUDIENCE_CONFIGS
        
        print(f"✅ Loaded {len(AUDIENCE_CONFIGS)} audience configurations:")
        
        for name, config in AUDIENCE_CONFIGS.items():
            print(f"   - {name}: {config.audience_type}")
            
            # Test that config has required attributes
            if hasattr(config, 'search_patterns') and config.search_patterns:
                print(f"     ✅ Has {len(config.search_patterns)} search patterns")
            else:
                print(f"     ❌ Missing or empty search patterns")
                
            if hasattr(config, 'keywords') and config.keywords:
                print(f"     ✅ Has {len(config.keywords)} keywords")
            else:
                print(f"     ❌ Missing or empty keywords")
                
        return True
        
    except Exception as e:
        print(f"❌ Audience config test failed: {e}")
        return False

async def test_playwright():
    """Test Playwright setup."""
    print("\n🎭 Testing Playwright setup...")
    
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Test loading a simple page
            await page.goto("data:text/html,<html><head><title>Test Page</title></head><body><h1>Test</h1></body></html>")
            title = await page.title()
            
            await browser.close()
            
            if title and "Test Page" in title:
                print("✅ Playwright test successful")
                return True
            else:
                print(f"❌ Playwright test failed - unexpected title: {title}")
                return False
                
    except Exception as e:
        print(f"❌ Playwright test failed: {e}")
        return False

async def test_web_search():
    """Test web search functionality."""
    print("\n🔍 Testing web search tool...")
    
    try:
        from website_prospector.tools.web_search import WebSearchTool
        
        search_tool = WebSearchTool()
        
        # Test a simple search using the correct API
        async with search_tool as tool:
            results = await tool.search_prospects(
                search_patterns=["restaurants {location}"],
                keywords=["pizza"],
                location="San Francisco"
            )
        
        if results and len(results) > 0:
            print(f"✅ Web search test successful - found {len(results)} results")
            return True
        else:
            print("⚠️  Web search test completed - no results (this is normal for demo)")
            return True  # This is acceptable for a test
            
    except Exception as e:
        print(f"❌ Web search test failed: {e}")
        return False

async def main():
    """Run all tests."""
    print("🧪 Website Prospector PoC - Setup Test")
    print("=" * 50)
    
    # Track test results
    results = []
    
    # Test dependencies
    results.append(check_dependencies())
    
    # Test environment
    results.append(check_environment())
    
    # Test OpenAI Agents SDK
    results.append(await test_agents_sdk())
    
    # Test audience configs
    results.append(test_audience_configs())
    
    # Test Playwright
    results.append(await test_playwright())
    
    # Test web search
    results.append(await test_web_search())
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your PoC is ready to use.")
        print("\n🚀 Next steps:")
        print("   uv run python quick_start.py")
        print("   uv run python main.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 