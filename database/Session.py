from enum import Enum

from utils.Utils import current_milli_time, formate_time


class Role(Enum):
    BOT = 0
    USER = 1


class Messages:
    def __init__(self, message='', role=Role.USER):
        self.__message = message
        self.__role: Role = role
        self.__created_at = current_milli_time()

    def get_message(self):
        return self.__message or '', self.__role, self.__created_at


class Session:
    session_id = 0

    def __init__(self, message=None):
        if message is None:
            message: [Messages] = []
        self.__messages = message
        self.session_id = Session.session_id
        self.created_at = current_milli_time()
        Session.session_id += 1

    def add_message(self, message: Messages):
        self.__messages.append(message)

    def get_messages(self):
        return self.__messages

    def get_created_time(self):
        return formate_time(self.created_at)


class SessionDatabase:
    def __init__(self, sessions=None):
        self.__sessions = sessions
        if sessions is None:
            self.create_new_session()
        else:
            self.__sessions = sessions

    def create_new_session(self):
        print('Creating new session')
        if self.__sessions is None:
            self.__sessions = []
        new_session = Session()
        self.__sessions.append(new_session)
        return new_session

    def get_sessions(self):
        return self.__sessions

    def get_recent_session(self):
        return self.__sessions[-1]

    def get_session_by_id(self, session_id):
        for session in self.__sessions:
            if session_id == session.session_id:
                return session
        return None
