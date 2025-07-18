# 🔑 Secrets Management for AI Agents

<img src="_static/robots/spyglass.png" alt="Secrets Management Robot" style="float:left; max-width:300px;margin:25px;" />

<h1 style="color:#6cb800; font-size:2.5em; margin-bottom:0.2em;">Secure API Key Management</h1>

<div style="font-size:1.2em; line-height:1.6;">

## Overview

Before building AI agents, you need to securely configure your API keys. Your API keys are the credentials that allow your agents to access powerful language models and other services. Keeping them secure is essential!

---

<img src="_static/robots/strong.png" alt="Security Features" style="float:right; max-width:280px; margin:20px 0 20px 30px; border-radius:12px; box-shadow:0 2px 8px #ccc;" />

## Required API Keys

For this workshop, you'll need:

### 🎯 **NGC API Key** *(Required)*
- Access to NVIDIA's model catalog
- Powers the main workshop content
- Free tier available
- **Get yours at:** [build.nvidia.com](https://build.nvidia.com)

### 🤖 **OpenAI API Key** *(Optional)*
- Access to OpenAI models
- Useful for comparisons
- Pay-per-use pricing
- **Get yours at:** [platform.openai.com](https://platform.openai.com)

### 🔧 **Set Up Your Keys**
Once you have your API keys, use our interactive dashboard to configure them securely:

<a style="cursor: pointer;" onclick="openOrCreateFileInJupyterLab('report-generation-agent/voila_api_dashboard.ipynb');"><i class="fas fa-key"></i> **Configure API Keys Dashboard**</a>

- Interactive web interface
- Real-time status validation
- Secure environment variable storage

---

<img src="_static/robots/startup.png" alt="Security Best Practices" style="float:left; max-width:260px; margin:20px 30px 20px 0; border-radius:12px; box-shadow:0 2px 8px #ccc;" />

## Security Best Practices

### ✅ **Do:**
- Use environment variables for key storage
- Never commit API keys to version control
- Rotate keys regularly
- Use different keys for development vs production

### ❌ **Don't:**
- Hardcode keys in your notebooks
- Share keys in chat or email
- Use production keys for testing
- Store keys in plain text files

### 🔒 **Workshop Security Features:**
- Automatic environment variable loading
- Encrypted storage options
- Session-based key management
- Secure key validation

---

## Troubleshooting

<img src="_static/robots/wave.png" alt="Need Help?" style="float:right; max-width:250px; margin:20px 0 20px 30px; border-radius:12px; box-shadow:0 2px 8px #ccc;" />

### Common Issues:

**"API key not found"**
- Restart your notebook kernel after setting keys
- Check that environment variables are properly set
- Verify key format (no extra spaces)

**"Invalid API key"**
- Double-check your key from the provider
- Ensure key has proper permissions
- Try regenerating the key

**"Keys not persisting"**
- Use the provided setup scripts
- Check `.env` file creation
- Verify postBuild.bash execution

### Need More Help?
- Each method includes detailed instructions
- Look for 💡 **HELP** sections in notebooks
- Check the troubleshooting section in our support resources

---

## Next Steps

Once your API keys are configured:

1. **Verify Setup** - Run the test cells in your chosen notebook
2. **Start Building** - Jump into the main agent workshop
3. **Explore Advanced Features** - Try the interactive dashboard

<div style="text-align: center; margin-top: 40px;">
<img src="_static/robots/party.png" alt="Ready to Build!" style="max-width:200px; border-radius:12px; box-shadow:0 2px 8px #ccc;" />
<p><strong>Ready to build amazing AI agents! 🚀</strong></p>
</div>

</div> 