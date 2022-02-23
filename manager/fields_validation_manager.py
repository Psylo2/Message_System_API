import re

from manager.services import FieldsValidationService


class FieldsValidationManager(FieldsValidationService):
    def __init__(self):
        pass

    def is_valid_email(self, email: str) -> bool:
        """Regex Formula for User's Email
        first not dot,
        besides of '@' no dots,
        no more then 2 dots after '@',
        dont finish with dot"""
        if self.__sanitizer(email):
            reg = r"^[a-zA-Z0-9+_.-]+[^\.\_]+[@]+[^\.\_]+[a-zA-Z0-9]+[\w\.\-]+[a-zA-Z]{2,3}$"
            return True if re.match(reg, email) else False

    def is_valid_username(self, string: str) -> bool:
        """Regex Formula for User's Username
        dont start with digits and no digits only
        4 to 12 length"""
        if self.__sanitizer(string):
            reg = r"^([^\d][\w]{4,12})$"
            return True if re.match(reg, string) else False
        return False

    def is_valid_password(self, password: str) -> bool:
        """Regex Formula for User's Password
        at least: 2 Upper, 2 Lower, 4 Digits, 1 Special
        no more then 1 special"""
        if self.__sanitizer(password):
            reg = r"^(?=.{10,15}$)(?=.*[a-z])(?=.*[A-Z])(?=.*[\d])" \
                  r"(?=.*[\!\@\#\$\%\^\&\*\-\=\+\_\<\>\{\}\(\)\[\]\:\;\/\|\~\`\ ]).*$"
            return True if re.match(reg, password) else False
        return False

    def is_valid_login_inputs(self, name_email: str, password: str) -> bool:
        """Regex Formula for User's Username or Email"""
        return True if (self.is_valid_email(name_email) or self.is_valid_username(name_email)) \
                       and self.is_valid_password(password) else False

    def is_valid_msg_inputs(self, string: str) -> bool:
        """Regex Formula for String"""
        return True if self.__sanitizer(string) else False

    @staticmethod
    def __sanitizer(msg: str) -> bool:
        """REGEX Formula for Message control.
        dont start with '< {
        dont end with '> }
        no less then 3 character
        """
        reg = r"^([^\'\<\{\ \-\"]+[\w\!\@\#\$\%\^\&\*\-\=\+\_\'\<\>\{\}\(\)\[\]\:\;\\\/\|\~\`\ ]+[^\'\>\}\ \-])$"
        return True if re.match(reg, msg) else False
