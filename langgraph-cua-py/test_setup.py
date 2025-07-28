#!/usr/bin/env python3
"""
Test script for LangGraph CUA setup
This script will help verify that the installation is working and guide you through setting up API keys.
"""

import os
import sys
from dotenv import load_dotenv

def test_imports():
    """Test if all required packages can be imported."""
    print("🔍 Testing imports...")
    
    try:
        from langgraph_cua import create_cua
        print("✅ langgraph_cua imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import langgraph_cua: {e}")
        return False
    
    try:
        from langchain_openai import ChatOpenAI
        print("✅ langchain_openai imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import langchain_openai: {e}")
        return False
    
    try:
        import scrapybara
        print("✅ scrapybara imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import scrapybara: {e}")
        return False
    
    return True

def check_environment_variables():
    """Check if required environment variables are set."""
    print("\n🔍 Checking environment variables...")
    
    # Load from .env file if it exists
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    scrapybara_key = os.getenv("SCRAPYBARA_API_KEY")
    
    if openai_key and openai_key != "your_openai_api_key_here":
        print("✅ OPENAI_API_KEY is set")
    else:
        print("❌ OPENAI_API_KEY is not set or is placeholder")
        print("   You need to get an API key from: https://platform.openai.com/api-keys")
    
    if scrapybara_key and scrapybara_key != "your_scrapybara_api_key_here":
        print("✅ SCRAPYBARA_API_KEY is set")
    else:
        print("❌ SCRAPYBARA_API_KEY is not set or is placeholder")
        print("   You need to get an API key from: https://scrapybara.com/")
    
    return bool(openai_key and openai_key != "your_openai_api_key_here" and 
                scrapybara_key and scrapybara_key != "your_scrapybara_api_key_here")

def test_cua_creation():
    """Test if we can create a CUA graph."""
    print("\n🔍 Testing CUA graph creation...")
    
    try:
        from langgraph_cua import create_cua
        cua_graph = create_cua()
        print("✅ CUA graph created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create CUA graph: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 LangGraph CUA Setup Test")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed. Please check your installation.")
        return
    
    # Test environment variables
    env_ok = check_environment_variables()
    
    # Test CUA creation
    cua_ok = test_cua_creation()
    
    print("\n" + "=" * 40)
    if env_ok and cua_ok:
        print("🎉 Setup looks good! You can now run the examples.")
        print("\nNext steps:")
        print("1. Set your API keys in environment variables or .env file")
        print("2. Run: python examples/price-finder.py")
    else:
        print("⚠️  Setup incomplete. Please fix the issues above.")
        
        if not env_ok:
            print("\nTo set environment variables in PowerShell:")
            print("$env:OPENAI_API_KEY='your_openai_key_here'")
            print("$env:SCRAPYBARA_API_KEY='your_scrapybara_key_here'")
            
            print("\nOr create a .env file in this directory with:")
            print("OPENAI_API_KEY=your_openai_key_here")
            print("SCRAPYBARA_API_KEY=your_scrapybara_key_here")

if __name__ == "__main__":
    main() 