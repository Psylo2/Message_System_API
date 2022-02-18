from abc import ABC, abstractmethod

class StringManagerService(ABC):

    @abstractmethod
    def refresh_cache(self) -> None:
        ...

    @abstractmethod
    def gettext(self, name) -> str:
        ...
