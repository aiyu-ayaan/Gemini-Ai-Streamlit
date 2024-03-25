import time
from datetime import datetime
from enum import Enum

import validators
from streamlit.components.v1 import html


def current_milli_time():
    return round(time.time() * 1000)


def formate_time(time_stamp):
    return datetime.fromtimestamp(time_stamp / 1000.0).strftime("%d %b %y %I:%M:%S %p")


class States(Enum):
    DATABASE_STATE = 'database_state'
    CURRENT_SESSION = 'current_session'
    IS_CHAT_HISTORY_EXPANDABLE = 'is_chat_history_expandable'
    IS_CREATE_NEW_SESSION_ENABLED = 'is_create_new_session_enabled'


class Links(Enum):
    GITHUB = 'https://github.com/aiyu-ayaan/Gemini-Ai-Streamlit'
    GEMINI = 'https://ai.google.dev/'
    STREAMLIT = 'https://streamlit.io/'
    PYTHON = 'https://www.python.org/'
    AYAAN = 'https://www.github.com/aiyu-ayaan'


def open_page(url):
    open_script = """
            <script type="text/javascript">
                window.open('%s', '_blank').focus();
            </script>
        """ % url
    html(open_script)


def is_valid_url(url):
    return validators.url(url) is True
