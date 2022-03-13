from socket import *
from beans import *
from constant import *


def deal_request_types(client: socket, database, body):
    # 此时传入当前位置,返回类型列表
    pos = int(body)

    type_bean_list = list()

    cursor = database.cursor()
    lines = cursor.execute('select * from %s where id > %d' % (TABLE_NAME_TYPE, pos))
    for i in range(lines):
        type_id, type_name = cursor.fetchone()
        type_bean = TypeBean()
        type_bean.set_type_id(type_id)
        type_bean.set_type_name(type_name)
        type_bean_list.append(type_bean)
    cursor.close()

    send_data = "["
    for type_bean in type_bean_list:
        send_data += type_bean.to_json()
        send_data += ','
    send_data += ']'
    client.send(send_data.encode('utf-8'))


def deal_search_type(client: socket, database, body):
    search_type_name = str(body)

    cursor = database.cursor()

    lines = cursor.execute('select * from ' + TABLE_NAME_TYPE + ' where name like "%' + search_type_name + '%"')
    send_data = '['
    for i in range(lines):
        type_id, type_name = cursor.fetchone()
        type_bean = TypeBean()
        type_bean.set_type_id(int(type_id))
        type_bean.set_type_name(str(type_name))
        send_data += type_bean.to_json() + ','
    send_data += ']'
    client.send(send_data.encode('utf-8'))

    cursor.close()


def deal_create_type(client: socket, database, body):
    # 此时传入TypeBean的json，返回结果(json或者失败的信号)
    type_bean = TypeBean()
    type_bean.parse_json(body)

    type_name = type_bean.get_type_name()

    cursor = database.cursor()

    lines = cursor.execute('select * from %s where name = "%s"' % (TABLE_NAME_TYPE, type_name))
    if lines > 0:
        # 存在相同行数
        type_id, type_name = cursor.fetchone()
        type_bean = TypeBean()
        type_bean.set_type_id(type_id)
        type_bean.set_type_name(type_name)
        cursor.close()
        client.send((ERROR_TYPE_EXIST_SAME_TYPE + '#TypeBeanExist#' + type_bean.to_json()).encode('utf-8'))
        return
    cursor.execute('insert into ' + TABLE_NAME_TYPE + ' values (NULL, "%s")' % type_name)
    database.commit()

    cursor.execute('select id from ' + TABLE_NAME_TYPE + ' where name = "%s"' % type_name)
    type_id = int(cursor.fetchone()[0])
    type_bean = TypeBean()
    type_bean.set_type_id(type_id)
    type_bean.set_type_name(type_name)
    client.send(type_bean.to_json().encode('utf-8'))

    cursor.close()
