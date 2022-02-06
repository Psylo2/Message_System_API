from abc import ABC, abstractmethod
from typing import List, Dict


class AdminHandlerService(ABC):

    @abstractmethod
    def _get_all_users_list(self) -> List[Dict]:
        ...

    @abstractmethod
    def _aggregate_user(self, user: "UserSchema") -> Dict:
        ...

    @abstractmethod
    def _is_admin(self, jwt_claims: Dict) -> bool:
        ...

    @abstractmethod
    def _get_all_logs_list(self) -> List[Dict]:
        ...

    @abstractmethod
    def _aggregate_log(self, log: "LogSchema") -> Dict:
        ...

    @abstractmethod
    def _get_log_by_id(self, log_id: int) -> Dict:
        ...

    @abstractmethod
    def _get_all_logs_by_threats_level(self, threat_lvl: str) -> List[Dict]:
        ...
