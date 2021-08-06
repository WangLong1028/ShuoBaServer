from constant import *


def deaL_request_user(client, database, body):
    user_name = body

    cursor = database.cursor()
    lines = cursor.execute('select * from ' + TABLE_NAME_USER)

    for i in range(lines):
        user_info_tuple = cursor.fetchone()
        if user_name == user_info_tuple[1]:
            # 用户存在
            user_id = str(user_info_tuple[0])
            user_password = user_info_tuple[2]
            secure_problem = user_info_tuple[3]
            secure_answer = user_info_tuple[4]
            headshot = str(user_info_tuple[5])

            send_data = user_id + DATA_SEPARATOR
            send_data += user_name + DATA_SEPARATOR
            send_data += user_password + DATA_SEPARATOR
            send_data += secure_problem + DATA_SEPARATOR
            send_data += secure_answer + DATA_SEPARATOR
            send_data += headshot

            client.send(send_data.encode('utf-8'))
            cursor.close()
            return

    # 说明用户不存在
    cursor.close()
    client.send(LOGIN_USER_NOT_EXIST_ERROR.encode('utf-8'))
