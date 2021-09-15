from beans import *
from constant import *


def wrap_chat_data(chat_tuple):
    chat_bean_data = str(chat_tuple[0]) + CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR
    chat_bean_data += chat_tuple[1] + CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR
    return chat_bean_data


def deal_request_history(client, database, body):
    chat_id = int(body)
    cursor = database.cursor()

    if chat_id == -1:
        cursor.execute('select max(id) from %s' % TABLE_NAME_CHAT)
        chat_id = cursor.fetchone()[0] + 1

    lines = cursor.execute('select * from %s where id < %d order by id desc limit 5' % (TABLE_NAME_CHAT, chat_id))
    chat_id_list = list()

    for i in range(lines):
        chat_id_list.append(int(cursor.fetchone()[0]))

    new_chat_id_list = chat_id_list.__reversed__()
    send_data = "["

    for cur_chat_id in new_chat_id_list:
        chat_bean: ChatBean = ChatBean()
        user_bean: UserBean = UserBean()

        cursor.execute('select content from %s where id = %d' % (TABLE_NAME_CHAT, cur_chat_id))
        chat_content_text = cursor.fetchone()[0]
        cursor.execute('select user_id from %s where id = %d' % (TABLE_NAME_CHAT, cur_chat_id))
        user_id = int(cursor.fetchone()[0])
        cursor.execute('select img from %s where id = %d' % (TABLE_NAME_CHAT, cur_chat_id))
        chat_img_tuple = cursor.fetchone()
        chat_img = chat_img_tuple[0] if len(chat_img_tuple) == 1 else None
        cursor.execute('select like_count from %s where id = %d' % (TABLE_NAME_CHAT, cur_chat_id))
        chat_like_count = int(cursor.fetchone()[0])
        cursor.execute('select * from %s where id = %d' % (TABLE_NAME_USER, user_id))
        user_info_tuple = cursor.fetchone()

        user_bean.set_user_id(user_id)
        user_bean.set_user_name(user_info_tuple[1])

        chat_bean.set_chat_id(cur_chat_id)
        chat_bean.set_chat_content_text(chat_content_text)
        chat_bean.set_chat_belong_user(user_bean)
        chat_bean.set_chat_img(chat_img)
        chat_bean.set_like_count(chat_like_count)

        send_data += chat_bean.to_json() + ","

    send_data += "]"

    chat_data_send = PREFIX_MODE_GET_HISTORY + CHAT_MODE_SEPARATOR + send_data
    client.send(chat_data_send.encode('utf-8'))
    cursor.close()
