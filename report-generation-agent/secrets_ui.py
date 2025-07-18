"""
Simple secrets management UI for Jupyter notebooks
"""
import os
from IPython.display import HTML, display
import ipywidgets as widgets
from cryptography.fernet import Fernet
import json
import base64

class SecretsManager:
    def __init__(self):
        self.secrets_file = '.workshop_secrets.json'
        self.key_file = '.workshop_key'
        
    def _get_or_create_key(self):
        """Get or create encryption key"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        return key
    
    def _encrypt_value(self, value):
        """Encrypt a secret value"""
        key = self._get_or_create_key()
        f = Fernet(key)
        return f.encrypt(value.encode()).decode()
    
    def _decrypt_value(self, encrypted_value):
        """Decrypt a secret value"""
        try:
            key = self._get_or_create_key()
            f = Fernet(key)
            return f.decrypt(encrypted_value.encode()).decode()
        except:
            return ""
    
    def save_secret(self, name, value):
        """Save an encrypted secret"""
        # Load existing secrets
        secrets = {}
        if os.path.exists(self.secrets_file):
            try:
                with open(self.secrets_file, 'r') as f:
                    secrets = json.load(f)
            except:
                secrets = {}
        
        # Encrypt and save new secret
        secrets[name] = self._encrypt_value(value)
        
        with open(self.secrets_file, 'w') as f:
            json.dump(secrets, f)
        
        # Also save to environment for immediate use
        os.environ[name] = value
        
        print(f"✅ Saved {name} securely!")
    
    def get_secret(self, name):
        """Get a decrypted secret"""
        if os.path.exists(self.secrets_file):
            try:
                with open(self.secrets_file, 'r') as f:
                    secrets = json.load(f)
                if name in secrets:
                    return self._decrypt_value(secrets[name])
            except:
                pass
        return os.environ.get(name, "")
    
    def create_ui(self):
        """Create the secrets management UI"""
        # Create widgets
        title = widgets.HTML("<h3>🔑 Workshop Secrets Manager</h3>")
        
        # NGC API Key input
        ngc_label = widgets.HTML("<b>NGC API Key:</b>")
        ngc_input = widgets.Password(
            placeholder="Enter your NGC API key",
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='400px')
        )
        ngc_button = widgets.Button(
            description="Save NGC Key",
            button_style='primary',
            layout=widgets.Layout(width='120px')
        )
        
        # OpenAI API Key input  
        openai_label = widgets.HTML("<b>OpenAI API Key:</b>")
        openai_input = widgets.Password(
            placeholder="Enter your OpenAI API key",
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='400px')
        )
        openai_button = widgets.Button(
            description="Save OpenAI Key",
            button_style='primary', 
            layout=widgets.Layout(width='120px')
        )
        
        # Status display
        status = widgets.HTML("")
        
        # Load existing values
        ngc_input.value = self.get_secret('NGC_API_KEY')
        openai_input.value = self.get_secret('OPENAI_API_KEY')
        
        # Event handlers
        def save_ngc(b):
            if ngc_input.value.strip():
                self.save_secret('NGC_API_KEY', ngc_input.value.strip())
                status.value = "<p style='color: green'>✅ NGC API Key saved!</p>"
            else:
                status.value = "<p style='color: red'>❌ Please enter a valid NGC API key</p>"
        
        def save_openai(b):
            if openai_input.value.strip():
                self.save_secret('OPENAI_API_KEY', openai_input.value.strip())
                status.value = "<p style='color: green'>✅ OpenAI API Key saved!</p>"
            else:
                status.value = "<p style='color: red'>❌ Please enter a valid OpenAI API key</p>"
        
        # Connect event handlers
        ngc_button.on_click(save_ngc)
        openai_button.on_click(save_openai)
        
        # Layout
        ngc_row = widgets.HBox([ngc_input, ngc_button])
        openai_row = widgets.HBox([openai_input, openai_button])
        
        ui = widgets.VBox([
            title,
            ngc_label,
            ngc_row,
            widgets.HTML("<br>"),
            openai_label, 
            openai_row,
            widgets.HTML("<br>"),
            status
        ])
        
        return ui

# Convenience function for students
def show_secrets_manager():
    """Display the secrets management interface"""
    manager = SecretsManager()
    return manager.create_ui()

# Function to load secrets into environment
def load_secrets():
    """Load saved secrets into environment variables"""
    manager = SecretsManager()
    
    # Load all common secrets
    secrets = ['NGC_API_KEY', 'OPENAI_API_KEY']
    loaded = []
    
    for secret in secrets:
        value = manager.get_secret(secret)
        if value:
            os.environ[secret] = value
            loaded.append(secret)
    
    if loaded:
        print(f"✅ Loaded secrets: {', '.join(loaded)}")
    else:
        print("ℹ️ No secrets found. Use show_secrets_manager() to add some!") 