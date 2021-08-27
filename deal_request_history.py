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

    chat_data_dict = dict()
    chat_data_img_dict = dict()
    for i in range(lines):
        chat_tuple = cursor.fetchone()
        key_chat_data = wrap_chat_data(chat_tuple)
        chat_data_dict[key_chat_data] = chat_tuple[2]
        chat_data_img_dict[key_chat_data] = None if len(chat_tuple) < 4 else chat_tuple[3]

    chat_data_send = PREFIX_MODE_GET_HISTORY + CHAT_MODE_SEPARATOR
    for key in chat_data_dict.keys().__reversed__():
        cursor.execute('select * from %s where id = %d' % (TABLE_NAME_USER, chat_data_dict[key]))
        user_data_tuple = cursor.fetchone()
        chat_data_send += key + str(user_data_tuple[0]) + CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR + user_data_tuple[1]
        if chat_data_img_dict[key]:
            chat_data_send += CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR + chat_data_img_dict[key]
        chat_data_send += CHAT_BEAN_SEPARATOR

    client.send(chat_data_send.encode('utf-8'))

    cursor.close()
