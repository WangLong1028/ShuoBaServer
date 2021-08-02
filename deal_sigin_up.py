from constant import *
import pymysql


def deal_sign_up(client, database: pymysql):
    # 向客户端发送处理数据
    client.send(ACCESS_SIGN_UP_SIGNAL.encode('utf-8'))
    # 接收来自客户端的数据
    data = client.recv(1024).decode('utf-8')
    # 将数据处理
    user_data = data.split(USER_SIGN_UP_SEPARATOR)
    user_name = user_data[0]
    user_password = user_data[1]
    user_secure_problem = user_data[2]
    user_secure_answer = user_data[3]

    if user_name == "null" and user_password == "null" or user_secure_problem == "null" or user_secure_answer == "null":
        # 说明数据传输有误
        client.send(SIGN_UP_TRANSLATE_ERROR.encode('utf-8'))
        client.close()
        return

    # 连接数据库光标
    cursor = database.cursor()
    # 获取所有用户
    lines = cursor.execute('select * from ' + TABLE_NAME_USER)
    for i in range(lines):
        user_data_tuple = cursor.fetchone()
        if user_data_tuple[1] == user_name:
            # 发送存在相同用户名错误
            client.send(SIGN_UP_EXIST_SAME_NAME_ERROR.encode('utf-8'))
            cursor.close()
            client.close()
            return

    # 插入数据
    cursor.execute('insert into ' + TABLE_NAME_USER + ' values (null, "%s", "%s", "%s", "%s")' % (
        user_name, user_password, user_secure_problem, user_secure_answer))
    database.commit()
    # 关闭光标
    cursor.close()

    client.send(SIGN_UP_ANSWER_SUCCESS_SIGNAL.encode('utf-8'))

    client.close()
