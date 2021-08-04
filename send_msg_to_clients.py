from constant import *


def send_to_clients(content_text, user_id, database, online_clients):
    cursor = database.cursor()
    cursor.execute('select * from user where id= %d ' % user_id)
    user_info_tuple = cursor.fetchone()
    user_name = user_info_tuple[1]
    cursor.close()

    chat_bean_data = content_text + CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR
    chat_bean_data += str(user_id) + CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR + user_name

    send_data = PREFIX_MODE_RECEIVE + CHAT_MODE_SEPARATOR + chat_bean_data

    for client in online_clients:
        client.send(send_data.encode('utf-8'))
