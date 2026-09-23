from os import path, listdir


def dir_contents(contents: list[str], target_dir: str) -> list[str]:
    return list(map(lambda c: f"- {c}: file_size={path.getsize(path.join(target_dir, c))} bytes, is_dir={path.isdir(path.join(target_dir, c))}", contents))


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        work_dir: str = path.abspath(working_directory)
        target_dir: str = path.normpath(path.join(work_dir, directory))

        valid_target_dir: bool = path.commonpath([work_dir, target_dir]) == work_dir
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        return "\n".join(dir_contents(listdir(target_dir), target_dir))

    except Exception as e:
        return f"Error: {e}"
