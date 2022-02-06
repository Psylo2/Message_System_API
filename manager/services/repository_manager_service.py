from abc import ABC, abstractmethod

class RepositoryService(ABC):

    @abstractmethod
    def db(self):
        ...

    @abstractmethod
    def encrypt(self, string: str) -> bytes:
        ...

    @abstractmethod
    def decrypt(self, x: bytes, y: bytes) -> bool:
        ...

    @abstractmethod
    def insert_timestamp(self) -> float:
        ...

    @abstractmethod
    def convert_timestamp(self, timestamp) -> str:
        ...
