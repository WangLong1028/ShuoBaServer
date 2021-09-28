import json

from constant import *


class UserBean:

    def __init__(self):
        self.user_bean_data = dict()
        self.user_bean_data.setdefault(None)

    def parse_json(self, json_data):
        data: dict = json.loads(json_data)
        for key in data.keys():
            self.user_bean_data[key] = data[key]

    def parse_dict(self, dict_data: dict):
        for key in dict_data.keys():
            self.user_bean_data[key] = dict_data[key]

    def to_json(self):
        return json.dumps(self.user_bean_data, ensure_ascii=False)

    def get_user_id(self):
        return self.user_bean_data[JSON_KEY_USER_ID]

    def set_user_id(self, user_id):
        self.user_bean_data[JSON_KEY_USER_ID] = user_id

    def set_user_name(self, user_name):
        self.user_bean_data[JSON_KEY_USER_NAME] = user_name


class ChatBean:

    def __init__(self):
        self.chat_bean_data = dict()
        self.chat_bean_data.setdefault(JSON_KEY_CHAT_PIC_IMG, None)

    def parse_json(self, json_data):
        data: dict = json.loads(json_data)
        for key in data.keys():
            if key == JSON_KEY_CHAT_BELONG_USER:
                user_bean: UserBean = UserBean()
                user_bean.parse_dict(data[key])
                self.chat_bean_data[key] = user_bean
                continue
            self.chat_bean_data[key] = data[key]

    def to_json(self):
        json_dict: dict = dict()
        for key in self.chat_bean_data.keys():
            if key == JSON_KEY_CHAT_BELONG_USER:
                json_dict[key] = self.chat_bean_data[key].user_bean_data
                continue
            json_dict[key] = self.chat_bean_data[key]
        return json.dumps(json_dict, ensure_ascii=False)

    def get_chat_id(self):
        return self.chat_bean_data[JSON_KEY_CHAT_ID]

    def get_chat_content_text(self):
        return self.chat_bean_data[JSON_KEY_CHAT_CONTENT_TEXT]

    def get_chat_belong_user(self):
        return self.chat_bean_data[JSON_KEY_CHAT_BELONG_USER]

    def get_chat_img(self):
        return self.chat_bean_data[JSON_KEY_CHAT_PIC_IMG]

    def get_like_count(self):
        return self.chat_bean_data[JSON_KEY_CHAT_LIKE_COUNT]

    def get_comment_count(self):
        return self.chat_bean_data[JSON_KEY_CHAT_COMMENT_COUNT]

    def set_chat_id(self, chat_id):
        self.chat_bean_data[JSON_KEY_CHAT_ID] = chat_id

    def set_chat_content_text(self, chat_content_text):
        self.chat_bean_data[JSON_KEY_CHAT_CONTENT_TEXT] = chat_content_text

    def set_chat_belong_user(self, user):
        self.chat_bean_data[JSON_KEY_CHAT_BELONG_USER] = user

    def set_chat_img(self, img):
        self.chat_bean_data[JSON_KEY_CHAT_PIC_IMG] = img

    def set_like_count(self, like_count):
        self.chat_bean_data[JSON_KEY_CHAT_LIKE_COUNT] = like_count

    def set_comment_count(self, comment_count):
        self.chat_bean_data[JSON_KEY_CHAT_COMMENT_COUNT] = comment_count


class CommentBean:

    def __init__(self):
        self.comm_bean_data = dict()
        self.comm_bean_data[JSON_KEY_COMM_IMG] = None

    def parse_json(self, json_data):
        data: dict = json.loads(json_data)
        for key in data.keys():
            if key == JSON_KEY_COMM_BELONG_USER:
                user_bean = UserBean()
                user_bean.parse_dict(data[key])
                self.comm_bean_data[key] = user_bean
                continue
            self.comm_bean_data[key] = data[key]

    def to_json(self):
        json_dict: dict = dict()
        for key in self.comm_bean_data.keys():
            if key == JSON_KEY_COMM_BELONG_USER:
                json_dict[key] = self.comm_bean_data[key].user_bean_data
                continue
            json_dict[key] = self.comm_bean_data[key]
        return json.dumps(json_dict, ensure_ascii=False)

    def get_id(self):
        return self.comm_bean_data[JSON_KEY_COMM_ID]

    def get_comm_content(self):
        return self.comm_bean_data[JSON_KEY_COMM_CONTENT_TEXT]

    def get_comm_user(self):
        return self.comm_bean_data[JSON_KEY_COMM_BELONG_USER]

    def get_chat_id(self):
        return self.comm_bean_data[JSON_KEY_COMM_CHAT_ID]

    def get_comm_img(self):
        return self.comm_bean_data[JSON_KEY_COMM_IMG]

    def set_comm_img(self, file_name):
        self.comm_bean_data[JSON_KEY_COMM_IMG] = file_name

    def set_id(self, comm_id):
        self.comm_bean_data[JSON_KEY_COMM_ID] = comm_id

    def set_comm_content(self, comm_content):
        self.comm_bean_data[JSON_KEY_COMM_CONTENT_TEXT] = comm_content

    def set_comm_user(self, belong_user):
        self.comm_bean_data[JSON_KEY_COMM_BELONG_USER] = belong_user

    def set_comm_chat_id(self, chat_id):
        self.comm_bean_data[JSON_KEY_COMM_CHAT_ID] = chat_id

    def set_comm_img(self, comm_img):
        self.comm_bean_data[JSON_KEY_COMM_IMG] = comm_img
