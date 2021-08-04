class UserBean:

    def __init__(self, user_id, user_name):
        self.id = user_id
        self.user_name = user_name


class ChatBean:

    def __init__(self, content_text, belong_user):
        self.content_text = content_text
        self.belong_user = belong_user
