import socket
from random import randint
from sys import argv
from time import sleep

FIRST_PORT = 8113
DELAY = 1
CLIENT_DELAY = 1


def choose_port() -> int:
    return randint(8000, 9000)


def get_msg() -> str:
    return input("Message to send: ")


def send(msg: str, sock: socket.socket, next_port: str) -> None:
    assert len(msg) <= 9999, "message too long"
    length = str(len(msg)).zfill(4)

    print(f"sending: {length+next_port+msg}...")
    sock.send((length + next_port + msg).encode())


def recv(sock: socket.socket) -> tuple[str, str]:
    length = int(sock.recv(4))
    return sock.recv(4).decode(), sock.recv(length).decode()


def run_client(server_port: int) -> tuple[int, bool]:
    """returns next server port, and weather the program is exited"""
    sleep(CLIENT_DELAY)
    sock = socket.socket()
    print(f"client trying to connect to {server_port}...")
    sock.connect(("127.0.0.1", server_port))
    print(f"connected to {server_port}")
    msg = get_msg()
    exit = msg == "exit"
    port = choose_port()
    send(msg, sock, str(port))
    sock.close()
    return port, exit


def run_server(source_port: int) -> tuple[int, bool]:
    """returns next server port, and weather the program is exited"""
    other_port = -1
    exit = False
    sock = socket.socket()
    sock.bind(("127.0.0.1", source_port))
    print(f"listening on port {source_port}...")
    sock.listen()
    print("connecting...")
    client_sock, _ = sock.accept()
    port, msg = recv(client_sock)
    print(f"received: {msg}")
    other_port = int(port)
    if msg == "exit":
        exit = True
    client_sock.close()
    sock.close()
    return other_port, exit


if __name__ == "__main__":
    side = argv[1].upper().strip()
    print(side in ("A", "B"))
    assert side == "A" or side == "B", "argument `side`: A | B"

    is_client = side == "B"
    server_port = FIRST_PORT
    exit = False
    while not exit:
        if is_client:
            server_port, exit = run_client(server_port)
        else:
            server_port, exit = run_server(server_port)
        is_client = not is_client
        sleep(DELAY)
