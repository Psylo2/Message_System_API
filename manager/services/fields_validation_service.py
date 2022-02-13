from abc import ABC, abstractmethod


class FieldsValidationService(ABC):

    @abstractmethod
    def is_valid_email(self, email: str) -> bool:
        ...

    @abstractmethod
    def is_valid_username(self, string: str) -> bool:
        ...

    @abstractmethod
    def is_valid_password(self, password: str) -> bool:
        ...

    @abstractmethod
    def is_valid_login_inputs(self, name_email: str, password: str) -> bool:
        ...

    @abstractmethod
    def is_valid_msg_inputs(self, string: str) -> bool:
        ...

