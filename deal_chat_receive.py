from constant import *


class UserBean:

    def __init__(self, id, user_name):
        self.id = id
        self.user_name = user_name


class ChatBean:

    def __init__(self, content_text, belong_user):
        self.content_text = content_text
        self.belong_user = belong_user


def user_bean_to_str(user_bean):
    return user_bean.id + CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR + user_bean.user_name


def chat_bean_to_str(chat_bean):
    return chat_bean.content_text + CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR + user_bean_to_str(chat_bean.belong_user)


def deal_chat_receive(client, database, body):
    # 检查数据
    if body is None:
        client.close()
        return
        # 获取当前所指id
    pointer = int(body)
    # 获取数据库
    cursor = database.cursor()
    # 获取id行数
    lines = cursor.execute('select * from chats')
    # 检查pointer是否合法
    if pointer >= lines:
        client.close()
        cursor.close()
        return
    # 获取ChatBean和user_id数据
    chat_bean_list = list()
    beans_user_id_dict = dict()

    for i in range(lines - pointer):
        chat_tuple = cursor.fetchone()
        content_text = chat_tuple[1]
        user_id = chat_tuple[2]
        chat_bean = ChatBean(content_text, None)
        chat_bean_list.append(chat_bean)
        beans_user_id_dict[chat_bean] = user_id

    send_data = ""

    for i in range(len(chat_bean_list)):
        chat_bean = chat_bean_list[i]
        cursor.execute('select * from chats where id = %d' % (beans_user_id_dict[chat_bean]))
        user_info_tuple = cursor.fetchone()
        user_name = user_info_tuple[1]
        belong_user = UserBean(beans_user_id_dict[chat_bean], user_name)
        chat_bean.belong_user = belong_user
        if i == len(chat_bean_list) - 1:
            send_data += chat_bean_to_str(chat_bean)
            break
        send_data += chat_bean_to_str(chat_bean) + CHAT_RECEIVE_CHAT_BEAN_SEPARATOR

    cursor.close()
    client.send(send_data.encode('utf-8'))
