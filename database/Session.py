from enum import Enum
from utils.Utils import current_milli_time, formate_time


class Role(Enum):
    BOT = 0
    USER = 1


class Message:
    def __init__(self, role: Role = Role.BOT, content: str = ''):
        self.__role = role
        self.__content = content
        self.__time_stamp = current_milli_time()

    def get_role(self):
        return self.__role

    def get_content(self):
        return self.__content


class Session:
    def __init__(self):
        self.__session_id = current_milli_time()
        self.__session_name = formate_time(self.__session_id)
        self.__messages = []

    def get_session_id(self):
        return self.__session_id

    def get_session_name(self):
        return self.__session_name

    def update_message(self, message=None):
        if message is None:
            message = []
        self.__messages = message

    def get_messages(self):
        return self.__messages
