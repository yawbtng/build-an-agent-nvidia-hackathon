#!/bin/bash

# Workshop post-build script
# This script runs after the container is built to set up environment variable loading

echo "🔧 Setting up automatic environment variable loading..."

# Create the load-vars.sh script in /etc/profile.d/
# This will automatically source both variables.env and secrets.env for all sessions
sudo tee /etc/profile.d/load-vars.sh > /dev/null << 'EOF'
#!/bin/bash

# Automatically load workshop environment variables
# This script runs for every shell session

set -o allexport

# Load base variables if they exist
if [ -f /project/variables.env ]; then
    source /project/variables.env
fi

# Load user secrets if they exist  
if [ -f /project/secrets.env ]; then
    source /project/secrets.env
fi

set +o allexport
EOF

# Make the script executable
sudo chmod +x /etc/profile.d/load-vars.sh

echo "✅ Environment variable auto-loading configured!"
echo "📁 Files will be sourced:"
echo "   - /project/variables.env (workshop defaults)"
echo "   - /project/secrets.env (user API keys)"
echo ""
echo "🚀 Students can now access API keys with os.getenv('NGC_API_KEY') immediately!"

