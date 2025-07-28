import os
import sys
from dotenv import load_dotenv

# Add the code directory to the Python path
sys.path.append('code')

# Load environment variables
load_dotenv("variables.env")
load_dotenv("secrets.env")

print("=== Simple Agent Test ===")

# Test 1: Check if we can import the modules
try:
    from docgen_agent import AgentState, graph
    print("✅ Successfully imported AgentState and graph")
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)

# Test 2: Check if we can create an AgentState
try:
    state = AgentState(
        topic="Test topic",
        report_structure="Simple test structure"
    )
    print("✅ Successfully created AgentState")
except Exception as e:
    print(f"❌ Error creating AgentState: {e}")
    exit(1)

# Test 3: Check if the graph exists
try:
    print(f"✅ Graph has {len(graph.nodes)} nodes")
    print(f"✅ Graph nodes: {list(graph.nodes.keys())}")
except Exception as e:
    print(f"❌ Error checking graph: {e}")
    exit(1)

print("\n=== Environment Check ===")
print(f"NVIDIA_API_KEY: {'✅ Set' if os.getenv('NVIDIA_API_KEY') else '❌ Missing'}")
print(f"TAVILY_API_KEY: {'✅ Set' if os.getenv('TAVILY_API_KEY') else '❌ Missing'}")

print("\n✅ All basic tests passed! The agent should be ready to use.")
print("\nTo run the agent, you can:")
print("1. Use the Jupyter notebooks in the code/ folder")
print("2. Run: python -m code.docgen_agent")
print("3. Or use the agent_client.ipynb notebook") 