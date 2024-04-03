import textwrap
from enum import Enum

from IPython.core.display import Markdown

from database.utils import current_milli_time, formate_time


def to_markdown(text: str) -> Markdown:
    """Convert the text to markdown.

    Args:
        text (str): Text to be converted to markdown.

    Returns:
        Markdown: Markdown text
    """
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


class Role(Enum):
    """
    Enum to define the role of the message.
    """
    MODEL = 0
    USER = 1


class Message:
    """Class to define the message.
    Message with contain the role and content.And further can we wrap in the session.
    """

    def __init__(self, role: Role = Role.MODEL, content: str = ''):
        """Constructor to initialize the message.
        
        Args:
            role (Role, optional): Role of the message. Defaults to Role.MODEL.
            content (str, optional): Content of the message. Defaults to ''.
        """
        self.__role = role
        self.__content = content
        self.__time_stamp = current_milli_time()

    def get_role(self) -> Role:
        """Get the role of the message.
        
        Returns:
            Role: Role of the message
        """
        return self.__role

    def get_content(self) -> str:
        """Get the content of the message.

        Returns:
            str: Content of the message
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

    def get_session_id(self) -> int:
        """Get the session id.

        Returns:
            int: Session id
        """
        return self.__session_id

    def get_session_name(self) -> str:
        """Get the session name.

        Returns:
            str: Session name
        """
        return self.__session_name

    def update_message(self, message=None):
        """Update the messages.

        Args:
            message (list, optional): List of messages. Defaults to None.
        """
        if message is None:
            message = []
        self.__messages = message

    def get_messages(self) -> list[Message]:
        """Get the session name.

        Returns:
            list[Message]: Get the list of messages
        """
        return self.__messages


def convert_to_markdown(session: Session) -> str:
    """Function to convert the session to markdown.

    Args:
        session (Session): Session to be converted to markdown.

    Returns:
        str: Markdown text
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

    return to_markdown(markdown).data


def map_message_list_to_history(messages: list[Message]) -> list[dict]:
    """Function to map the message list to history.
    Give a list of messages and return the history mentioned in https://ai.google.dev/tutorials/python_quickstart .

    Args:
        messages (list[Message]): List of messages

    Returns:
        list[dict]: converted history
    """
    return [{'role': message.get_role().name.lower(), 'parts': [message.get_content()]} for message in messages]
