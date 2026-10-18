from sys import argv


def save_file(path: str, content: str) -> None:

    with open(path, "w+") as file:
        file.write(content)


def remove_comment_lines(file_name: str) -> None:  # jfgjh
    with open(file=file_name, mode="r") as file:
        uncommented = ""
        for line in file:
            stripped_line = line.lstrip()
            if stripped_line:
                if not stripped_line.startswith("#"):  # jfoosogj
                    uncommented += line
            else:
                uncommented += "\n"
        save_file(path=file_name + ".no_comment.py", content=uncommented)


def remove_comments(file_name: str) -> None:  # jfgjh
    with open(file=file_name, mode="r") as file:
        uncommented = ""
        for line in file:
            stripped_line = line.lstrip()
            if stripped_line and "#" in line:  # jfoosogj
                comment_index = line.index("#")
                uncommented += line[:comment_index] + "\n"
            else:
                uncommented += line
        save_file(path=file_name + ".really_no_comment.py", content=uncommented)


def fibonacci(n: int) -> list[int]:
    fibo = []
    for i in range(1, n + 1):
        if i <= 2:
            fibo.append(1)
        else:
            fibo.append(fibo[-1] + fibo[-2])
    return fibo


if __name__ == "__main__":
    path = argv[1]
    remove_comment_lines(path)
    remove_comments(path)
    print(fibonacci(6))
