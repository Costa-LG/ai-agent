from functions.run_python_file import run_python_file


def show_result(label: str, file: str, args: list[str] | None = None) -> None:
    result = run_python_file(label, file, args)
    print(result)


if __name__ == "__main__":
    show_result("calculator", "main.py")
    show_result("calculator", "main.py", ["3 + 5"])
    show_result("calculator", "tests.py")
    show_result("calculator", "../main.py")
    show_result("calculator", "nonexistent.py")
    show_result("calculator", "lorem.txt")

