from abc import ABC, abstractmethod


class AppConfigurationService(ABC):

    @abstractmethod
    def app(self):
        ...

    @abstractmethod
    def repository(self):
        ...

    @abstractmethod
    def add_configurations(self) -> None:
        ...

    @abstractmethod
    def repository_init_app(self) -> None:
        ...

    @abstractmethod
    def repository_create_all_tables(self) -> None:
        ...

    @abstractmethod
    def _add_admin(self, factory) -> None:
        ...
