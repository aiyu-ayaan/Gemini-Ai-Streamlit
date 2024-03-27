from enum import Enum

from gemini.Gemini import Gemini
from utils.Utils import current_milli_time, formate_time


class Role(Enum):
    """
    Enum to define the role of the message.
    """
    MODEL = 0
    USER = 1


class Message:
    """
    Class to define the message.
    Message with contain the role and content.And further can we wrap in the session.
    """

    def __init__(self, role: Role = Role.MODEL, content: str = ''):
        """
        Constructor to initialize the message.
        :param role: Role of the message.
        :param content: Content of the message
        """
        self.__role = role
        self.__content = content
        self.__time_stamp = current_milli_time()

    def get_role(self):
        """
        Get the role of the message.
        :return:  Role of the message
        """
        return self.__role

    def get_content(self):
        """
        Get the content of the message.
        :return: Content of the message
        """
        return self.__content


class Session:
    """
    Class to define the session.
    Session act as a container for the messages. A session will have a unique id and name.
    """

    def __init__(self):
        """
        Constructor to initialize the session.
        """
        self.__session_id = current_milli_time()
        self.__session_name = formate_time(self.__session_id)
        self.__messages = []

    def get_session_id(self):
        """
        Get the session id.
        :return: Session id
        """
        return self.__session_id

    def get_session_name(self):
        """
        Get the session name.
        :return: Session name
        """
        return self.__session_name

    def update_message(self, message=None):
        """
        Use to update a message.
        :param message: messageList
        """
        if message is None:
            message = []
        self.__messages = message

    def get_messages(self):
        """
        Get the messages.
        :return: Message list
        """
        return self.__messages


def convert_to_markdown(session: Session):
    """
    Function to convert the session to markdown.
    :param session: Session
    :return: markdown string
    """
    markdown = '# ' + 'Tutor Talk\n\n'
    markdown += f'## {session.get_session_name()}\n\n'
    for message in session.get_messages():
        if message.get_role() == Role.MODEL:
            markdown += message.get_content() + '\n'
        else:
            markdown += '### ' + message.get_content() + '\n'
    markdown += '\n\n'
    markdown += '---'
    markdown += '\n\n'
    # markdown += '\n\n'
    # markdown += 'Developed by [Ayaan](https://www.github.com/aiyu-ayaan)'
    # markdown += '\n\n'
    markdown += 'Get the code on [GitHub](https://github.com/aiyu-ayaan/Gemini-Ai-Streamlit)'

    return Gemini.to_markdown(markdown).data


def map_message_list_to_history(messages: list[Message]):
    """
    Function to map the message list to history.
    Give a list of messages and return the history mentioned in https://ai.google.dev/tutorials/python_quickstart .
    :param messages: List of a message.
    :return: List of history

    """
    return [{'role': message.get_role().name.lower(), 'parts': [message.get_content()]} for message in messages]
