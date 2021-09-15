from constant import *
from beans import *

from send_msg_to_clients import *


def add_prefix(origin):
    return PREFIX_MODE_SEND + CHAT_MODE_SEPARATOR + origin


def deal_chat_send(client, database, body, online_clients):
    # 检查数据
    if body is None:
        client.send(add_prefix(CONNECT_ERROR).encode('utf-8'))
        return

    chat_bean: ChatBean = ChatBean()
    chat_bean.parse_json(body)
    user_bean: UserBean = chat_bean.get_chat_belong_user()

    chat_data_content_text = chat_bean.get_chat_content_text()
    chat_data_user_id = user_bean.get_user_id()
    chat_img = chat_bean.get_chat_img()

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
            if chat_img is None:
                cursor.execute(('insert into ' + TABLE_NAME_CHAT + ' values (null, "%s", %d, null, 0)') % (
                    chat_data_content_text, chat_data_user_id))
            else:
                cursor.execute(('insert into ' + TABLE_NAME_CHAT + ' values (null, "%s", %d, "%s", 0)') % (
                    chat_data_content_text, chat_data_user_id, chat_img))
            database.commit()

            cursor.execute('select max(id) from ' + TABLE_NAME_CHAT)
            cur_id = str(cursor.fetchone()[0])

            cursor.close()
            client.send(add_prefix(CHAT_SEND_SUCCESS + '#' + cur_id).encode('utf-8'))
            # 将数据发送给客户端
            send_to_clients(chat_data_user_id, database, online_clients)
            return

    # 该用户不存在
    cursor.close()
    client.send(add_prefix(CHAT_SEND_NOT_EXIST_USER_ERROR).encode('utf-8'))
