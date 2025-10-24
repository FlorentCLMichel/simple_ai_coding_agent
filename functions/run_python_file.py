from utils import *
import subprocess

def run_python_file(working_directory, file_path, args=[]) -> str:
    file_path = os.path.join(working_directory, file_path)
    if not path_is_parent(working_directory, file_path):
        return f'ERROR: Cannot execute "{file_path}" as it is outside the permitted working directory {working_directory}'
    if not os.path.exists(file_path):
        f'ERROR: File "{file_path}" not found.'
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        commands = ["python", file_path]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.path.abspath(working_directory),
        )
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"
