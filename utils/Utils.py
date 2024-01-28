import time
from datetime import datetime
from enum import Enum


def current_milli_time():
    return round(time.time() * 1000)


def formate_time(time_stamp):
    return datetime.fromtimestamp(time_stamp / 1000.0).strftime("%d %b %y %I:%M:%S %p")


class States(Enum):
    DATABASE_STATE = 'database_state'
    CURRENT_SESSION = 'current_session'
    IS_CHAT_HISTORY_EXPANDABLE = 'is_chat_history_expandable'
    IS_CREATE_NEW_SESSION_ENABLED = 'is_create_new_session_enabled'



