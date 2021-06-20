from flask_jwt_extended import (jwt_required,
                                get_jwt_identity,
                                get_jwt_claims)
from flask_restful import Resource
from libs.strings import gettext
from models.user import UserModel
from models.log import LogModel

"""Admin:     [*] Grant Admin Privileges, [*] All Users List,
              [*] Watch All Logs, [*] Watch Log by ID, 
              [*] Watch All Logs by Treat Level, 
              [*] Watch All Logs of a User by Treat Level,
              [*] Watch All Logs of a User"""


class AdminUsersList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        """All Users List:    [*] Admin privileges only!
                              [*] Display all users data except passwords and emails"""
        claims = get_jwt_claims()
        if not claims['is_admin']:
            LogModel(get_jwt_identity(),
                     f"User have tried to access Users List",
                     'H').save_to_db()
            return {"message": gettext("admin_privilege")}, 401
        LogModel(get_jwt_identity(),
                 f"Admin access to All Users List",
                 'H').save_to_db()
        return [user.json() for user in UserModel.query.all()], 200


class AdminWatchLogs(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        """Users List:    [*] Admin privileges only!
                          [*] Display all logs"""
        claims = get_jwt_claims()
        if not claims['is_admin']:
            LogModel(get_jwt_identity(),
                     f"User have tried to access Users List",
                     'H').save_to_db()
            return {"message": gettext("admin_privilege")}, 401
        LogModel(get_jwt_identity(),
                 f"Admin access to All Logs List",
                 'H').save_to_db()
        return [log.json() for log in LogModel.find_all_logs()], 200


class AdminSearchByLogId(Resource):
    @classmethod
    @jwt_required
    def post(cls, log_id: int):
        """Search Log by Log.idx:    [*] Admin privileges only!
                                     [*] Display a log by its id"""
        claims = get_jwt_claims()
        if not claims['is_admin']:
            LogModel(get_jwt_identity(),
                     f"User have tried to access Users List",
                     'H').save_to_db()
            return {"message": gettext("admin_privilege")}, 401
        LogModel(get_jwt_identity(),
                 f"Admin access to Log ID: [{log_id}]",
                 'H').save_to_db()
        return LogModel.find_by_id(log_id).json(), 200


class AdminSearchByThreat(Resource):
    @classmethod
    @jwt_required
    def post(cls, lvl: int):
        """Search Log by Log.idx:    [*] Admin privileges only!
                                     [*] Display all logs by chosen threat level"""
        claims = get_jwt_claims()
        if not claims['is_admin']:
            LogModel(get_jwt_identity(),
                     f"User have tried to access Users List",
                     'H').save_to_db()
            return {"message": gettext("admin_privilege")}, 401
        LogModel(get_jwt_identity(),
                 f"Admin access to All Threat Log Level: [{lvl}]",
                 'H').save_to_db()
        return [log.json() for log in LogModel.find_by_level(lvl)], 200


class AdminSearchUserThreat(Resource):
    @classmethod
    @jwt_required
    def post(cls, user_id: int, lvl: int):
        """Search Log by Log.idx:    [*] Admin privileges only!
                                     [*] Display all logs of user by chosen threat level"""
        claims = get_jwt_claims()
        if not claims['is_admin']:
            LogModel(get_jwt_identity(),
                     f"User have tried to access Users List",
                     'H').save_to_db()
            return {"message": gettext("admin_privilege")}, 401
        LogModel(get_jwt_identity(),
                 f"Admin access to All Log of User: [{user_id}], and Threat Level: [{lvl}]",
                 'H').save_to_db()
        return [log.json() for log in LogModel.find_user_and_level(user_id, lvl)], 200


class AdminSearchByUserId(Resource):
    @classmethod
    @jwt_required
    def post(cls, user_id: int):
        """Search Log by Log.idx:    [*] Admin privileges only!
                                     [*] Display all logs of a user"""
        claims = get_jwt_claims()
        if not claims['is_admin']:
            LogModel(get_jwt_identity(),
                     f"User have tried to access Users List",
                     'H').save_to_db()
            return {"message": gettext("admin_privilege")}, 401
        LogModel(get_jwt_identity(),
                 f"Admin access to all Logs of User: [{user_id}]",
                 'H').save_to_db()
        return [log.json() for log in LogModel.find_by_user_id(user_id)], 200
