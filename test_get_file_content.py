from functions.get_file_content import get_file_content


def show_result(label: str, file: str) -> None:
    result = get_file_content(label, file)
    print(f"{file} length: {len(result)}")
    print(f"{file} truncated: {'truncated' in result}")
    print(result)

def show_lorem(label: str, file: str) -> None:
    result = get_file_content(label, file)
    print(f"{file} length: {len(result)}")
    print(f"{file} truncated: {'truncated' in result}")

if __name__ == "__main__":
    show_lorem("calculator", "lorem.txt")
    show_result("calculator", "main.py")
    show_result("calculator", "pkg/calculator.py")
    show_result("calculator", "pkg/does_not_exist.py")

