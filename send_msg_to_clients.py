from constant import *


def send_to_clients(user_id, database, online_clients):
    cursor = database.cursor()
    cursor.execute('select * from user where id= %d ' % user_id)
    user_info_tuple = cursor.fetchone()
    user_name = user_info_tuple[1]

    cursor.execute('select * from %s where id = (select max(id) from %s)' % (TABLE_NAME_CHAT, TABLE_NAME_CHAT))
    chat_tuple = cursor.fetchone()
    chat_id = str(chat_tuple[0])
    chat_content_text = chat_tuple[1]
    chat_img = None if len(chat_tuple) != 4 else chat_tuple[3]

    cursor.close()

    chat_bean_data = chat_id + CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR
    chat_bean_data += chat_content_text + CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR
    chat_bean_data += str(user_id) + CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR + user_name
    if chat_img:
        chat_bean_data += CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR + chat_img

    send_data = PREFIX_MODE_RECEIVE + CHAT_MODE_SEPARATOR + chat_bean_data

    for client in online_clients:
        client.send(send_data.encode('utf-8'))
