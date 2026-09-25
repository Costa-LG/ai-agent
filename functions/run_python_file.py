from os import path
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute a python module in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "Module": {
                    "type": "string",
                    "description": "Module path to be executed, relative to the working directory (default is the working directory itself)",
                },
                "Arguments": {
                    "type": "list[string] | None",
                    "description": "List of arguments to be passet to the python module.",
                },
            },
        },
    },
}

def is_python(path: str) -> bool:
    return path.split(".")[-1] == "py"

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        work_dir: str = path.abspath(working_directory)
        target_file: str = path.normpath(path.join(work_dir, file_path))

        valid_target_dir: bool = path.commonpath([work_dir, target_file]) == work_dir
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if is_python(target_file):
            command = ["python", target_file]
            if args:
                command.extend(args)
            process_result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            text_result: str = ""

            if process_result.returncode != 0:
                text_result += f"Process exited with code {process_result.returncode}a\n"
            if not (process_result.stderr or process_result.stdout):
                text_result += "No output produced"

            text_result += f"STDOUT: {process_result.stdout}STDERR: {process_result.stderr}"

            return text_result
        else:
            return f'Error: "{file_path}" is not a Python file'

    except Exception as e:
        return f"Error: {e}"
