from threading import Thread

import pymysql

from deal_chat_operate import *
from deal_chat_send import *
from deal_comm_send import *
from deal_file_request import *
from deal_login import *
from deal_pic_post import *
from deal_request_history import *
from deal_request_user import *
from deal_sigin_up import *
from deal_types import *

# 在线的客户端
online_clients = list()


def deal_data(client: socket, database):
    global online_clients
    while True:
        try:
            data_b = client.recv(1024)
            data = data_b.decode('utf-8')
        except Exception:
            if online_clients.__contains__(client):
                online_clients.remove(client)
                print('有客户端断开连接')
            client.close()
            return
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
            # 向客户端发送允许连接消息
            client.send(ACCESS_CHAT.encode('utf-8'))
            print("有用户接入")
        elif header == REQUEST_HEADER_CHAT_SEND:
            # 此时是发送信息请求
            deal_chat_send(client, database, body, online_clients)
        elif header == REQUEST_HEADER_REQUEST_USER:
            # 此时是申请用户请求
            client.settimeout(2)
            deaL_request_user(client, database, body)
        elif header == REQUEST_HEADER_CHAT_LIKE:
            # 此时是点赞请求
            deal_like_chat(client, database, body)
        elif header == REQUEST_HEADER_CHAT_UNLIKE:
            # 此时是收回点赞请求
            deal_unlike_chat(client, database, body)
        elif header == REQUEST_HEADER_REQUEST_HISTORY:
            # 此时是申请历史消息
            deal_request_history_chat(client, database, body)
        elif header == REQUEST_HEADER_POST_HEADSHOT_PIC:
            # 此时是上传头像图片请求
            deal_headshot_pic_post(client, database)
        elif header == REQUEST_HEADER_POST_CHAT_PIC:
            # 此时是上传聊天图片请求
            deal_chat_pic_post(client, database)
        elif header == REQUEST_HEADER_POST_COMM_PIC:
            # 此时是上传评论图片请求
            deal_comm_pic_post(client, database, body)
        elif header == REQUEST_HEADER_SEND_COMMENT:
            # 此时是发表评论请求
            deal_comm_send(client, database, body)
        elif header == REQUEST_HEADER_REQUEST_COMMENT:
            # 此时是获取评论请求
            deal_request_history_comm(client, database, body)
        elif header == REQUEST_HEADER_CREATE_TYPE:
            # 此时是创建标签请求
            deal_create_type(client, database, body)
        elif header == REQUEST_HEADER_SEARCH_TYPE:
            # 此时是搜索标签请求
            deal_search_type(client, database, body)
        elif header == REQUEST_HEADER_HISTORY_TYPE:
            # 此时是获取更多类型标签请求
            deal_request_types(client, database, body)
        else:
            # 此时是发送文件
            deal_file_request(client, header)


def check_conn(database):
    try:
        database.ping()
    except Exception as e:
        database = pymysql.connect(host="127.0.0.1", port=3306, user="root", database="shuoba")


def start_server():
    # 首先加载数据库
    database = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd='', database="shuoba")

    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(("", 8001))
    server.listen(128)

    g_conn_pool = []  # 连接池

    while True:
        client, addr = server.accept()

        # 检查数据库连接
        try:
            database.ping()
        except Exception as e:
            database = pymysql.connect(host="127.0.0.1", port=3306, user="root", database="shuoba")
        # 以上代码不能用则更换为check_conn(database)

        # 加入连接池
        g_conn_pool.append(client)
        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=deal_data, args=(client, database))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()


if __name__ == '__main__':
    start_server()
