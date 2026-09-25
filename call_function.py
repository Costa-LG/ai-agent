from collections.abc import Callable

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file_content import schema_write_file, write_file
import json

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(tool_call, verbose: bool = False) -> dict:
    name:str = tool_call.function.name
    args:dict = json.loads(tool_call.function.arguments or "{}")

    if verbose:
        print(f" - Calling function: {name}({args})")
    else:
        print(f" - Calling function: {name}")

    if name not in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {name}",
        }
    result = function_map[name](working_directory="./calculator", **args)
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }
