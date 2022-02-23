from abc import ABC, abstractmethod
from typing import Dict, Tuple


class UserUseCaseService(ABC):

    @abstractmethod
    def user_register(self, user_data: Dict) -> Tuple:
        ...

    @abstractmethod
    def user_login(self, user_data: Dict) -> Tuple:
        ...

    @abstractmethod
    def user_logout(self) -> Tuple:
        ...

    @abstractmethod
    def user_refresh_token(self) -> Tuple:
        ...

    @abstractmethod
    def user_forgot_password(self, user_data: Dict) -> Tuple:
        ...

    @abstractmethod
    def user_delete(self) -> Tuple:
        ...