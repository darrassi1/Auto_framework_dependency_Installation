# Auto_framework_dependency_Installation
### Project Description

This repository contains a comprehensive framework for managing and installing various development tools and frameworks, as well as executing commands and handling missing dependencies. Key features include:

1. **Installation Functions**:
    - Functions to install popular frameworks and tools like Angular CLI, React, Next.js, Vue.js, Symfony, Laravel, Django, and Flutter.
    - Example commands to automate these installations.

2. **Utility Functions**:
    - Check if a tool or command is installed.
    - Install missing Python packages.
    - Find available ports.
    - Monitor and manage running processes.
    - Install Composer.
    - Handle and resolve missing dependencies.

3. **Command Execution**:
    - Execute and monitor commands, including starting servers for different frameworks.
    - Handle termination of processes.
    - Handle missing dependencies by attempting to install them and retrying the original command.

4. **Integration with IPython**:
    - Utilize IPython for enhanced interactive computing.

5. **Svelte Component for Jupyter Notebook Execution**:
    - Svelte component to execute Jupyter notebook code via an API, transforming the output to HTML and displaying it in a responsive, scrollable design.

### Key Files

- **installation_functions.py**: Contains functions for installing various development tools and frameworks.
- **utilities.py**: Contains utility functions for checking tool installations, handling processes, and managing dependencies.
- **command_execution.py**: Functions for executing commands, handling server processes, and managing missing dependencies.
- **Svelte Component**:
  - `NotebookExecutor.svelte`: A Svelte component for executing Jupyter notebook commands and displaying the output.

### Example Usage

- **Installing Angular CLI**:
    ```python
    install_angular_cli()
    ```

- **Executing a Command and Running a Server**:
    ```python
    command = "npx create-react-app my-react-app"
    execute_command(command)
    command_server = "npm start"
    folder = "my-react-app"
    execute_command(command_server,folder)
    ```

- **Handling Missing Dependencies**:
    ```python
    error_message = "Cannot find module 'express'"
    original_command = "npm start"
    handle_missing_dependency(error_message, original_command)
    ```
- **API Configuration**:
    ```javascript
    const getApiBaseUrl = () => {
      if (typeof window !== 'undefined') {
        const host = window.location.hostname;
        if (host === 'localhost' || host === '127.0.0.1') {
          return 'http://127.0.0.1:1337';
        } else {
          return `http://${host}:1337`;
        }
      } else {
        return 'http://127.0.0.1:1337';
      }
    };

    export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || getApiBaseUrl();
    export const socket = io(API_BASE_URL);

    export async function executeNotebookapi(userInput) {
      console.log('Executing notebook with input:', userInput);
      const projectName = localStorage.getItem("selectedProject");
      const response = await fetch(`${API_BASE_URL}/executenotebook`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ input: userInput, project_name: projectName })
      });

      if (response.ok) {
          const data = await response.json();
          console.log('Received response:', data);
          return data.html;
      } else {
          console.error('Failed to execute notebook');
          return '';
      }
    }
    ```

- **Using the Svelte Component**:
    ```svelte
    <script>
      import { onMount } from 'svelte';
      import { executeNotebookapi } from "../api.js";

      let userInput = '';
      let htmlOutput = '';

      async function executeNotebook() {
        htmlOutput = await executeNotebookapi(userInput);
      }
    </script>

    <main>
      <div class="input-section">
        <textarea bind:value={userInput} placeholder="Enter your code here..."></textarea>
        <button on:click={executeNotebook}>Execute</button>
      </div>
      <div class="output-section">
        <div class="output">
          {@html htmlOutput}
        </div>
      </div>
    </main>
    ```

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/darrassi1/Auto_framework_dependency_Installation.git
    cd Auto_framework_dependency_Installation
    ```

2. **Install required dependencies** (if any, like `npm`, `composer`, `flutter`, etc.).

3. **Run example commands** to test the functionality.

### Contribution

Feel free to contribute by submitting issues or pull requests. Ensure your code follows the existing structure and includes relevant documentation.

### License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
