import os
from dotenv import load_dotenv

# Load the environment files
load_dotenv("variables.env")
load_dotenv("secrets.env")

# Check if the keys are loaded
print("=== Environment Variable Check ===")
print(f"NVIDIA_API_KEY: {'✅ Set' if os.getenv('NVIDIA_API_KEY') else '❌ Missing'}")
print(f"TAVILY_API_KEY: {'✅ Set' if os.getenv('TAVILY_API_KEY') else '❌ Missing'}")
print(f"LANGSMITH_API_KEY: {'✅ Set' if os.getenv('LANGSMITH_API_KEY') else '❌ Optional'}")

# Show the actual values (be careful with this in production)
nvidia_key = os.getenv('NVIDIA_API_KEY')
tavily_key = os.getenv('TAVILY_API_KEY')

if nvidia_key:
    print(f"NVIDIA key starts with: {nvidia_key[:10]}...")
if tavily_key:
    print(f"Tavily key starts with: {tavily_key[:10]}...")

print("\n=== File Check ===")
print(f"variables.env exists: {'✅ Yes' if os.path.exists('variables.env') else '❌ No'}")
print(f"secrets.env exists: {'✅ Yes' if os.path.exists('secrets.env') else '❌ No'}")

if os.path.exists('secrets.env'):
    print("\n=== Secrets.env content (first few lines) ===")
    with open('secrets.env', 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines[:5]):
            if line.strip() and not line.strip().startswith('#'):
                # Show key name but mask the value
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    masked_value = value[:4] + '...' if len(value) > 4 else '***'
                    print(f"{key}={masked_value}")
                else:
                    print(f"Line {i+1}: {line.strip()}") 