from abc import ABC, abstractmethod
from typing import List, Dict


class UserRepositoryService(ABC):

    @abstractmethod
    def save_user(self, user_data: Dict) -> "UserSchema":
        ...

    @abstractmethod
    def delete_user(self, user) -> None:
        ...

    @abstractmethod
    def find_by_id(self, idx: int) -> "UserSchema":
        ...

    @abstractmethod
    def find_by_username(self, name: str) -> "UserSchema":
        ...

    @abstractmethod
    def find_by_email(self, email: str) -> "UserSchema":
        ...

    @abstractmethod
    def find_all_not_u(self, idx: int) -> "UserSchema":
        ...

    @abstractmethod
    def _update_password(self, new: str) -> None:
        ...

    @abstractmethod
    def _get_all_users(self) -> List["UserSchema"]:
        ...

    @abstractmethod
    def _encrypt_fields(self, user_data: Dict) -> None:
        ...

    @abstractmethod
    def insert_timestamp(self) -> float:
        ...

    @abstractmethod
    def convert_timestamp(self, timestamp: float) -> str:
        ...
