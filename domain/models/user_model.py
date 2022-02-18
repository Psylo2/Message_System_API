from pydantic import BaseModel, validator
from typing import Optional, Union


class UserModel(BaseModel):
    id: Optional[int]
    name: str
    email: bytes
    password: bytes
    create_at:  Optional[Union[float, str]]
    last_login: Optional[float]

    @validator('name')
    def validate_str(cls, v) -> str:
        if not isinstance(v, str):
            raise TypeError("Type must be str")
        return v

    @validator('email', 'password')
    def validate_bytes(cls, v) -> bytes:
        if not isinstance(v, bytes):
            raise TypeError("Type must be bytes")
        return v

