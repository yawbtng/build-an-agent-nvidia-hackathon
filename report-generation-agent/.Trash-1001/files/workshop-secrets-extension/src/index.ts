import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICommandPalette } from '@jupyterlab/apputils';

import { Widget } from '@lumino/widgets';

/**
 * The plugin registration information.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'workshop-secrets-extension:plugin',
  description: 'Demo showing proper secrets manager integration',
  autoStart: true,
  requires: [ICommandPalette],
  optional: [],
  activate: activateExtension
};

/**
 * A widget that demonstrates proper secrets manager usage
 */
class SecretsWidget extends Widget {
  private secretsManager: any;

  constructor(app: JupyterFrontEnd) {
    super();
    this.addClass('jp-secrets-widget');
    this.title.label = 'Workshop Secrets Demo';
    this.title.closable = true;
    
    // This is the KEY part - accessing the secrets manager service
    // This is what students would need to understand!
    try {
      this.secretsManager = app.serviceManager.get('secrets-manager');
      this.setupWidget();
    } catch (error) {
      console.error('Failed to get secrets manager:', error);
      this.setupErrorWidget();
    }
  }

  private setupWidget(): void {
    this.node.innerHTML = `
      <div style="padding: 20px;">
        <h3>🔑 Workshop API Keys (Proper Integration)</h3>
        <p>This demonstrates the CORRECT way to use jupyter-secrets-manager</p>
        
        <div style="margin: 20px 0;">
          <label for="ngc-key">NGC API Key:</label><br>
          <input type="password" id="ngc-key" 
                 style="width: 400px; padding: 8px; margin: 5px 0;" 
                 placeholder="Enter your NGC API key">
          <button onclick="window.attachNGCSecret()" 
                  style="margin-left: 10px; padding: 8px 16px;">
            🔗 Attach to Secrets
          </button>
        </div>

        <div style="margin: 20px 0;">
          <label for="openai-key">OpenAI API Key:</label><br>
          <input type="password" id="openai-key" 
                 style="width: 400px; padding: 8px; margin: 5px 0;" 
                 placeholder="Enter your OpenAI API key">
          <button onclick="window.attachOpenAISecret()" 
                  style="margin-left: 10px; padding: 8px 16px;">
            🔗 Attach to Secrets
          </button>
        </div>

        <div style="margin: 20px 0;">
          <button onclick="window.testSecrets()" 
                  style="background: #0066cc; color: white; padding: 10px 20px; border: none; border-radius: 4px;">
            🧪 Test Secrets Manager
          </button>
        </div>

        <div id="status" style="margin-top: 20px; padding: 10px; background: #f5f5f5; border-radius: 4px;">
          Ready to attach secrets...
        </div>
      </div>
    `;

    // This is where the REAL complexity lies - proper secret attachment
    this.setupSecretAttachment();
  }

  private setupErrorWidget(): void {
    this.node.innerHTML = `
      <div style="padding: 20px;">
        <h3>❌ Secrets Manager Not Available</h3>
        <p>The jupyter-secrets-manager extension is not properly loaded.</p>
        <p>This demonstrates why this approach is complex for students!</p>
      </div>
    `;
  }

  private setupSecretAttachment(): void {
    const self = this;
    
    // Expose functions to global window for button clicks
    // (This is a hack for demo purposes - real extensions wouldn't do this)
    (window as any).attachNGCSecret = () => {
      self.attachSecret('ngc-key', 'workshop', 'ngc-api-key');
    };

    (window as any).attachOpenAISecret = () => {
      self.attachSecret('openai-key', 'workshop', 'openai-api-key');
    };

    (window as any).testSecrets = () => {
      self.testSecretsManager();
    };
  }

  /**
   * This is the core method - how to properly attach a secret
   * This is what students would need to implement!
   */
  private attachSecret(inputId: string, namespace: string, secretId: string): void {
    const input = this.node.querySelector(`#${inputId}`) as HTMLInputElement;
    const status = this.node.querySelector('#status') as HTMLDivElement;

    if (!input) {
      status.innerHTML = `❌ Input ${inputId} not found`;
      return;
    }

    if (!this.secretsManager) {
      status.innerHTML = `❌ Secrets manager not available`;
      return;
    }

    try {
      // THIS IS THE KEY LINE - the proper way to attach secrets
      // This is what the README talks about but students would need to figure out
      this.secretsManager.attach(input, namespace, secretId);
      
      status.innerHTML = `✅ Attached ${inputId} to secrets manager (namespace: ${namespace}, id: ${secretId})`;
      
      // Listen for changes to save secrets
      input.addEventListener('input', () => {
        status.innerHTML = `💾 Saving secret for ${secretId}...`;
      });
      
    } catch (error) {
      status.innerHTML = `❌ Failed to attach secret: ${error}`;
      console.error('Secret attachment error:', error);
    }
  }

  private testSecretsManager(): void {
    const status = this.node.querySelector('#status') as HTMLDivElement;
    
    if (!this.secretsManager) {
      status.innerHTML = `❌ Secrets manager not available`;
      return;
    }

    try {
      // Test fetching a secret
      this.secretsManager.get('workshop', 'ngc-api-key').then((secret: any) => {
        if (secret) {
          status.innerHTML = `✅ Successfully retrieved NGC secret: ${secret.substring(0, 10)}...`;
        } else {
          status.innerHTML = `ℹ️ No NGC secret stored yet`;
        }
      }).catch((error: any) => {
        status.innerHTML = `❌ Error retrieving secret: ${error}`;
      });
    } catch (error) {
      status.innerHTML = `❌ Error testing secrets: ${error}`;
    }
  }
}

/**
 * Activate the extension.
 */
function activateExtension(
  app: JupyterFrontEnd,
  palette: ICommandPalette
): void {
  console.log('JupyterLab extension workshop-secrets-extension is activated!');

  // Create a command to open our secrets widget
  const command = 'workshop-secrets:open';
  app.commands.addCommand(command, {
    label: 'Open Workshop Secrets Demo',
    execute: () => {
      const widget = new SecretsWidget(app);
      app.shell.add(widget, 'main');
    }
  });

  // Add the command to the palette
  palette.addItem({ command, category: 'Workshop Demo' });
}

/**
 * Export the plugin as default.
 */
export default plugin; 