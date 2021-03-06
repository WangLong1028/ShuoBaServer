from constant import *


def deal_sign_up(client, database, body):
    # 切割得到数据
    user_data = body.split(DATA_SEPARATOR)

    if user_data is None or len(user_data) < 3:
        # 说明数据传输有误
        client.send(DATA_ILLEGAL_ERROR.encode('utf-8'))
        return

    user_name = user_data[0]
    user_password = user_data[1]
    user_secure_problem = user_data[2]
    user_secure_answer = user_data[3]

    if user_name == "null" and user_password == "null" or user_secure_problem == "null" or user_secure_answer == "null":
        # 说明数据传输有误
        client.send(DATA_ILLEGAL_ERROR.encode('utf-8'))
        return

    print()
    print('+', '-' * 50, '+', sep='')
    print('|', ' \t有用户注册', sep='')
    print('|', " \t用户名 : ", user_name, sep='')
    print('+', '-' * 50, '+', sep='')
    print()

    # 连接数据库光标
    cursor = database.cursor()
    # 获取所有用户
    lines = cursor.execute('select * from ' + TABLE_NAME_USER)
    cur_id = 0
    for i in range(lines):
        user_data_tuple = cursor.fetchone()
        cur_id = user_data_tuple[0]
        if user_data_tuple[1] == user_name:
            # 发送存在相同用户名错误
            client.send(SIGN_UP_EXIST_SAME_USER_NAME_ERROR.encode('utf-8'))
            cursor.close()
            return

    # 插入数据
    cursor.execute('insert into ' + TABLE_NAME_USER + ' values (null, "%s", "%s", "%s", "%s", null)' % (
        user_name, user_password, user_secure_problem, user_secure_answer))
    database.commit()
    # 关闭光标
    cursor.close()
    # 表明成功
    client.send((SIGN_UP_SUCCESS + '#' + str(cur_id + 1)).encode('utf-8'))
