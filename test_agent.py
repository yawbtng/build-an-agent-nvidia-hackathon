import os
import sys
from dotenv import load_dotenv

# Add the code directory to the Python path
sys.path.append('code')

# Load environment variables
load_dotenv("variables.env")
load_dotenv("secrets.env")

print("=== Testing Agent Setup ===")

# Check if required packages are installed
try:
    from docgen_agent import write_report
    print("✅ Successfully imported docgen_agent")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the project root directory")
    exit(1)

# Test the agent with a simple topic
print("\n=== Testing Agent ===")
try:
    result = write_report(
        topic="The benefits of using GPUs for AI training",
        report_structure="""This report should be informative and technical.
        The report structure should include:
        1. Introduction
        2. Main Body Sections:
           - One section for each major benefit
           - Each section should examine benefits and use cases
        3. Conclusion"""
    )
    
    if result and result.get("report"):
        print("✅ Agent ran successfully!")
        print(f"Report length: {len(result['report'])} characters")
        print("\n=== First 500 characters of report ===")
        print(result["report"][:500] + "...")
    else:
        print("❌ Agent ran but returned no report")
        
except Exception as e:
    print(f"❌ Error running agent: {e}")
    print("This might be due to missing API keys or network issues") 