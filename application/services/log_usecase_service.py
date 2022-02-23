from abc import ABC, abstractmethod
from typing import Tuple


class LogUseCaseService(ABC):

    @abstractmethod
    def low_priority_log(self, id: int, msg: str) -> None:
        ...

    @abstractmethod
    def medium_priority_log(self, id: int, msg: str) -> None:
        ...

    @abstractmethod
    def high_priority_log(self, id: int, msg: str) -> None:
        ...
