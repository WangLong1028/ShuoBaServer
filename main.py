from socket import *

import pymysql
import gevent

from deal_sigin_up import *
from deal_login import *
from deal_chat_send import *
from deal_request_user import *

from threading import Thread

# 在线的客户端
online_clients = list()


def deal_data(client, database):
    global online_clients
    while True:
        data = None
        try:
            data_b = client.recv(1024)
            data = data_b.decode('utf-8')
            print(data)
        except Exception:
            pass
        # 检查数据
        if not data:
            client.close()
            if online_clients.__contains__(client):
                online_clients.remove(client)
                print('有客户端断开连接')
            return

        header_and_body = data.split(REQUEST_SEPARATOR)

        header = header_and_body[0]
        body = None
        if len(header_and_body) > 1:
            body = header_and_body[1]

        if header == REQUEST_HEADER_SIGN_UP:
            # 此时是注册请求
            client.settimeout(2)
            deal_sign_up(client, database, body)
        elif header == REQUEST_HEADER_LOGIN:
            # 此时是登录请求
            client.settimeout(2)
            deal_login(client, database, body)
        elif header == REQUEST_HEADER_CHAT_CLIENT_LOGIN:
            # 此时是聊天客户端登录请求
            # 添加该客户端
            online_clients.append(client)
            print("有用户接入")
        elif header == REQUEST_HEADER_CHAT_SEND:
            # 此时是发送信息请求
            deal_chat_send(client, database, body, online_clients)
        elif header == REQUEST_HEADER_REQUEST_USER:
            # 此时是申请用户请求
            client.settimeout(2)
            deaL_request_user(client, database, body)
        else:
            pass


def start_server():
    # 首先加载数据库
    database = pymysql.connect(host="127.0.0.1", port=3306, user="root", database="shuoba")

    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(("", 1028))
    server.listen(128)

    g_conn_pool = []  # 连接池

    while True:
        client, addr = server.accept()

        # 加入连接池
        g_conn_pool.append(client)
        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=deal_data, args=(client, database))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()
        # try:
        #     deal_thread = threading.Thread(target=deal_data, args=(client, database))
        #     deal_thread.start()
        # except Exception as e:
        #     print(e)

        # try:
        #     g1 = gevent.spawn(deal_data, client, database)
        #     g1.join()
        # except Exception as e:
        #     print(e)


if __name__ == '__main__':
    start_server()
