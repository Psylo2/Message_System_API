from repository import UserRepository, MessageRepository, LogRepository


class Factory:
    def __init__(self):
        self._user_repository = None
        self._message_repository = None
        self._logs_repository = None

    def get_user_repository(self) -> UserRepository:
        if not self._user_repository:
            self._user_repository = UserRepository()
        return self._user_repository

    def get_log_repository(self) -> LogRepository:
        if not self._logs_repository:
            self._logs_repository = LogRepository()
        return self._logs_repository

    def get_message_repository(self) -> MessageRepository:
        if not self._message_repository:
            self._message_repository = MessageRepository()
        return self._message_repository
