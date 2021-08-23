from constant import *


def deal_headshot_pic_post(client, database):
    file_name = client.recv(1024).decode('utf-8')

    length = int(client.recv(1024).decode('utf-8'))

    data = client.recv(1024)
    file_data = b''
    while data is not None:
        file_data += data
        if len(file_data) >= length:
            break
        data = client.recv(1024)

    try:
        with open('./headshot/' + file_name, 'wb') as f:
            f.write(file_data)
            client.send(UPLOAD_SUCCESS.encode('utf-8'))
            client.close()
    except Exception as e:
        client.send(UPLOAD_FAILED.encode('utf-8'))
        client.close()
