import os

import bcrypt
import pytz
from datetime import datetime
from tzlocal import get_localzone

from application.core.services import RepositoryService


class RepositoryManager(RepositoryService):

    def encrypt(self, string: str) -> bytes:
        """Encrypt given string"""
        key = int(os.environ.get('SALT_KEY'))
        generate_salt_key = bcrypt.gensalt(key)
        return bcrypt.hashpw(string.encode("UTF-8"), generate_salt_key)

    def decrypt(self, x: str, y: bytes) -> bool:
        """Match 2 hash to Verify string context """
        return bcrypt.checkpw(x.encode("UTF-8"), y)

    def insert_timestamp(self) -> float:
        """Get Current time in local timezone and convert it to UTC TIMESTAMP"""
        user_timezone = pytz.timezone(get_localzone().zone)
        new_post_date = user_timezone.localize(datetime.now())
        return new_post_date.astimezone(pytz.utc).timestamp()

    def convert_timestamp(self, timestamp: float) -> str:
        """Convert UTC TIMESTAMP to Local Host Time"""
        convert_to_utc_timestamp = datetime.utcfromtimestamp(timestamp)
        utc_date = pytz.utc.localize(convert_to_utc_timestamp)
        return str(utc_date.astimezone(pytz.timezone(get_localzone().zone)))
