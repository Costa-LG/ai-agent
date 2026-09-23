from functions.get_files_info import get_files_info


def show_result(label: str, directory: str) -> None:
    print(label)
    print("\n".join(f"  {line}" for line in get_files_info("calculator", directory).splitlines()))
    print()


if __name__ == "__main__":
    show_result("Result for current directory:", ".")
    show_result("Result for 'pkg' directory:", "pkg")
    show_result("Result for '/bin' directory:", "/bin")
    show_result("Result for '../' directory:", "../")
