from beans import *


def send_to_clients(user_id, database, online_clients):
    cursor = database.cursor()
    cursor.execute('select * from user where id= %d ' % user_id)

    user_info_tuple = cursor.fetchone()
    user_name = user_info_tuple[1]
    user_bean: UserBean = UserBean()
    user_bean.set_user_id(user_id)
    user_bean.set_user_name(user_name)

    chat_bean: ChatBean = ChatBean()
    cursor.execute('select id from %s where id = (select max(id) from %s)' % (TABLE_NAME_CHAT, TABLE_NAME_CHAT))
    chat_id = int(cursor.fetchone()[0])
    cursor.execute('select content from %s where id = (select max(id) from %s)' % (TABLE_NAME_CHAT, TABLE_NAME_CHAT))
    chat_content_text = cursor.fetchone()[0]
    cursor.execute('select img from %s where id = (select max(id) from %s)' % (TABLE_NAME_CHAT, TABLE_NAME_CHAT))
    chat_img_tuple = cursor.fetchone()
    chat_img = chat_img_tuple[0] if len(chat_img_tuple) == 1 else None
    cursor.execute('select like_count from %s where id = (select max(id) from %s)' % (TABLE_NAME_CHAT, TABLE_NAME_CHAT))
    chat_like_count = int(cursor.fetchone()[0])
    cursor.execute('select type_id from %s where id = (select max(id) from %s)' % (TABLE_NAME_CHAT, TABLE_NAME_CHAT))
    chat_type_id = int(cursor.fetchone()[0])
    cursor.execute('select * from %s where id = %d' % (TABLE_NAME_TYPE, chat_type_id))
    type_bean = TypeBean()
    type_tuple = cursor.fetchone()
    if type_tuple:
        type_id, type_name = type_tuple
        type_bean.set_type_id(int(type_id))
        type_bean.set_type_name(type_name)

    chat_bean.set_chat_id(chat_id)
    chat_bean.set_chat_content_text(chat_content_text)
    chat_bean.set_chat_belong_user(user_bean)
    chat_bean.set_chat_img(chat_img)
    chat_bean.set_like_count(chat_like_count)
    chat_bean.set_type_bean(type_bean)

    chat_bean_data = chat_bean.to_json()
    send_data = PREFIX_MODE_RECEIVE + CHAT_MODE_SEPARATOR + chat_bean_data

    for client in online_clients:
        try:
            client.send(send_data.encode('utf-8'))
        except Exception as e:
            print(e)
            continue
