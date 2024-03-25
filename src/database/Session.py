import textwrap
from enum import Enum

from IPython.display import Markdown

from utils.Utils import current_milli_time, formate_time


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


class Role(Enum):
    MODEL = 0
    USER = 1


class Message:
    def __init__(self, role: Role = Role.MODEL, content: str = ''):
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

    def convert_to_markdown(self):
        markdown = '# ' + 'Tutor Talk\n\n'
        markdown += f'## {self.__session_name}\n\n'
        for message in self.__messages:
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


def map_message_list_to_history(messages: list[Message]):
    return [{'role': message.get_role().name.lower(), 'parts': [message.get_content()]} for message in messages]
