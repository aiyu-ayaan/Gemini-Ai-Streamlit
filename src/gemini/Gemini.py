import os
import textwrap

import google.generativeai as genai
from IPython.display import Markdown
from dotenv import load_dotenv

from database.Session import Message, Role, map_message_list_to_history

load_dotenv(override=True)


class Gemini:
    """
    Gemini is a class that uses the Gemini API to generate responses to messages.
    Docs: - https://ai.google.dev/tutorials/python_quickstart
    """

    def __init__(self):
        """
        Initializes the Gemini API with the API key from the environment variables.
        """
        google_api_key = os.getenv('GEMINI_KEY')
        genai.configure(api_key=google_api_key)
        self.__model = genai.GenerativeModel('gemini-pro')
        self.__chat = self.__model.start_chat(history=[])

    def start_new_chat(self, m_list=None):
        """
        Starts a new chat with the Gemini API.
        :param m_list: History of messages to start the chat with.
        """
        if m_list is None:
            m_list = []
        self.__chat = genai.GenerativeModel('gemini-pro').start_chat(
            history=map_message_list_to_history(m_list)
        )

    async def send_message(self, message: str, role: Role) -> Message:
        """
        Sends a message to the Gemini API and returns the response.
        :param message: Message to send.
        :param role: Role of the message sender.
        :return: Response from the Gemini API mapped to the Message class.
        """
        response = self.__chat.send_message({'role': role.name.lower(), 'parts': [message]})
        return Message(
            role=Role.MODEL,
            content=Gemini.to_markdown(response.parts[0].text).data
        )

    def summaries(self, url) -> Markdown:
        """
        Summarizes the content of the given URL.
        :param url: Url
        :return: markdown formatted summary of the content.
        """
        prompt = f'''Summarize the following url in elaborately as possible.
        {url}
        '''
        response = self.__model.generate_content(prompt)
        return Gemini.to_markdown(response.text)

    @staticmethod
    def to_markdown(text):
        """
        Converts the given text to Markdown format.
        :param text: Text to convert.
        :return: Markdown formatted text.
        """
        text = text.replace('•', '  *')
        return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
