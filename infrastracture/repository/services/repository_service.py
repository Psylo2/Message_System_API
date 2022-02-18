from abc import abstractmethod
from typing import Dict


class RepositoryService:

    @abstractmethod
    def add_to_repository(self) -> None:
        ...

    @abstractmethod
    def remove_from_repository(self) -> None:
        ...

    @abstractmethod
    def update_repository(self) -> None:
        ...

    @abstractmethod
    def dict(self) -> Dict:
        ...
