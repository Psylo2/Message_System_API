from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv(".env", verbose=True)

from db.database import db
from libs.blacklist import BLACKLIST
from resources.user import (UserRegister, UserLogin,
                            UserLogout, TokenRefresh,
                            UserForgetPassword)
from resources.admin import (AdminUsersList, AdminWatchLogs,
                             AdminSearchByLogId, AdminSearchByThreat,
                             AdminSearchUserThreat, AdminSearchByUserId)

from resources.message import (MessageSend, MessageRead, MessageAllUnread,
                               MessageAllRead, MessageAllReceived,
                               MessageAllSent, MessageReadByRec)

app = Flask(__name__)

app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")

api = Api(app)

jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """Check if JWT Token is in BlackList"""
    return decrypted_token["jti"] in BLACKLIST


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    """Check if identity is Admin
    for ADMIN privileges"""
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


# resources.user
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserForgetPassword, '/forgot_password')

# resources.admin
api.add_resource(AdminUsersList, '/admin_users_list')
api.add_resource(AdminWatchLogs, '/logs/all')
api.add_resource(AdminSearchByLogId, '/logs/id=<int:log_id>')
api.add_resource(AdminSearchByThreat, '/logs/level=<string:lvl>')
api.add_resource(AdminSearchUserThreat, '/logs/id=<int:user_id>&level=<string:lvl>')
api.add_resource(AdminSearchByUserId, '/logs/user=<int:user_id>')

# resources.message
api.add_resource(MessageSend, '/msg/send')
api.add_resource(MessageRead, '/msg/id=<int:msg_id>')
api.add_resource(MessageAllUnread, '/msg/all_unread')
api.add_resource(MessageAllRead, '/msg/all_read')
api.add_resource(MessageAllReceived, '/msg/all_received')
api.add_resource(MessageAllSent, '/msg/all_sent')
api.add_resource(MessageReadByRec, '/msg/all_receivers_read')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000)
