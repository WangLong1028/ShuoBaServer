from constant import *
import pymysql


def deal_login(client, database):
    # 向客户端发送允许处理数据
    client.send(ACCESS_LOGIN_SIGNAL.encode('utf-8'))
    # 接收来自客户端的数据
    data = client.recv(1024).decode('utf-8')
    # 处理数据
    user_data = data.split(USER_LOGIN_SEPARATOR)

    if user_data is None:
        # 说明数据传输有误
        client.send(SIGN_UP_TRANSLATE_ERROR.encode('utf-8'))
        client.close()
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

    print(user_name)
    print(user_password)

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
                client.close()
                return
            else :
                # 密码错误
                client.send(LOGIN_PASSWORD_ERROR.encode('utf-8'))
                cursor.close()
                client.close()
                return

    # 用户名不存在
    client.send(LOGIN_USER_NOT_EXIST_ERROR.encode('utf-8'))
    cursor.close()
    cursor.close()



def login_with_secure(client, database, user_data):
    pass