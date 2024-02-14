from enum import Enum
import streamlit as st
from utils.Utils import current_milli_time, formate_time


class Role(Enum):
    BOT = 0
    USER = 1


class State(Enum):
    DATABASE_STATE = 'database_state'
    CURRENT_SESSION = 'current_session'
    MESSAGES = 'messages'


def create_or_update_session(key, init_value=None, updated_value=None):
    if key not in st.session_state and init_value is not None:
        st.session_state[key] = init_value
    elif key in st.session_state and updated_value is not None:
        st.session_state[key] = updated_value

    return st.session_state[key] if key in st.session_state else None


def get_session(key):
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


class Database:

    @staticmethod
    def add_message(message: str, role: Role = Role.BOT):
        messages = create_or_update_session(State.MESSAGES.value, [])
        messages.append(Message(role, message))
        print(len(messages))
        create_or_update_session(State.MESSAGES.value, updated_value=messages)
