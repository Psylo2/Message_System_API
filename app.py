from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv(".env", verbose=True)

from manager import RepositoryManager, JWTConfigurationManager

repository = RepositoryManager()

from factory import Factory
from application.handlers import UserHandler, MessageHandler, LogHandler, AdminHandler
from resources.user_resource import (UserRegister, UserLogin, UserLogout, TokenRefresh, UserForgetPassword, UserDelete)
from resources.admin_resource import (AdminUsersList, AdminWatchLogs, AdminSearchByLogId, AdminSearchByThreat,
                                      AdminSearchByUserId)
from resources.message_resource import (MessageSend, MessageRead, MessageAllUnread, MessageAllRead, MessageAllReceived,
                                        MessageAllSent, MessageReadByRec)

app = Flask(__name__)

app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")

api = Api(app)

jwt = JWTManager(app)
JWTConfigurationManager(jwt=jwt)

factory = Factory()
log_handler = LogHandler(factory=factory)
user_handler = UserHandler(factory=factory, log_handler=log_handler, repository=repository)
message_handler = MessageHandler(factory=factory, log_handler=log_handler)
_admin_handler = AdminHandler(factory=factory, log_handler=log_handler)

# resources.user
api.add_resource(UserRegister, '/register',
                 resource_class_kwargs={"handler": user_handler})
api.add_resource(UserLogin, '/login',
                 resource_class_kwargs={"handler": user_handler})
api.add_resource(UserLogout, '/logout',
                 resource_class_kwargs={"handler": user_handler})
api.add_resource(TokenRefresh, '/refresh',
                 resource_class_kwargs={"handler": user_handler})
api.add_resource(UserForgetPassword, '/forgot_password',
                 resource_class_kwargs={"handler": user_handler})
api.add_resource(UserDelete, '/delete',
                 resource_class_kwargs={"handler": user_handler})

# resources.message
api.add_resource(MessageSend, '/msg/send',
                 resource_class_kwargs={"handler": message_handler})
api.add_resource(MessageRead, '/msg/id=<int:msg_id>',
                 resource_class_kwargs={"handler": message_handler})
api.add_resource(MessageAllUnread, '/msg/all_unread',
                 resource_class_kwargs={"handler": message_handler})
api.add_resource(MessageAllRead, '/msg/all_read',
                 resource_class_kwargs={"handler": message_handler})
api.add_resource(MessageAllReceived, '/msg/all_received',
                 resource_class_kwargs={"handler": message_handler})
api.add_resource(MessageAllSent, '/msg/all_sent',
                 resource_class_kwargs={"handler": message_handler})
api.add_resource(MessageReadByRec, '/msg/all_receivers_read',
                 resource_class_kwargs={"handler": message_handler})

# resources.admin
api.add_resource(AdminUsersList, '/admin_users_list',
                 resource_class_kwargs={"handler": _admin_handler})
api.add_resource(AdminWatchLogs, '/logs/all',
                 resource_class_kwargs={"handler": _admin_handler})
api.add_resource(AdminSearchByLogId, '/logs/id=<int:log_id>',
                 resource_class_kwargs={"handler": _admin_handler})
api.add_resource(AdminSearchByThreat, '/logs/level=<string:lvl>',
                 resource_class_kwargs={"handler": _admin_handler})
api.add_resource(AdminSearchByUserId, '/logs/user=<int:user_id>',
                 resource_class_kwargs={"handler": _admin_handler})

if __name__ == '__main__':
    repository.db.init_app(app)
    app.run(port=5000)
