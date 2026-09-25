from os import path, makedirs

schema_write_python_file = {
    "type": "function",
    "function": {
        "name": "write_python_file",
        "description": "Write content in a python module in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "Module": {
                    "type": "string",
                    "description": "Module path to be overwritten, relative to the working directory (default is the working directory itself)",
                },
                "Content": {
                    "type": "string",
                    "description": "Python module content to be written.",
                },
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        work_dir: str = path.abspath(working_directory)
        target_file: str = path.normpath(path.join(work_dir, file_path))

        valid_target_dir: bool = path.commonpath([work_dir, target_file]) == work_dir
        if not valid_target_dir:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
        if path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        makedirs(path.dirname(target_file), exist_ok=True)
        with open(target_file, mode="w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
