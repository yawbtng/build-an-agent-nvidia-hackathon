"""
Simple API Key Input Form using ipywidgets
"""
import ipywidgets as widgets
from IPython.display import display, clear_output
import os

class SimpleAPIForm:
    def __init__(self):
        # Create input widgets
        self.ngc_key = widgets.Password(
            placeholder='Enter your NGC API Key',
            description='NGC API:',
            style={'description_width': 'initial'}
        )
        
        self.openai_key = widgets.Password(
            placeholder='Enter your OpenAI API Key', 
            description='OpenAI API:',
            style={'description_width': 'initial'}
        )
        
        # Create save button
        self.save_button = widgets.Button(
            description='Save',
            button_style='success',
            icon='check'
        )
        
        # Create status output
        self.status = widgets.Output()
        
        # Set up button click handler
        self.save_button.on_click(self.save_keys)
        
    def save_keys(self, b):
        """Save the API keys to environment variables"""
        with self.status:
            clear_output()
            
            # Set environment variables
            if self.ngc_key.value:
                os.environ['NGC_API_KEY'] = self.ngc_key.value
                print("✅ NGC API Key saved")
            
            if self.openai_key.value:
                os.environ['OPENAI_API_KEY'] = self.openai_key.value
                print("✅ OpenAI API Key saved")
            
            # Also save to /project/secrets.env file for persistence (matches variables.env format)
            from datetime import datetime
            secrets_content = [
                "# Workshop secrets - saved by API key form",
                f"# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                ""
            ]
            
            if self.ngc_key.value:
                secrets_content.append(f'NGC_API_KEY={self.ngc_key.value}')
            if self.openai_key.value:
                secrets_content.append(f'OPENAI_API_KEY={self.openai_key.value}')
            
            if len(secrets_content) > 3:  # More than just comments
                with open('/project/secrets.env', 'w') as f:
                    f.write('\n'.join(secrets_content) + '\n')
            
            print("✅ Keys saved to /project/secrets.env")
            print("🚀 Ready to build AI agents!")
    
    def show(self):
        """Display the form"""
        # Create title
        title = widgets.HTML(value="<h2>🔑 Workshop API Keys Setup</h2>")
        
        # Create form layout
        form = widgets.VBox([
            title,
            self.ngc_key,
            self.openai_key,
            self.save_button,
            self.status
        ])
        
        display(form)

# Function to show the form easily
def show_api_form():
    """Show the API key input form"""
    form = SimpleAPIForm()
    form.show()
    return form 