from abc import ABC, abstractmethod

class LogUseCase(ABC):

    @abstractmethod
    def low_priority_log(self, _id: int, msg: str) -> None:
        ...

    @abstractmethod
    def medium_priority_log(self, _id: int, msg: str) -> None:
        ...

    @abstractmethod
    def high_priority_log(self, _id: int, msg: str) -> None:
        ...
