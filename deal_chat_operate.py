from constant import *


def deal_like_chat(client, database, body):
    chat_id = int(body)
    cursor = database.cursor()
    cursor.execute("update %s set like_count = like_count + 1 where id = %d" % (TABLE_NAME_CHAT, chat_id))
    database.commit()
    cursor.close()


def deal_unlike_chat(client, database, body):
    chat_id = int(body)
    cursor = database.cursor()
    cursor.execute("update %s set like_count = like_count - 1 where id = %d" % (TABLE_NAME_CHAT, chat_id))
    database.commit()
    cursor.close()
