from infrastracture.repository.controllers import (UserRepositoryController, MessageRepositoryController,
                                                   LogRepositoryController)
from manager import FieldsValidation, StringManager

class Factory:
    def __init__(self):
        self._user_repository = None
        self._message_repository = None
        self._logs_repository = None
        self._field_validation = None
        self._string_manager = None

    def get_user_repository(self) -> UserRepositoryController:
        if not self._user_repository:
            self._user_repository = UserRepositoryController()
        return self._user_repository

    def get_log_repository(self) -> LogRepositoryController:
        if not self._logs_repository:
            self._logs_repository = LogRepositoryController()
        return self._logs_repository

    def get_message_repository(self) -> MessageRepositoryController:
        if not self._message_repository:
            self._message_repository = MessageRepositoryController()
        return self._message_repository

    def get_field_validation(self) -> FieldsValidation:
        if not self._field_validation:
            self._field_validation = FieldsValidation()
        return self._field_validation

    def get_string_manager(self) -> StringManager:
        if not self._string_manager:
            self._string_manager = StringManager()
        return self._string_manager
