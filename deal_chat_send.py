from constant import *
from send_msg_to_clients import *


def add_prefix(origin):
    return PREFIX_MODE_SEND + CHAT_MODE_SEPARATOR + origin


def deal_chat_send(client, database, body, online_clients):
    # 检查数据
    if body is None:
        client.send(add_prefix(CONNECT_ERROR).encode('utf-8'))
        return

    chat_data = body.split(DATA_SEPARATOR)

    # 再次检查数据
    if len(chat_data) != 2:
        # 数据不合法
        client.send(add_prefix(DATA_ILLEGAL_ERROR).encode('utf-8'))
        return

    chat_data_content_text = chat_data[0]
    chat_data_user_id = int(chat_data[1])

    # 检查用户合法性
    cursor = database.cursor()
    # 获取所有用户
    lines = cursor.execute('select * from ' + TABLE_NAME_USER)
    # 找到所属用户
    for i in range(lines):
        user_data_tuple = cursor.fetchone()
        if user_data_tuple[0] == chat_data_user_id:
            # 该用户存在
            cursor.close()
            cursor = database.cursor()
            cursor.execute(('insert into ' + TABLE_NAME_CHAT + ' values (null, "%s", %d, %s)') % (
                chat_data_content_text, chat_data_user_id, 'null'))
            database.commit()
            cursor.close()
            client.send(add_prefix(CHAT_SEND_SUCCESS).encode('utf-8'))
            # 将数据发送给客户端
            send_to_clients(chat_data_user_id, database, online_clients)
            return

    # 该用户不存在
    cursor.close()
    client.send(add_prefix(CHAT_SEND_NOT_EXIST_USER_ERROR).encode('utf-8'))
