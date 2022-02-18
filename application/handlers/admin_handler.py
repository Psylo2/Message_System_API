from typing import Dict, Tuple, List

from application.usecases import AdminUseCase
from application.services import AdminHandlerService


class AdminHandler(AdminUseCase, AdminHandlerService):
    def __init__(self, factory, log_handler):
        self._user_repository = factory.get_user_repository
        self._log_repository = factory.get_log_repository()
        self._log_handler = log_handler

    def get_users_list(self, jwt_claims: Dict, admin_id: int) -> Tuple:
        if not self._is_admin(jwt_claims=jwt_claims):
            self._log_handler.add_high_priority_log(id=admin_id,
                                                    msg=f"User Id: {admin_id} have tried to access Users List")
            return {"message": gettext("admin_privilege")}, 401

        self._log_handler.add_high_priority_log(id=admin_id, msg="Admin access to All Users List")
        return self._get_all_users_list(), 200

    def get_all_logs(self, jwt_claims: Dict, admin_id: int) -> Tuple:
        if not self._is_admin(jwt_claims=jwt_claims):
            self._log_handler.add_high_priority_log(id=admin_id,
                                                    msg=f"User Id: {admin_id} have tried to access Users List")
            return {"message": gettext("admin_privilege")}, 401

        self._log_handler.add_high_priority_log(id=admin_id, msg="Admin access to All Users List")
        return self._get_all_logs_list(), 200

    def get_log_by_id(self, jwt_claims: Dict, admin_id: int, log_id: int) -> Tuple:
        if not self._is_admin(jwt_claims=jwt_claims):
            self._log_handler.add_high_priority_log(id=admin_id,
                                                    msg=f"User Id: {admin_id} have tried to access Users List")
            return {"message": gettext("admin_privilege")}, 401

        self._log_handler.add_high_priority_log(id=admin_id, msg=f"Admin access to Log ID: {log_id}")
        return self._get_log_by_id(log_id=log_id), 200

    def get_all_threats_by_level(self, jwt_claims: Dict, admin_id: int, threat_lvl: str) -> Tuple:
        if not self._is_admin(jwt_claims=jwt_claims):
            self._log_handler.add_high_priority_log(id=admin_id,
                                                    msg=f"User Id: {admin_id} have tried to access Users List")
            return {"message": gettext("admin_privilege")}, 401

        self._log_handler.add_high_priority_log(id=admin_id, msg=f"Admin access to All Threat Log Level: {threat_lvl}")
        return self._get_all_logs_by_threats_level(threat_lvl=threat_lvl), 200

    def get_all_user_log(self, jwt_claims: Dict, admin_id: int, user_id: int) -> Tuple:
        if not self._is_admin(jwt_claims=jwt_claims):
            self._log_handler.add_high_priority_log(id=admin_id,
                                                    msg=f"User Id: {admin_id} have tried to access Users List")
            return {"message": gettext("admin_privilege")}, 401

        self._log_handler.add_high_priority_log(id=admin_id, msg=f"Admin access to All Threat Log Level: {threat_lvl}")
        return self._get_user_logs(user_id=user_id), 200

    def _get_user_logs(self, user_id: int) -> List:
        all_user_logs_list = self._log_repository.find_user_logs(id=user_id)
        return [self._aggregate_log(log=log) for log in all_user_logs_list]

    def _get_all_logs_by_threats_level(self, threat_lvl: str) -> List[Dict]:
        all_logs_by_threat = self._log_repository.find_by_level(threat_lvl=threat_lvl)
        return [self._aggregate_log(log=log) for log in all_logs_by_threat]

    def _get_log_by_id(self, log_id: int) -> Dict:
        log = self._log_repository.find_by_log_id(id=log_id)
        return self._aggregate_log(log=log)

    def _get_all_logs_list(self) -> List[Dict]:
        all_logs_raw_list = self._log_repository.find_all_logs()
        return [self._aggregate_log(log=log) for log in all_logs_raw_list]

    def _aggregate_log(self, log: "LogRepository") -> Dict:
        create_at = self._log_repository.convert_timestamp(log.create_at)
        return {log.id: {"create_at": create_at,
                          "user_id": log.user_id,
                          "action": log.action,
                          "threat_lvl": log.threat_lvl}}

    def _get_all_users_list(self) -> List[Dict]:
        all_users_raw_list = self._user_repository._get_all_users()
        return [self._aggregate_user(user=user) for user in all_users_raw_list]

    def _aggregate_user(self, user: "UserSchema") -> Dict:
        create_at = self._user_repository.convert_timestamp(user.create_at)
        return {user.id: {"name": user.name,
                          "create_at": create_at}}

    def _is_admin(self, jwt_claims: Dict) -> bool:
        if not jwt_claims['is_admin']:
            return False
        return True
