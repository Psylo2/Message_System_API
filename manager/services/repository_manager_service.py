from abc import ABC, abstractmethod

class RepositoryService(ABC):

    @abstractmethod
    def encrypt(self, string: str) -> bytes:
        ...

    @abstractmethod
    def decrypt(self, x: str, y: bytes) -> bool:
        ...

    @abstractmethod
    def insert_timestamp(self) -> float:
        ...

    @abstractmethod
    def convert_timestamp(self, timestamp) -> str:
        ...
