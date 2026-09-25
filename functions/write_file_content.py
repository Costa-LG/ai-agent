from os import path, makedirs

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write content to a file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                },
            },
            "required": ["file_path", "content"],
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
