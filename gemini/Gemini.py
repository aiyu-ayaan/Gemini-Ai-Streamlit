import os
import textwrap

import google.generativeai as genai
from IPython.display import Markdown
from dotenv import load_dotenv

from database.Session import Message, Role, map_message_list_to_history

load_dotenv(override=True)


class Gemini:
    def __init__(self):
        google_api_key = os.getenv('GEMINI_KEY')
        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel('gemini-pro')
        self.__chat = model.start_chat(history=[])

    def start_new_chat(self, m_list=None):
        if m_list is None:
            m_list = []
        self.__chat = genai.GenerativeModel('gemini-pro').start_chat(
            history=map_message_list_to_history(m_list)
        )

    def send_message(self, message: str, role: Role):
        response = self.__chat.send_message({'role': role.name.lower(), 'parts': [message]})
        return Message(
            role=Role.MODEL,
            content=response.parts[0].text
        )

    @staticmethod
    def to_markdown(text):
        text = text.replace('•', '  *')
        return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))