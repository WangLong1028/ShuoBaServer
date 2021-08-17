from constant import *


def wrap_chat_data(chat_tuple):
    chat_bean_data = str(chat_tuple[0]) + CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR
    chat_bean_data += chat_tuple[1] + CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR
    return chat_bean_data


def deal_request_history(client, databse, body):
    chat_id = int(body)
    cursor = databse.cursor()

    if chat_id == -1:
        cursor.execute('select max(id) from %s' % TABLE_NAME_CHAT)
        chat_id = cursor.fetchone()[0] + 1

    lines = cursor.execute('select * from %s where id > %d && id < %d' % (TABLE_NAME_CHAT, chat_id - 5, chat_id))

    chat_data_dict = dict()
    for i in range(lines):
        chat_tuple = cursor.fetchone()
        key_chat_data = wrap_chat_data(chat_tuple)
        chat_data_dict[key_chat_data] = chat_tuple[2]

    chat_data_send = PREFIX_MODE_GET_HISTORY + CHAT_MODE_SEPARATOR
    for key in chat_data_dict.keys():
        cursor.execute('select * from %s where id = %d' % (TABLE_NAME_USER, chat_data_dict[key]))
        user_data_tuple = cursor.fetchone()
        chat_data_send += key + str(user_data_tuple[0]) + CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR + user_data_tuple[
            1] + CHAT_BEAN_SEPARATOR

    result = client.send(chat_data_send.encode('utf-8'))
    print(result)

    cursor.close()
