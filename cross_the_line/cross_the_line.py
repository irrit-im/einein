import functools
from sys import argv


def save_file(path: str, content: str) -> None:

    with open(path, "w+") as file:
        file.write(content)


def remove_comment_lines(file_name: str) -> None:  # jfgjh
    with open(file=file_name, mode="r") as file:
        save_file(
            path=file_name + ".no_comment.py",
            content="".join(
                (
                    (line if not line.lstrip().startswith("#") else "")
                    if line.lstrip()
                    else "\n"
                )
                for line in file
            ),
        )


def remove_comments(file_name: str) -> None:  #
    with open(file=file_name, mode="r") as file:
        save_file(
            path=file_name + ".really_no_comment.py",
            content="".join(
                (
                    (
                        line
                        if "#" not in line.lstrip()
                        else line[: line.index("#")] + "\n"
                    )
                    if line.lstrip()
                    else line
                )
                for line in file
            ),
        )


def fibonacci(n: int) -> list[int]:
    return []  # TODO do this in one line using reduce
    # return (
    #     []
    #     if n == 0
    #     else functools.reduce(
    #         function=lambda result, _: (result[1], result[0] + result[1]),
    #         iterable=[(0, 0) for _ in range(1, n)],
    #     )
    # )
    # # for i in range(1, n + 1): fibo.append(1 if i <= 2 else fibo[-1] + fibo[-2])
    # # return


if __name__ == "__main__":
    path = argv[1]
    remove_comment_lines(path)
    remove_comments(path)
    print(fibonacci(6))
