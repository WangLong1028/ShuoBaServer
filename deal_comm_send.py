from constant import *
from socket import *
from beans import *
from pymysql import *


def deal_comm_send(client: socket, database, body):
    if body:
        comment_bean: CommentBean = CommentBean()
        comment_bean.parse_json(body)

        cursor = database.cursor()
        if comment_bean.get_comm_img():
            cursor.execute(('insert into ' + TABLE_NAME_COMM + ' values (null, "%s", %d, %d, "%s")') %
                           (comment_bean.get_comm_content(),
                            comment_bean.get_chat_id(),
                            comment_bean.get_comm_user().get_user_id(),
                            comment_bean.get_comm_img()))
        else:
            cursor.execute(('insert into ' + TABLE_NAME_COMM + ' values (null, "%s", %d, %d, null)') %
                           (comment_bean.get_comm_content(),
                            comment_bean.get_chat_id(),
                            comment_bean.get_comm_user().get_user_id()))
        database.commit()
        cursor.close()
        client.send(COMM_SEND_SUCCESS.encode('utf-8'))
    else:
        client.send(CONNECT_ERROR.encode('utf-8'))
