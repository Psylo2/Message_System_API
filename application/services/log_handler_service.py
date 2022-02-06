from abc import ABC, abstractmethod
from typing import Tuple


class LogHandlerServices(ABC):

    @abstractmethod
    def _attempt_change_password(self, user, new_password) -> Tuple:
        ...
