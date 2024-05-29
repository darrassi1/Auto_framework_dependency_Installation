import re
import signal
import subprocess
import sys
import os
import time
import socket
import threading
import psutil
from IPython import get_ipython

# Function declarations

# Store server processes
running_servers = {}


# Installation functions for various frameworks and tools
def install_angular_cli():
    try:
        subprocess.run(["npm", "install", "-g", "@angular/cli"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Angular CLI: {e}")


def install_react():
    try:
        subprocess.run(["npx", "create-react-app", "my-react-app"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to create React app: {e}")


def install_nextjs():
    try:
        subprocess.run(["npx", "create-next-app", "my-nextjs-app"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to create Next.js app: {e}")


def install_vuejs():
    try:
        subprocess.run(["npm", "install", "-g", "@vue/cli"], check=True)
        subprocess.run(["vue", "create", "my-vue-app"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to create Vue.js app: {e}")


def install_symfony():
    try:
        subprocess.run(["composer", "create-project", "symfony/skeleton", "my-symfony-app"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to create Symfony app: {e}")


def install_laravel():
    try:
        subprocess.run(["composer", "create-project", "--prefer-dist", "laravel/laravel", "my-laravel-app"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to create Laravel app: {e}")


# Function to install missing Python packages
def install_missing_package(package_name):
    try:
        subprocess.run(["pip", "install", package_name], check=True)
        print(f"Installed missing Python package: {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install package {package_name}: {e}")


def install_flutter():
    try:
        subprocess.run(["flutter", "create", "my-flutter-app"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to create Flutter app: {e}")


def install_django():
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "django"], check=True)
        print("Installed Django successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Django: {e}")


# Example mapping of commands to installation functions
# Example mapping of commands to installation functions
installation_functions = {
    "ng": install_angular_cli,
    "npx create-react-app": install_react,
    "npx create-next-app": install_nextjs,
    "vue": install_vuejs,
    "composer create-project symfony/skeleton": install_symfony,
    "composer create-project --prefer-dist laravel/laravel": install_laravel,
    "flutter create": install_flutter,
    "pip install django": install_django
}


# Utility functions
# Function to check if a tool or command is installed
def is_tool_installed(tool_name, check_command=None):
    try:
        if check_command:
            subprocess.run(check_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            subprocess.run([tool_name, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


# Function to install Composer
def install_composer():
    try:
        subprocess.run(["php", "-r", "copy('https://getcomposer.org/installer', 'composer-setup.php');"], check=True)
        subprocess.run(["php", "composer-setup.php"], check=True)
        subprocess.run(["php", "-r", "unlink('composer-setup.php');"], check=True)
        subprocess.run(["mv", "composer.phar", "/usr/local/bin/composer"], check=True)
        print("Composer installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Composer: {e}")


def print_output(process):
    try:
        for line in process.stdout.splitlines():
            if line:
                print(line.strip())
        for line in process.stderr.splitlines():
            if line:
                print(line.strip())
    except Exception as e:
        print(f"Error reading output: {e}")


def monitor_process(process, pid, server_url):
    try:
        while True:
            time.sleep(1)
            return_code = process.poll()
            if return_code is not None:
                if return_code == 0:
                    print(f"Process with PID {pid} exited successfully.")
                else:
                    print(f"Process with PID {pid} terminated with return code {return_code}")
                if server_url in running_servers:
                    del running_servers[server_url]
                    print(f"Server at {server_url} has been removed from running servers")
                break
    except KeyboardInterrupt:
        print("Process terminated by user.")
        os.kill(pid, signal.SIGTERM)
    except Exception as e:
        print(f"Error monitoring process: {e}")


def run_command(command, server_url=None, port=None):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)
        pid = process.pid
        print(f"Process started with PID {pid}")

        if server_url and pid:
            time.sleep(1)  # Allow some time for the server to start
            print(f"Server running at {server_url} with PID {pid}")
            monitor_process(process, pid, server_url)
        else:
            # Monitor the process until it finishes
            while process.poll() is None:
                time.sleep(1)  # Adjust sleep time as needed

                # Print any new output from the process
                while process.stdout:
                    line = process.stdout.readline()
                    if line.strip():
                        print(line.strip())

                # Optionally, you can also check and print stderr
                while process.stderr:
                    line = process.stderr.readline()
                    if line.strip():
                        print(line.strip())

            # After the process completes, print remaining output
            remaining_output = process.communicate()[0]
            if remaining_output:
                print(remaining_output.strip())

            print(f"Command '{command}' executed successfully.")

        running_servers[server_url] = pid

    except Exception as e:
        print(f"Error running command '{command}': {e}")


def find_available_port(start_port):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', start_port))
            return start_port
        except OSError:
            start_port += 1


def execute_command(command, apps=None, project_directory=None):
    if project_directory:
        os.chdir(project_directory)

    if command.startswith("kill -9"):
        pid_to_kill = int(command.split()[2])
        if pid_to_kill in [pid for _, pid in running_servers.items()]:
            try:
                os.kill(pid_to_kill, 9)
                for url, pid in list(running_servers.items()):
                    if pid == pid_to_kill:
                        del running_servers[url]
                        print(f"Terminated server running at {url} with PID {pid_to_kill}")
                        break
            except ProcessLookupError as e:
                print(f"Failed to terminate server with PID {pid_to_kill}: {e}")
        return

    try:
        server_url = None
        port = None
        if "ng serve" in command and is_angular_project():
            port = find_available_port(4200)
            server_url = f"http://localhost:{port}"
        elif "npm start" in command:
            port = find_available_port(3000)
            server_url = f"http://localhost:{port}"
        elif "vue serve" in command:
            port = find_available_port(8080)
            server_url = f"http://localhost:{port}"
        elif "php -S" in command:
            port = find_available_port(8000)
            server_url = f"http://localhost:{port}"
        elif "python -m http.server" in command:
            port = find_available_port(8000)
            server_url = f"http://localhost:{port}"

        if apps:
            command += f" {apps}"

        run_command(command, server_url, port)

    except Exception as e:
        print(f"Error encountered: {e}")
        handle_missing_dependency(str(e), command)


def is_angular_project():
    return os.path.exists("angular.json") or os.path.exists("package.json")


def install_flutter():
    try:
        subprocess.run(["git", "clone", "https://github.com/flutter/flutter.git", "-b", "stable"])
        subprocess.run(["flutter/bin/flutter", "doctor"], check=True)
        print("Flutter installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Flutter: {e}")


# Function to handle missing dependencies
def handle_missing_dependency(error_message, original_command):
    for keyword, install_function in installation_functions.items():
        if keyword in error_message:
            if not is_tool_installed(keyword, check_command=[keyword, "--version"]):
                print(f"Detected missing dependency for: {keyword}. Installing...")
                if keyword == 'composer':
                    install_composer()  # Install Composer only if it's needed
                elif keyword == 'flutter':
                    install_flutter()  # Install Flutter if it's needed
                elif keyword == 'django':
                    install_django()  # Install Django if it's needed
                elif keyword == 'laravel':
                    install_laravel()  # Install Laravel if it's needed
                elif keyword == 'symfony':
                    install_symfony()  # Install Symfony if it's needed
                elif keyword == 'vue':
                    install_vuejs()  # Install Vue.js if it's needed
                elif keyword == 'next':
                    install_nextjs()  # Install Next.js if it's needed
                elif keyword == 'react':
                    install_react()  # Install React if it's needed
                elif keyword == 'ng':
                    install_angular_cli()  # Install Angular CLI if it's needed
                print(f"Retrying original command: {original_command}")
                execute_command(original_command)
                return

    if "Cannot find module" in error_message or "module not found" in error_message:
        missing_module_pattern = re.compile(r"Cannot find module '(\S+)'")
        match = missing_module_pattern.search(error_message)
        if match:
            missing_module = match.group(1)
            if "ng serve" in original_command:
                print(f"Detected missing Angular module: {missing_module}. Installing...")
                subprocess.run(["npm", "install", missing_module], check=True)
            elif "npm start" in original_command or "npx create-react-app" in original_command:
                print(f"Detected missing React module: {missing_module}. Installing...")
                subprocess.run(["npm", "install", missing_module], check=True)
            elif "vue serve" in original_command:
                print(f"Detected missing Vue module: {missing_module}. Installing...")
                subprocess.run(["npm", "install", missing_module], check=True)
            elif "php -S" in original_command:
                print(f"Detected missing PHP module: {missing_module}. Installing...")
                subprocess.run(["composer", "require", missing_module], check=True)
            elif "python -m http.server" in original_command:
                print(f"Detected missing Python module: {missing_module}. Installing...")
                install_missing_package(missing_module)
            print(f"Retrying original command: {original_command}")
            execute_command(original_command)


def execute_npm_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error encountered while executing npm command: {e}")
        handle_missing_dependency(str(e), command)


# Example usage for npm command
npm_command = "npx create-react-app zzap"
execute_command(npm_command)
execute_npm_command(npm_command)

# Additional functions and commands can be similarly integrated and executed as needed
command = "npx create-react-app zap"
apps = "folder"
execute_command(command, apps)

# Example usage: handle_missing_dependency(error_message, original_command)
error_message = "Cannot find module 'express'"
original_command = "npm start"
handle_missing_dependency(error_message, original_command)
