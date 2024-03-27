import os
import textwrap

import google.generativeai as genai
from IPython.display import Markdown
from dotenv import load_dotenv

from database.Session import Message, Role, map_message_list_to_history

load_dotenv(override=True)


class Gemini:
    """Gemini is a class that uses the Gemini API to generate responses to messages.
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

    def start_new_chat(self, m_list:list[dict]=None):
        """Start a new chat with the given message list.

        Args:
            m_list (list[dict], optional): Chat history. Defaults to None.
        """
        if m_list is None:
            m_list = []
        self.__chat = genai.GenerativeModel('gemini-pro').start_chat(
            history=map_message_list_to_history(m_list)
        )

    async def send_message(self, message: str, role: Role) -> Message:
        """Sends a message to the Gemini API and returns the response.

        Args:
            message (str): Message to send.
            role (Role): Role of the message sender.

        Returns:
            Message: Response from the Gemini API mapped to the Message class.
        """
        response = self.__chat.send_message({'role': role.name.lower(), 'parts': [message]})
        return Message(
            role=Role.MODEL,
            content=Gemini.to_markdown(response.parts[0].text).data
        )

    def summaries(self, url:str) -> Markdown:
        """Summarizes the content of the given URL.
        
        Args:
            url (str): Url to summarize.

        Returns:
            Markdown: Markdown formatted summary of the content.
        """
        prompt = f'''Summarize the following url in elaborately as possible.
        {url}
        '''
        response = self.__model.generate_content(prompt)
        return Gemini.to_markdown(response.text)

    @staticmethod
    def to_markdown(text:str)->Markdown:
        """Converts the given text to Markdown format.
    
        Args:
            text (str): Text to convert.

        Returns:
            Markdown: Markdown formatted text.
        """
        text = text.replace('•', '  *')
        return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
