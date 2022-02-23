from abc import ABC, abstractmethod
from typing import Dict, Tuple


class AdminUseCaseService(ABC):

    @abstractmethod
    def get_users_list(self, jwt_claims: Dict, admin_id: int) -> Tuple:
        ...

    @abstractmethod
    def get_all_logs(self, jwt_claims: Dict, admin_id: int) -> Tuple:
        ...

    @abstractmethod
    def get_log_by_id(self, jwt_claims: Dict, admin_id: int, log_id: int) -> Tuple:
        ...

    @abstractmethod
    def get_all_threats_by_level(self, jwt_claims: Dict, admin_id: int, threat_lvl: str) -> Tuple:
        ...

    @abstractmethod
    def get_all_user_log(self, jwt_claims: Dict, admin_id: int, user_id: int) -> Tuple:
        ...
