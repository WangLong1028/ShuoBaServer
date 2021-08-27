from constant import *
import os


def get_pic_info(client):
    file_name_with_length = client.recv(1024).decode('utf-8').split('#')
    file_name = file_name_with_length[0]
    length = int(file_name_with_length[1])

    client.send(b"Got")

    data = client.recv(1024)
    file_data = b''
    while data is not None:
        file_data += data
        if len(file_data) >= length:
            break
        data = client.recv(1024)

    return file_name, file_data


def write_file(client, file_name, file_dir, file_data):
    try:
        with open('./' + file_dir + '/' + file_name, 'wb') as f:
            f.write(file_data)
            client.send(UPLOAD_SUCCESS.encode('utf-8'))
    except Exception as e:
        client.send(UPLOAD_FAILED.encode('utf-8'))


def get_chat_pic_info(client):
    file_name_with_length = client.recv(1024).decode('utf-8').split('#')
    file_name = file_name_with_length[0]
    length = int(file_name_with_length[1])

    file_t = 0
    for cur_file_name in os.listdir('./chats/'):
        cur_num = int(cur_file_name.split('.')[0])
        if cur_num > file_t:
            file_t = cur_num
    file_t += 1
    file_name = str(file_t) + file_name

    client.send(("Got#" + file_name).encode('utf-8'))

    data = client.recv(1024)
    file_data = b''
    while data is not None:
        file_data += data
        if len(file_data) >= length:
            break
        data = client.recv(1024)

    return file_name, file_data


def deal_chat_pic_post(client, database):
    pic_info = get_chat_pic_info(client)
    file_name = pic_info[0]
    file_data = pic_info[1]
    write_file(client, file_name, 'chats', file_data)


def deal_headshot_pic_post(client, database):
    pic_info = get_pic_info(client)
    file_name = pic_info[0]
    file_data = pic_info[1]
    write_file(client, file_name, 'headshot', file_data)
    client.close()
