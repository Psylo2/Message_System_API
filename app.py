from dotenv import load_dotenv

load_dotenv(".env", verbose=True)

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from manager import AppConfigurations
from manager.blacklist_manager import BLACKLIST

from infrastracture.repository import repository
from factory import Factory
from application.handlers import *
from infrastracture.resources import *

app = Flask(__name__)
app_configuration = AppConfigurations(app=app, repository=repository)

jwt = JWTManager(app)
app_configuration.jwt_configuration(jwt=jwt)

api = Api(app)

factory = Factory()


# handlers
log_handler = LogHandler(factory=factory)
user_handler = UserHandler(factory=factory, log_handler=log_handler, black_list=BLACKLIST)
message_handler = MessageHandler(factory=factory, log_handler=log_handler)
admin_handler = AdminHandler(factory=factory, log_handler=log_handler)

# resources.user
api.add_resource(UserRegister,
                 '/register',
                 resource_class_kwargs={"handler": user_handler})

api.add_resource(UserLogin,
                 '/login',
                 resource_class_kwargs={"handler": user_handler})

api.add_resource(UserForgetPassword,
                 '/forgot_password',
                 resource_class_kwargs={"handler": user_handler})

api.add_resource(UserLogout,
                 '/logout',
                 resource_class_kwargs={"handler": user_handler})

api.add_resource(TokenRefresh,
                 '/refresh',
                 resource_class_kwargs={"handler": user_handler})

api.add_resource(UserDelete,
                 '/delete',
                 resource_class_kwargs={"handler": user_handler})

# resources.message
api.add_resource(MessageSend,
                 '/msg/send',
                 resource_class_kwargs={"handler": message_handler})

api.add_resource(MessageRead,
                 '/msg/id=<int:msg_id>',
                 resource_class_kwargs={"handler": message_handler})

api.add_resource(MessageAllUnread,
                 '/msg/all_unread',
                 resource_class_kwargs={"handler": message_handler})

api.add_resource(MessageAllRead,
                 '/msg/all_read',
                 resource_class_kwargs={"handler": message_handler})

api.add_resource(MessageAllReceived,
                 '/msg/all_received',
                 resource_class_kwargs={"handler": message_handler})

api.add_resource(MessageAllSent,
                 '/msg/all_sent',
                 resource_class_kwargs={"handler": message_handler})

api.add_resource(MessageReadByRec,
                 '/msg/all_receivers_read',
                 resource_class_kwargs={"handler": message_handler})

# resources.admin
api.add_resource(AdminUsersList,
                 '/admin_users_list',
                 resource_class_kwargs={"handler": admin_handler})

api.add_resource(AdminWatchLogs,
                 '/logs/all',
                 resource_class_kwargs={"handler": admin_handler})

api.add_resource(AdminSearchByLogId,
                 '/logs/id=<int:log_id>',
                 resource_class_kwargs={"handler": admin_handler})

api.add_resource(AdminSearchByThreat,
                 '/logs/level=<string:lvl>',
                 resource_class_kwargs={"handler": admin_handler})

api.add_resource(AdminSearchByUserId,
                 '/logs/user=<int:user_id>',
                 resource_class_kwargs={"handler": admin_handler})


@app.before_first_request
def create_tables():
    app_configuration.repository_create_all_tables()
    app_configuration._add_admin(user_handler=user_handler)


if __name__ == '__main__':
    app.run(port=5000)
