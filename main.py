from socket import *
from deal_sigin_up import *
import pymysql
import threading


def deal_data(client, database, data):
    if data == SIGN_UP_SIGNAL:
        # 此时表面是注册请求
        # 交给注册函数解决
        deal_sign_up(client, database)
    else:
        pass


def start_server():
    # 首先加载数据库
    database = pymysql.connect(host="127.0.0.1", port=3306, user="root", database="shuoba")

    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(("", 1028))
    server.listen(128)

    while True:
        client, addr = server.accept()
        deal_thread = threading.Thread(target=deal_data, args=(client, database, client.recv(1024).decode('utf-8')))
        deal_thread.start()


if __name__ == '__main__':
    start_server()
