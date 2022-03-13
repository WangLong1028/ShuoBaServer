from beans import *
from constant import *


def wrap_chat_data(chat_tuple):
    chat_bean_data = str(chat_tuple[0]) + CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR
    chat_bean_data += chat_tuple[1] + CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR
    return chat_bean_data


def deal_request_history_chat(client, database, body):
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

        comment_count = cursor.execute('select * from %s where chat_id = %d' % (TABLE_NAME_COMM, cur_chat_id))
        cursor.execute('select * from %s where id = %d' % (TABLE_NAME_USER, user_id))
        user_info_tuple = cursor.fetchone()
        user_bean.set_user_id(user_id)
        user_bean.set_user_name(user_info_tuple[1])

        cursor.execute('select type_id from %s where id = %d' % (TABLE_NAME_CHAT, cur_chat_id))
        chat_type_id = cursor.fetchone()[0]
        type_bean = TypeBean()
        if chat_type_id:
            cursor.execute('select * from %s where id = %d' % (TABLE_NAME_TYPE, chat_type_id))
            type_id, type_name = cursor.fetchone()
            type_bean.set_type_id(int(type_id))
            type_bean.set_type_name(type_name)

        chat_bean.set_chat_id(cur_chat_id)
        chat_bean.set_chat_content_text(chat_content_text)
        chat_bean.set_chat_belong_user(user_bean)
        chat_bean.set_chat_img(chat_img)
        chat_bean.set_like_count(chat_like_count)
        chat_bean.set_comment_count(int(comment_count))
        chat_bean.set_type_bean(type_bean)

        send_data += chat_bean.to_json() + ","

    send_data += "]"

    chat_data_send = PREFIX_MODE_GET_HISTORY + CHAT_MODE_SEPARATOR + send_data
    client.send(chat_data_send.encode('utf-8'))
    cursor.close()


def deal_request_history_comm(client, database, body):
    info = body.split('&&')
    chat_id: int = int(info[0])
    comm_id: int = int(info[1])
    cursor = database.cursor()

    if comm_id == -1:
        cursor.execute('select min(id) from ' + TABLE_NAME_COMM)
        max_id_tuple = cursor.fetchone()
        if max_id_tuple:
            comm_id = max_id_tuple[0] - 1
        else:
            client.send(b'')
            cursor.close()
            return

    lines = cursor.execute(
        'select * from %s where id > %d and chat_id = %d limit 5' % (TABLE_NAME_COMM, comm_id, chat_id))
    comm_id_list = list()

    for i in range(lines):
        comm_id_list.append(int(cursor.fetchone()[0]))

    send_data = "["

    for cur_comm_id in comm_id_list:
        comm_bean: CommentBean = CommentBean()
        user_bean: UserBean = UserBean()

        cursor.execute('select content from %s where id = %d' % (TABLE_NAME_COMM, cur_comm_id))
        comm_content_text = cursor.fetchone()[0]
        cursor.execute('select user_id from %s where id = %d' % (TABLE_NAME_COMM, cur_comm_id))
        user_id = int(cursor.fetchone()[0])
        cursor.execute('select comm_img from %s where id = %d' % (TABLE_NAME_COMM, cur_comm_id))
        comm_img_tuple = cursor.fetchone()
        comm_img = comm_img_tuple[0] if len(comm_img_tuple) == 1 else None
        cursor.execute('select chat_id from %s where id = %d' % (TABLE_NAME_COMM, cur_comm_id))
        chat_id = int(cursor.fetchone()[0])
        cursor.execute('select * from %s where id = %d' % (TABLE_NAME_USER, user_id))
        user_info_tuple = cursor.fetchone()

        user_bean.set_user_id(user_id)
        user_bean.set_user_name(user_info_tuple[1])

        comm_bean.set_id(int(cur_comm_id))
        comm_bean.set_comm_content(comm_content_text)
        comm_bean.set_comm_chat_id(chat_id)
        comm_bean.set_comm_user(user_bean)
        comm_bean.set_comm_img(comm_img)

        send_data += comm_bean.to_json() + ","

    send_data += "]"

    client.send(send_data.encode('utf-8'))
    cursor.close()
