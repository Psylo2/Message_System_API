"""this file is made for
[*] Handling Authentications inputs
[*] Add Complexity to Passwords
[*] Handling MESSAGE Inputs

"""
import re

from models.log import LogModel


def valid_email(email: str):
    """Regex Formula for User's Email
    first not dot,
    besides of '@' no dots,
    no more then 2 dots after '@',
    dont finish with dot"""
    if __sanitizer(email):
        reg = r"^[a-zA-Z0-9+_.-]+[^\.\_]+[@]+[^\.\_]+[a-zA-Z0-9]+[\w\.\-]+[a-zA-Z]{2,3}$"
        return True if re.match(reg, email) else False


def valid_username(string: str):
    """Regex Formula for User's Username
    dont start with digits and no digits only
    4 to 12 length"""
    if __sanitizer(string):
        reg = r"^([^\d][\w]{4,12})$"
        return True if re.match(reg, string) else False
    return False


def valid_password(password: str):
    """Regex Formula for User's Password
    at least: 2 Upper, 2 Lower, 4 Digits, 1 Special
    no more then 1 special"""
    if __sanitizer(password):
        reg = "^(?=.{10,15}$)(?=.*[a-z])(?=.*[A-Z])(?=.*[\d])(?=.*[\!\@\#\$\%\^\&\*\-\=\+\_\<\>\{\}\(\)\[\]\:\;\/\|\~\`\ ]).*$"
        return True if re.match(reg, password) else False
    return False


def valid_login_inputs(name_email: str, password: str):
    """Regex Formula for User's Username or Email"""
    return True if __sanitizer(name_email) and __sanitizer(password) else False


def valid_msg_inputs(string: str):
    """Regex Formula for User's Username or Email"""
    return True if __sanitizer(string) else False


def __sanitizer(msg: str):
    """REGEX Formula for Message control.
    dont start with '<{
    dont end with '>}
    no less then 3 character
    """
    reg = r"^([^\'\<\{]+[\w\!\@\#\$\%\^\&\*\-\=\+\_\'\<\>\{\}\(\)\[\]\:\;\\\/\|\~\`\ ]+[^\'\>\}])$"
    if not re.match(reg, msg):
        LogModel(None,
                 f"sanitizer: {msg} ",
                 'H').save_to_db()
        return False
    else:
        return True
