from os import path
from config import MAX_CHARS

schema_get_files_content = {
    "type": "function",
    "function": {
        "name": "get_files_content",
        "description": "Lists content of a file in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "File": {
                    "type": "string",
                    "description": "File path to get the content from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        work_dir: str = path.abspath(working_directory)
        target_file: str = path.normpath(path.join(work_dir, file_path))

        valid_target_dir: bool = path.commonpath([work_dir, target_file]) == work_dir
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file) as f:
            content:str = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content

    except Exception as e:
        return f"Error: {e}"
