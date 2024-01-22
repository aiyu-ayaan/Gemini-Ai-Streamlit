import time
from datetime import datetime


def current_milli_time():
    return round(time.time() * 1000)


def formate_time(time_stamp):
    return datetime.fromtimestamp(time_stamp / 1000.0).strftime("%d %b %y %I:%M:%S %p")


