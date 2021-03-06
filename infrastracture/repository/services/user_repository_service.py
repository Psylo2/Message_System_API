from abc import ABC, abstractmethod
from typing import List, Dict


class UserRepositoryService(ABC):

    @abstractmethod
    def save_user(self, user_data: Dict) -> "UserRepository":
        ...

    @abstractmethod
    def delete_user(self, user) -> None:
        ...

    @abstractmethod
    def find_by_id(self, idx: int) -> "UserRepository":
        ...

    @abstractmethod
    def find_by_username(self, name: str) -> "UserRepository":
        ...

    @abstractmethod
    def find_by_email(self, email: str) -> "UserRepository":
        ...

    @abstractmethod
    def find_all_not_u(self, idx: int) -> "UserRepository":
        ...

    @abstractmethod
    def _update_password(self, new: str) -> None:
        ...

    @abstractmethod
    def _get_all_users(self) -> List["UserRepository"]:
        ...

    @abstractmethod
    def encrypt_fields(self, user_data: Dict) -> None:
        ...

    @abstractmethod
    def insert_timestamp(self) -> float:
        ...

    @abstractmethod
    def convert_timestamp(self, timestamp: float) -> str:
        ...
