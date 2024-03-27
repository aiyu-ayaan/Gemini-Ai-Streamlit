import time
from datetime import datetime
from enum import Enum

import validators
from streamlit.components.v1 import html


def current_milli_time():
    """
    Get the current time in milliseconds.
    :return: Current time in milliseconds
    """
    return round(time.time() * 1000)


def formate_time(time_stamp):
    """
    Format the given time stamp to the given format.
    :param time_stamp: Time stamp to format
    :return: Formatted time
    """
    return datetime.fromtimestamp(time_stamp / 1000.0).strftime("%d %b %y %I:%M:%S %p")


class States(Enum):
    """
    Enum to define the state keys for the session state.
    """
    DATABASE_STATE = 'database_state'
    CURRENT_SESSION = 'current_session'
    IS_CHAT_HISTORY_EXPANDABLE = 'is_chat_history_expandable'
    IS_CREATE_NEW_SESSION_ENABLED = 'is_create_new_session_enabled'


class Links(Enum):
    """
    Enum to define the links.
    """
    GITHUB = 'https://github.com/aiyu-ayaan/Gemini-Ai-Streamlit'
    GEMINI = 'https://ai.google.dev/'
    STREAMLIT = 'https://streamlit.io/'
    PYTHON = 'https://www.python.org/'
    AYAAN = 'https://www.github.com/aiyu-ayaan'


def open_page(url):
    """
    Open the given URL in a new tab.
    :param url: URL to open
    """
    open_script = """
            <script type="text/javascript">
                window.open('%s', '_blank').focus();
            </script>
        """ % url
    html(open_script)


def is_valid_url(url):
    """
    Check if the given URL is valid.
    :param url: URL to check
    :return: True if the URL is valid, False otherwise
    """
    return validators.url(url) is True
