from constant import *


def deal_login(client, database, body):
    # 处理数据
    user_data = body.split(DATA_SEPARATOR)

    if user_data is None:
        # 说明数据传输有误
        client.send(DATA_ILLEGAL_ERROR.encode('utf-8'))
        return

    if len(user_data) == 2:
        # 用账号和密码登录
        login_with_password(client, database, user_data)
    else:
        # 用安全问题登录
        login_with_secure(client, database, user_data)


def login_with_password(client, database, user_data):
    user_name = user_data[0]
    user_password = user_data[1]

    print()
    print('+', '-' * 50, '+', sep='')
    print('|', ' 有用户登录', ' ' * 41)
    print('|', " 用户名 :", user_name)
    print('+', '-' * 50, '+', sep='')
    print()

    # 得到数据库光标
    cursor = database.cursor()
    # 获取所有用户
    lines = cursor.execute('select * from ' + TABLE_NAME_USER)
    for i in range(lines):
        user_data_tuple = cursor.fetchone()
        if user_data_tuple[1] == user_name:
            if user_data_tuple[2] == user_password:
                # 登陆成功
                client.send(LOGIN_SUCCESS.encode('utf-8'))
                cursor.close()
                return
            else:
                # 密码错误
                client.send(LOGIN_PASSWORD_ERROR.encode('utf-8'))
                cursor.close()
                return

    # 用户名不存在
    client.send(LOGIN_USER_NOT_EXIST_ERROR.encode('utf-8'))
    cursor.close()


def login_with_secure(client, database, user_data):
    pass
