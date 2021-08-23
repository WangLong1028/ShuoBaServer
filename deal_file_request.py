import re
import os


def deal_file_request_headshot(client, user_id):
    for file_name in os.listdir('./headshot/'):
        if file_name.split('.')[0] == user_id:
            return file_name


def deal_file_request(client, header):
    data_re = re.match(r'[^ ]* /([^ ]*).*', header)
    if data_re:
        file_name = None
        if data_re.group(1)[0:8] == 'headshot':
            # 处理头像请求
            file_name = deal_file_request_headshot(client, data_re.group(1)[9:])
            if file_name:
                file_name = './headshot/' + file_name
                print(file_name)
        else:
            file_name = './' + data_re.group(1)

        if file_name is None:
            header = 'HTTP/1.1 404 Not Found\r\n'
            client.send(header.encode('utf-8'))
            client.close()
            return

        data = b''
        try:
            with open(file_name, 'rb') as f:
                data = f.read()

            header = 'HTTP/1.1 200 Ok\r\n'
            header += 'Accept-Ranges: bytes\r\n'
            header += 'Cache-Control: max-age=315360000\r\n'
            header += f'Content-Length: {len(data):d}\r\nServer: Apache\r\n\r\n'
            client.send(header.encode('utf-8'))
            client.send(data)
            client.close()

        except Exception as e:
            header = 'HTTP/1.1 404 Not Found\r\n'
            client.send(header.encode('utf-8'))
            client.close()
