from functions.write_file_content import write_file


def show_result(label: str, file: str, content: str) -> None:
    result = write_file(label, file, content)
    print(result)


if __name__ == "__main__":
    show_result("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    show_result("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    show_result("calculator", "/tmp/temp.txt", "this should not be allowed")

