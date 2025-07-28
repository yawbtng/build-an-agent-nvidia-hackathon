import os
import requests
import json

# Load environment variables from secrets.env
def load_env_vars():
    """Load environment variables from secrets.env file."""
    try:
        with open('../secrets.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
        print("✅ Loaded environment variables from secrets.env")
    except Exception as e:
        print(f"⚠️  Could not load secrets.env: {e}")

# Load environment variables at startup
load_env_vars()

def test_nvidia_api():
    """Test NVIDIA API connection."""
    try:
        # Check if NVIDIA API key is available
        api_key = os.getenv('NVIDIA_API_KEY')
        if not api_key:
            print("⚠️  No NVIDIA API key found.")
            return
        
        print(f"🔑 API Key found: {api_key[:10]}...")
        
        # Test different endpoints
        endpoints = [
            "https://api.nvcf.nvidia.com/v2/chat/completions",
            "https://api.nvcf.nvidia.com/v1/chat/completions",
            "https://api.nvcf.nvidia.com/chat/completions"
        ]
        
        models = [
            "nvidia/llama-3_3-nemotron-super-49b-v1",
            "nvidia/llama-3-3-nemotron-super-49b-v1",
            "nvidia/llama3-70b-instruct",
            "nvidia/llama-3-70b-instruct"
        ]
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        for endpoint in endpoints:
            print(f"\n🔍 Testing endpoint: {endpoint}")
            
            for model in models:
                print(f"  Testing model: {model}")
                
                data = {
                    "messages": [
                        {"role": "user", "content": "Hello, this is a test. Please respond with 'Test successful'."}
                    ],
                    "model": model,
                    "max_tokens": 50,
                    "temperature": 0.7
                }
                
                try:
                    response = requests.post(endpoint, headers=headers, json=data, timeout=30)
                    print(f"    Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"    ✅ Success! Response: {result}")
                        return endpoint, model
                    else:
                        print(f"    ❌ Error: {response.text}")
                        
                except Exception as e:
                    print(f"    ❌ Exception: {e}")
        
        print("\n❌ No working endpoint/model combination found")
        
    except Exception as e:
        print(f"⚠️  Test failed: {e}")

if __name__ == "__main__":
    test_nvidia_api() 