from abc import ABC, abstractmethod
from typing import Tuple, Dict


class UserHandlerService(ABC):

    @abstractmethod
    def _attempt_change_password(self, user, new_password) -> Tuple:
        ...

    @abstractmethod
    def _is_valid_input(self, user_data: Dict) -> bool:
        ...

    @abstractmethod
    def _is_user_name_exist(self, name: str) -> bool:
        ...

    @abstractmethod
    def _get_user_from_repository(self, user_data: str) -> "UserModel":
        ...

    @abstractmethod
    def _get_user_name_and_email(self, name: str, email: str) -> Tuple:
        ...

    @abstractmethod
    def _get_user_by_id(self, user_id) -> "UserSchema":
        ...

    @abstractmethod
    def _save_user(self, user: "UserModel") -> 'UserSchema':
        ...

    @abstractmethod
    def _is_eligible_data(self, user_name, user_email, new_password, re_password) -> bool:
        ...

    @abstractmethod
    def _attempt_login(self, user, password: str) -> Tuple:
        ...

    @abstractmethod
    def _get_tokens(self, user_id: int) -> Dict:
        ...

    @abstractmethod
    def _insert_token_to_blacklist(self) -> None:
        ...
