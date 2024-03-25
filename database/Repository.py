from enum import Enum

import streamlit as st

from database.Interface import ChatRepository
from database.Session import Session, Message, Role


class State(Enum):
    CHAT_REPOSITORY = 'ChatRepository'
    GEMINI = 'Gemini'
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


class ChatRepositoryImp(ChatRepository):

    def __init__(self):
        self.__session_list = create_or_update_session(State.SESSION_LIST_STATE.value, [Session()])
        self.__current_session: Session = create_or_update_session(State.CURRENT_SESSION.value,
                                                                   get_value_from_state(State.SESSION_LIST_STATE.value)[
                                                                       0])

    def create_new_session(self):
        session = self.__session_list
        session.append(Session())
        create_or_update_session(State.SESSION_LIST_STATE.value, updated_value=session)
        create_or_update_session(State.CURRENT_SESSION.value, updated_value=session[-1])
        print('Session Created', get_value_from_state(State.CURRENT_SESSION.value).get_session_name())
        self.__session_list = session
        self.__current_session = session[-1]
        print('Current Session', self.__current_session.get_session_name())

    def get_all_session(self):
        return self.__session_list

    def get_current_session(self, session_id: int):
        for session in self.__session_list:
            if session.get_session_id() == session_id:
                self.__current_session = session
                create_or_update_session(
                    State.CURRENT_SESSION.value,
                    updated_value=self.__current_session
                )
                return session
        return self.__current_session

    def get_current(self) -> Session:
        return get_value_from_state(State.CURRENT_SESSION.value)

    def add_message(self, message: str, role: Role):
        messages = self.get_current().get_messages()
        messages.append(Message(role, message))
        self.__current_session.update_message(messages)
        session = create_or_update_session(State.CURRENT_SESSION.value, updated_value=self.__current_session)
        self.__current_session = session
