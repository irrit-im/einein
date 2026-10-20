import functools
from pathlib import Path
from sys import argv


def remove_comment_lines(file_name: str) -> None: 
    Path(file_name + ".no_comment.py").write_text("".join(((line if not line.lstrip().startswith("#") else "")if line.lstrip()else "\n") for line in Path(file_name).read_text()))


def remove_comments(file_name: str) -> None: 
    open(file_name + ".no_comment.py", "w+").write("".join(((line if "#" not in line.lstrip() else line[: line.index("#")] + "\n") if line.lstrip() else line) for line in open(file=file_name, mode="r")))


def fibonacci(n: int) -> list[int]:
    return [functools.reduce(lambda prev, _: (prev[1],prev[0] + prev[1]),range(i),(0, 1),)[1] for i in range(n)]


if __name__ == "__main__":
    path = argv[1]
    remove_comment_lines(path)
    remove_comments(path)

    print(fibonacci(0))
