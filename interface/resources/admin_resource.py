from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims

from application.services import AdminUseCaseService

"""Admin:     [*] Grant Admin Privileges, [*] All Users List,
              [*] Watch All Logs, [*] Watch Log by ID, 
              [*] Watch All Logs by Treat Level, 
              [*] Watch All Logs of a User by Treat Level,
              [*] Watch All Logs of a User"""


class AdminUsersList(Resource):
    def __init__(self, *args, use_case: AdminUseCaseService, **kwargs):
        self._use_case = use_case
        super().__init__(*args, **kwargs)

    @jwt_required
    def get(self):
        """All Users List:    [*] Admin privileges only!
                              [*] Display all users data except passwords and emails"""
        try:
            response, status_code = self._use_case.get_users_list(jwt_claims=get_jwt_claims(),
                                                                  admin_id=get_jwt_identity())
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400


class AdminWatchLogs(Resource):
    def __init__(self, *args, use_case: AdminUseCaseService, **kwargs):
        self._use_case = use_case
        super().__init__(*args, **kwargs)

    @jwt_required
    def get(self):
        """Users List:    [*] Admin privileges only!
                          [*] Display all logs"""
        try:
            response, status_code = self._use_case.get_all_logs(jwt_claims=get_jwt_claims(),
                                                                admin_id=get_jwt_identity())
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400


class AdminSearchByLogId(Resource):
    def __init__(self, *args, use_case: AdminUseCaseService, **kwargs):
        self._use_case = use_case
        super().__init__(*args, **kwargs)

    @jwt_required
    def post(self, log_id: int):
        """Search Log by Log.idx:    [*] Admin privileges only!
                                     [*] Display a log by its id"""
        try:
            response, status_code = self._use_case.get_log_by_id(jwt_claims=get_jwt_claims(),
                                                                 admin_id=get_jwt_identity(),
                                                                 log_id=log_id)
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400


class AdminSearchByThreat(Resource):
    def __init__(self, *args, use_case: AdminUseCaseService, **kwargs):
        self._use_case = use_case
        super().__init__(*args, **kwargs)

    @jwt_required
    def post(self, lvl: str):
        """Search Log by Log.idx:    [*] Admin privileges only!
                                     [*] Display all logs by chosen threat level"""

        try:
            response, status_code = self._use_case.get_all_threats_by_level(jwt_claims=get_jwt_claims(),
                                                                            admin_id=get_jwt_identity(),
                                                                            threat_lvl=lvl)
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400


class AdminSearchByUserId(Resource):
    def __init__(self, *args, use_case: AdminUseCaseService, **kwargs):
        self._use_case = use_case
        super().__init__(*args, **kwargs)

    @jwt_required
    def post(self, user_id: int):
        """Search Log by Log.idx:    [*] Admin privileges only!
                                     [*] Display all logs of a user"""
        try:
            response, status_code = self._use_case.get_all_user_log(jwt_claims=get_jwt_claims(),
                                                                    admin_id=get_jwt_identity(),
                                                                    user_id=user_id)
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400
