from pydantic import BaseModel, validator
from typing import Optional, Union


class UserModel(BaseModel):
    name: str
    email: bytes
    password: bytes
    create_at:  Optional[Union[float, str]]
    last_login: Optional[float]
    active:  bool = False

    @validator('name')
    def validate_str(cls, str_) -> str:
        if not isinstance(str, str_):
            raise TypeError("Type must be str")
        return str_

    @validator('email', 'password')
    def validate_bytes(cls, bytes_) -> bytes:
        if not isinstance(bytes, bytes_):
            raise TypeError("Type must be bytes")
        return bytes_

    @validator('active')
    def validate_bool(cls, bool_) -> bool:
        if not isinstance(bool, bool_):
            raise TypeError("Type must be boolean")
        return bool_
