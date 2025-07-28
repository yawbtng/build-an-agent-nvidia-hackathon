import os
import sys
from dotenv import load_dotenv

# Add the code directory to the Python path
sys.path.append('code')

# Load environment variables
load_dotenv("variables.env")
load_dotenv("secrets.env")

print("=== Quick Agent Test ===")

try:
    from docgen_agent import write_report
    
    # Use a simpler topic and structure for faster testing
    result = write_report(
        topic="Benefits of Python programming language",
        report_structure="""This report should be brief and focused.
        The report structure should include:
        1. Introduction (2-3 sentences)
        2. Main Body: One section about key benefits
        3. Conclusion (2-3 sentences)"""
    )
    
    if result and result.get("report"):
        print("✅ Agent completed successfully!")
        print(f"Report length: {len(result['report'])} characters")
        print("\n=== Generated Report ===")
        print(result["report"])
    else:
        print("❌ Agent ran but returned no report")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("This might be due to API rate limits or network issues") 