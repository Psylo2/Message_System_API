from abc import ABC, abstractmethod
from typing import Dict, List

class LogRepositoryService(ABC):

    @abstractmethod
    def save_log(self, log_data: Dict) -> "LogSchema":
        ...

    @abstractmethod
    def find_by_log_id(self, idx: int) -> "LogSchema":
        ...

    @abstractmethod
    def find_all_logs(self) -> List["LogSchema"]:
        ...

    @abstractmethod
    def find_by_level(self, threat_lvl: str) -> "LogSchema":
        ...

    @abstractmethod
    def find_user_logs(self, idx: int) -> "LogSchema":
        ...

    @abstractmethod
    def insert_timestamp(self) -> float:
        ...

    @abstractmethod
    def convert_timestamp(self, timestamp: float) -> str:
        ...
