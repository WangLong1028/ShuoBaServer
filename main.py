from socket import *
from constant import *

def start_server():
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(("", 1028))
    server.listen(128)
    server.setblocking(False)

    client_list = list()

    while True:
        pass


if __name__ == '__main__':
    start_server()
