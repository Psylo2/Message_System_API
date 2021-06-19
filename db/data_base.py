"""this file is made in order to:
[*] prevent over looped imports
[*] Encrypt / Decrypt Passwords
[*] Convert local TZ to UTC for DB / Logs Save
[*] Convert UTC to local TZ
"""
from flask_sqlalchemy import SQLAlchemy
import pytz
import datetime
from tzlocal import get_localzone

db = SQLAlchemy()


def insert_timestamp():
    """Get Current time in local timezone and convert it to UTC TIMESTAMP"""
    user_timezone = pytz.timezone(get_localzone().zone)
    new_post_date = user_timezone.localize(datetime.datetime.now())
    return new_post_date.astimezone(pytz.utc).timestamp()


def convert_timestamp(timestamp):
    """Convert UTC TIMESTAMP to Local Host Time"""
    utc_date = pytz.utc.localize(datetime.datetime.utcfromtimestamp(timestamp))
    return str(utc_date.astimezone(pytz.timezone(get_localzone().zone)))
