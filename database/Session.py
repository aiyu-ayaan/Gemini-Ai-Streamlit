from enum import Enum
import streamlit as st
from utils.Utils import current_milli_time, formate_time


class Role(Enum):
    BOT = 0
    USER = 1


class State(Enum):
    DATABASE_STATE = 'database_state'
    SESSION_LIST_STATE = 'session_list_state'
    CURRENT_SESSION = 'current_session'
    MESSAGES_LIST = 'messages_list'


def create_or_update_session(key, init_value=None, updated_value=None):
    if key not in st.session_state and init_value is not None:
        st.session_state[key] = init_value
    elif key in st.session_state and updated_value is not None:
        st.session_state[key] = updated_value

    return st.session_state[key] if key in st.session_state else None


def get_value_from_state(key):
    return st.session_state[key]


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


class Database:

    @staticmethod
    def create_new_session_session_list():
        create_or_update_session(State.SESSION_LIST_STATE.value, init_value=[Session()])

    @staticmethod
    def get_session(session_id=None) -> Session:
        create_or_update_session(
            State.CURRENT_SESSION.value,
            init_value=get_value_from_state(State.SESSION_LIST_STATE.value)[0],
            # updated_value=get_value_from_state(State.SESSION_LIST_STATE.value)[0] if session_id is None else
            # [session for 9session in get_value_from_state(State.SESSION_LIST_STATE.value) if
            #  session.get_session_id() == session_id][0]
        )
        return get_value_from_state(State.CURRENT_SESSION.value)

    @staticmethod
    def get_all_session():
        return get_value_from_state(State.SESSION_LIST_STATE.value)

    @staticmethod
    def add_message(message: str, role: Role = Role.BOT):
        current_session = Database.get_session()
        d = current_session.get_messages()
        print(len(d))
        messages = create_or_update_session(State.MESSAGES_LIST.value, init_value=[])
        messages.append(Message(role, message))
        current_session.update_message(messages)
        create_or_update_session(State.MESSAGES_LIST.value, updated_value=messages)
