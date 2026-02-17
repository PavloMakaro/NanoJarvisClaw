import subprocess
import os

def register_tools(registry):
    registry.register("execute_command", execute_command, "Executes a shell command. Arguments: command (str), timeout (int, optional).")
    registry.register("read_file", read_file, "Reads content of a file. Arguments: filepath (str).")
    registry.register("write_file", write_file, "Writes content to a file. Arguments: filepath (str), content (str).")
    registry.register("list_files", list_files, "Lists files in a directory. Arguments: directory (str, optional).")

def execute_command(command, timeout=30):
    """Executes a shell command."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=timeout
        )
        output = result.stdout
        if result.stderr:
            output += "\nSTDERR:\n" + result.stderr
        return output.strip()
    except subprocess.TimeoutExpired:
        return "Error: Command timed out."
    except Exception as e:
        return f"Error executing command: {str(e)}"

def read_file(filepath):
    """Reads content of a file."""
    if not os.path.exists(filepath):
        return "Error: File not found."
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(filepath, content):
    """Writes content to a file."""
    try:
        dir_path = os.path.dirname(filepath)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return "File written successfully."
    except Exception as e:
        return f"Error writing file: {str(e)}"

def list_files(directory="."):
    """Lists files in a directory."""
    try:
        if not os.path.exists(directory):
            return f"Error: Directory '{directory}' not found."
        return str(os.listdir(directory))
    except Exception as e:
        return f"Error listing files: {str(e)}"
