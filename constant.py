# 表名
TABLE_NAME_USER = "user"
TABLE_NAME_CHAT = "chats"

# user表相关列名
USER_COLUMN_NAME_USER_ID = "id"
USER_COLUMN_NAME_USER_NAME = "user_name"
USER_COLUMN_NAME_USER_PASSWORD = "password"
USER_COLUMN_NAME_USER_SECURE_PROBLEM = "secure_problem"
USER_COLUMN_NAME_USER_SECURE_ANSWER = "secure_answer"

# 请求分隔符
REQUEST_SEPARATOR = "&REQUEST_SEPARATOR&"
DATA_SEPARATOR = "&DATA_SEPARATOR&"

# 请求头
REQUEST_HEADER_SIGN_UP = "REQUEST_HEADER_SIGN_UP"
REQUEST_HEADER_LOGIN = "REQUEST_HEADER_LOGIN"
REQUEST_HEADER_CHAT_CLIENT_LOGIN = "REQUEST_HEADER_CHAT_CLIENT_LOGIN"
REQUEST_HEADER_CHAT_SEND = "REQUEST_HEADER_CHAT_SEND"
REQUEST_HEADER_CHAT_RECEIVE = "REQUEST_HEADER_CHAT_RECEIVE"
REQUEST_HEADER_REQUEST_USER = "REQUEST_HEADER_REQUEST_USER"
REQUEST_HEADER_REQUEST_HISTORY = "REQUEST_HEADER_REQUEST_HISTORY"
REQUEST_HEADER_POST_HEADSHOT_PIC = "REQUEST_HEADER_POST_HEADSHOT_PIC"
REQUEST_HEADER_POST_CHAT_PIC = "REQUEST_HEADER_POST_CHAT_PIC"

REQUEST_HEADER_CHAT_LIKE = "REQUEST_HEADER_CHAT_LIKE"
REQUEST_HEADER_CHAT_UNLIKE = "REQUEST_HEADER_CHAT_UNLIKE"

# 注册相关常量
SIGN_UP_SUCCESS = "SIGN_UP_SUCCESS"
SIGN_UP_EXIST_SAME_USER_NAME_ERROR = "SIGN_UP_EXIST_SAME_USER_NAME_ERROR"

# 登录相关常量
LOGIN_SUCCESS = "LOGIN_SUCCESS"
LOGIN_PASSWORD_ERROR = "LOGIN_PASSWORD_ERROR"
LOGIN_USER_NOT_EXIST_ERROR = "LOGIN_USER_NOT_EXIST_ERROR"

# 聊天相关常量
PREFIX_MODE_SEND = "PREFIX_MODE_SEND"
PREFIX_MODE_RECEIVE = "PREFIX_MODE_RECEIVE"
PREFIX_MODE_GET_HISTORY = "PREFIX_MODE_GET_HISTORY"
CHAT_MODE_SEPARATOR = "&CHAT_MODE_SEPARATOR&"
CHAT_BEAN_SEPARATOR = "&CHAT_BEAN_SEPARATOR&"
CHAT_SEND_SUCCESS = "CHAT_SEND_SUCCESS"
CHAT_SEND_NOT_EXIST_USER_ERROR = "CHAT_SEND_NOT_EXIST_USER_ERROR"
ACCESS_CHAT = "ACCESS_CHAT"

# 聊天接收相关常量
# ChatBean个体间切割符
CHAT_RECEIVE_CHAT_BEAN_SEPARATOR = "&CHAT_BEAN_SEPARATOR&"
CHAT_RECEIVE_CHAT_BEAN_ATTRIBUTE_SEPARATOR = "&CHAT_ATTR_SEPARATOR&"

# 文件上传常量
ACCESS_POST = "ACCESS_POST"
UPLOAD_SUCCESS = "UPLOAD_SUCCESS"
UPLOAD_FAILED = "UPLOAD_FAILED"

# JSON的KEY值
JSON_KEY_USER_ID = "id"
JSON_KEY_USER_NAME = "userName"
JSON_KEY_CHAT_ID = "id"
JSON_KEY_CHAT_CONTENT_TEXT = "contentText"
JSON_KEY_CHAT_BELONG_USER = "belongUser"
JSON_KEY_CHAT_PIC_PATH = "picPath"
JSON_KEY_CHAT_PIC_IMG = "chatPicImg"
JSON_KEY_CHAT_LIKE_COUNT = "likeCount"

# 通用错误返回码
DATA_ILLEGAL_ERROR = "DATA_ILLEGAL_ERROR"
CONNECT_ERROR = "CONNECT_ERROR"
