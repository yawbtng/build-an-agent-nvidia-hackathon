# 🔍 Testing Jupyter Secrets Manager Extension

> **🎯 Goal**: Hands-on evaluation of the jupyter-secrets-manager extension to see if it's useful for managing NGC_API_KEY and other secrets in our workshop.

## 📋 How the Extension Works

### Core Concept
The extension provides **two main components**:

1. **SecretsManager**: The interface that extensions/users interact with
2. **SecretsConnector**: The backend that actually stores/retrieves secrets

### Key Features
- **Auto-fill inputs** with stored secrets based on namespace/ID
- **Auto-save secrets** when users type in connected inputs  
- **Session-based storage** (by default - secrets lost when Jupyter restarts)
- **Extensible architecture** (can be extended with custom connectors)

---

## 🚀 Step-by-Step Testing Guide

### Step 1: Install the Extension

```bash
# Install the extension
pip install jupyter_secrets_manager

# Restart JupyterLab completely
# (Close all browser tabs and restart jupyter lab)
```

### Step 2: Verify Installation

```bash
# Check if extension is installed
jupyter labextension list | grep secrets

# Should see something like:
# jupyter-secrets-manager v0.4.0 enabled OK
```

### Step 3: Create a Test Notebook

Create a new notebook with this test code:

```python
# Cell 1: Test basic functionality
import ipywidgets as widgets
from IPython.display import display

# Create input widgets that could be connected to secrets
api_key_input = widgets.Text(
    placeholder="Enter your NGC API Key",
    description="NGC API Key:",
    style={'description_width': 'initial'}
)

openai_key_input = widgets.Text(
    placeholder="Enter your OpenAI API Key", 
    description="OpenAI Key:",
    style={'description_width': 'initial'}
)

display(api_key_input)
display(openai_key_input)
```

```python
# Cell 2: Try to access the secrets manager
# Note: This will likely require JavaScript interaction
from IPython.display import Javascript

# This is where we'd normally attach inputs to secrets
# The extension works through JavaScript APIs
Javascript("""
console.log("Testing if secrets manager is available");
// Check if the extension loaded properly
if (window.jupyter_secrets_manager) {
    console.log("Secrets manager found!");
} else {
    console.log("Secrets manager not found - extension might not be loaded");
}
""")
```

### Step 4: Test Manual JavaScript Integration

Since the extension works primarily through JavaScript APIs, let's test it directly:

```python
# Cell 3: JavaScript test of the extension
from IPython.display import Javascript, HTML

# Create HTML inputs and try to connect them to secrets
HTML("""
<div>
    <label for="ngc-key">NGC API Key:</label>
    <input type="password" id="ngc-key" placeholder="Your NGC API Key">
    <br><br>
    <label for="openai-key">OpenAI API Key:</label>
    <input type="password" id="openai-key" placeholder="Your OpenAI API Key">
    <br><br>
    <button onclick="testSecretsManager()">Test Secrets Manager</button>
    <div id="output"></div>
</div>

<script>
function testSecretsManager() {
    const output = document.getElementById('output');
    
    // Try to access the secrets manager
    if (typeof window.jupyterlab !== 'undefined' && window.jupyterlab.shell) {
        output.innerHTML = '<p style="color: green;">✅ JupyterLab context available</p>';
        
        // Look for secrets manager in the app
        const app = window.jupyterlab;
        console.log("Available services:", Object.keys(app.serviceManager || {}));
        
        // Try to find secrets manager
        try {
            // This is how we'd typically access the extension
            const secretsManager = app.serviceManager?.get('secrets-manager');
            if (secretsManager) {
                output.innerHTML += '<p style="color: green;">✅ Secrets manager found!</p>';
                
                // Try to attach an input
                const ngcInput = document.getElementById('ngc-key');
                if (ngcInput) {
                    // Attempt to attach (this might fail - extension is experimental)
                    output.innerHTML += '<p style="color: blue;">🔗 Attempting to attach NGC key input...</p>';
                }
            } else {
                output.innerHTML += '<p style="color: orange;">⚠️ Secrets manager not found in services</p>';
            }
        } catch (error) {
            output.innerHTML += `<p style="color: red;">❌ Error: ${error.message}</p>`;
        }
    } else {
        output.innerHTML = '<p style="color: red;">❌ JupyterLab context not available</p>';
    }
}
</script>
""")
```

---

## 🧪 Practical Testing Scenarios

### Test Scenario 1: Basic Functionality

1. **Run the test notebook** above
2. **Type values** into the input fields
3. **Restart the notebook** (Kernel → Restart)
4. **Check if values persist** (they probably won't with default in-memory storage)

### Test Scenario 2: Extension API Access

1. **Open browser developer tools** (F12)
2. **Go to Console tab**
3. **Type**:
   ```javascript
   // Check if extension is loaded
   console.log("Available extensions:", Object.keys(window.jupyterlab?.shell?._widgets || {}));
   
   // Look for secrets manager
   window.jupyterlab?.serviceManager?.secrets
   ```

### Test Scenario 3: Real-World Usage

Create a notebook that simulates your workshop scenario:

```python
# Workshop simulation notebook
import os
from IPython.display import HTML

# Create the kind of inputs students would use
HTML("""
<h3>🔑 API Key Setup for Creative Agent</h3>

<div style="margin: 20px 0;">
    <label for="ngc-api-key" style="display: block; margin-bottom: 5px;">NGC API Key:</label>
    <input type="password" id="ngc-api-key" 
           style="width: 400px; padding: 8px;" 
           placeholder="Enter your NGC API key here">
    <small style="display: block; color: #666; margin-top: 5px;">
        This will be used for NVIDIA model access
    </small>
</div>

<div style="margin: 20px 0;">
    <label for="openai-api-key" style="display: block; margin-bottom: 5px;">OpenAI API Key:</label>
    <input type="password" id="openai-api-key" 
           style="width: 400px; padding: 8px;" 
           placeholder="Enter your OpenAI API key here">
    <small style="display: block; color: #666; margin-top: 5px;">
        This will be used for GPT model access
    </small>
</div>

<button onclick="saveKeysToEnvironment()" 
        style="background: #0066cc; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;">
    💾 Save Keys
</button>

<div id="key-status" style="margin-top: 20px;"></div>

<script>
function saveKeysToEnvironment() {
    const ngcKey = document.getElementById('ngc-api-key').value;
    const openaiKey = document.getElementById('openai-api-key').value;
    const status = document.getElementById('key-status');
    
    if (ngcKey || openaiKey) {
        // In a real scenario, this would save to secrets manager
        status.innerHTML = `
            <div style="background: #d4edda; padding: 10px; border-radius: 4px; color: #155724;">
                ✅ Keys saved! (In real extension, these would be securely stored)
                <br>NGC Key: ${ngcKey ? '***hidden***' : 'not provided'}
                <br>OpenAI Key: ${openaiKey ? '***hidden***' : 'not provided'}
            </div>
        `;
        
        // Try to set environment variables (this is what the extension should do)
        window.localStorage.setItem('test_ngc_key', ngcKey);
        window.localStorage.setItem('test_openai_key', openaiKey);
    } else {
        status.innerHTML = `
            <div style="background: #f8d7da; padding: 10px; border-radius: 4px; color: #721c24;">
                ⚠️ Please enter at least one API key
            </div>
        `;
    }
}
</script>
""")
```

---

## 📊 What to Look For While Testing

### ✅ **Positive Signs**
- Extension appears in `jupyter labextension list`
- No errors in browser console when loading JupyterLab
- JavaScript can access secrets manager APIs
- Inputs can be attached to secrets successfully
- Values persist between notebook sessions

### ⚠️ **Warning Signs**
- Console errors about missing dependencies
- Extension fails to load properly
- APIs are undefined or throw errors
- Secrets don't persist as expected
- Conflicts with other extensions

### ❌ **Deal Breakers**
- Extension breaks JupyterLab functionality
- Frequent crashes or errors
- Unable to attach inputs to secrets
- No clear documentation for implementation
- Too complex for workshop timeframe

---

## 🤔 Evaluation Questions

After testing, ask yourself:

1. **Ease of Use**: Would college students find this intuitive?
2. **Reliability**: Does it work consistently without errors?
3. **Value Add**: Does it significantly improve the workshop experience?
4. **Time Cost**: How much workshop time would be spent explaining this vs. building agents?
5. **Maintenance**: Would this create support overhead during the workshop?

---

## 🚀 Quick Start Testing Commands

```bash
# Complete test sequence
pip install jupyter_secrets_manager
jupyter lab --version
jupyter labextension list | grep secrets
jupyter lab

# In JupyterLab, create new notebook and run the test code above
```

---

## 📝 My Hypothesis

**Likely outcome**: The extension will show promise but feel **too experimental** for a college workshop focused on creativity. The basic `variables.env` approach will probably feel more reliable and educational.

**Best case**: It works smoothly and provides a professional secrets management experience.

**Worst case**: It has bugs, complex setup, or interferes with the core workshop goals.

---

Let me know what you discover when you test it! I'm curious to see if my assessment holds up against real-world testing. 