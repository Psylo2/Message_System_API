from dotenv import load_dotenv

load_dotenv(".env", verbose=True)

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from application.core import (AppConfigurations, JWTConfigurationManager, RepositoryManager, StringManager,
                              FieldsValidationManager, BLACKLIST)
from application.usecases import LogUseCase, UserUseCase, MessageUseCase, AdminUseCase
from interface.resources import *

from infrastracture.repository import repository
from infrastracture.repository.queries import LogRepositoryQueries, UserRepositoryQueries, MessageRepositoryQueries

app = Flask(__name__)
app_configuration = AppConfigurations(app=app, repository=repository)

jwt = JWTManager(app)
JWTConfigurationManager(jwt=jwt)

api = Api(app)

# Manager Services
repository_manager_service = RepositoryManager()
field_validation_manager_service = FieldsValidationManager()
string_manager_service = StringManager()

# Repository Queries
log_repository_queries = LogRepositoryQueries(repository_services=repository_manager_service)
user_repository_queries = UserRepositoryQueries(repository_services=repository_manager_service)
message_repository_queries = MessageRepositoryQueries(repository_services=repository_manager_service)

# Use Cases
log_use_case = LogUseCase(logs_repository_service=log_repository_queries)

user_use_case = UserUseCase(user_repository_service=user_repository_queries,
                            log_use_case_service=log_use_case,
                            field_validation_service=field_validation_manager_service,
                            string_manager_service=string_manager_service,
                            black_list=BLACKLIST)

message_use_case = MessageUseCase(message_repository_service=message_repository_queries,
                                  user_repository_service=user_repository_queries,
                                  log_use_case_service=log_use_case,
                                  field_validation_service=field_validation_manager_service)

admin_use_case = AdminUseCase(user_repository_service=user_repository_queries,
                              logs_repository_service=log_repository_queries,
                              log_use_case_service=log_use_case)

# User Interface
api.add_resource(UserRegister,
                 '/register',
                 resource_class_kwargs={"use_case": user_use_case})

api.add_resource(UserLogin,
                 '/login',
                 resource_class_kwargs={"use_case": user_use_case})

api.add_resource(UserForgetPassword,
                 '/forgot_password',
                 resource_class_kwargs={"use_case": user_use_case})

api.add_resource(UserLogout,
                 '/logout',
                 resource_class_kwargs={"use_case": user_use_case})

api.add_resource(TokenRefresh,
                 '/refresh',
                 resource_class_kwargs={"use_case": user_use_case})

api.add_resource(UserDelete,
                 '/delete',
                 resource_class_kwargs={"use_case": user_use_case})

# Message Interface
api.add_resource(MessageSend,
                 '/msg/send',
                 resource_class_kwargs={"use_case": message_use_case})

api.add_resource(MessageRead,
                 '/msg/id=<int:msg_id>',
                 resource_class_kwargs={"use_case": message_use_case})

api.add_resource(MessageAllUnread,
                 '/msg/all_unread',
                 resource_class_kwargs={"use_case": message_use_case})

api.add_resource(MessageAllRead,
                 '/msg/all_read',
                 resource_class_kwargs={"use_case": message_use_case})

api.add_resource(MessageAllReceived,
                 '/msg/all_received',
                 resource_class_kwargs={"use_case": message_use_case})

api.add_resource(MessageAllSent,
                 '/msg/all_sent',
                 resource_class_kwargs={"use_case": message_use_case})

api.add_resource(MessageReadByRec,
                 '/msg/all_receivers_read',
                 resource_class_kwargs={"use_case": message_use_case})

# Admin Interface
api.add_resource(AdminUsersList,
                 '/admin_users_list',
                 resource_class_kwargs={"use_case": admin_use_case})

api.add_resource(AdminWatchLogs,
                 '/logs/all',
                 resource_class_kwargs={"use_case": admin_use_case})

api.add_resource(AdminSearchByLogId,
                 '/logs/id=<int:log_id>',
                 resource_class_kwargs={"use_case": admin_use_case})

api.add_resource(AdminSearchByThreat,
                 '/logs/level=<string:lvl>',
                 resource_class_kwargs={"use_case": admin_use_case})

api.add_resource(AdminSearchByUserId,
                 '/logs/user=<int:user_id>',
                 resource_class_kwargs={"use_case": admin_use_case})


@app.before_first_request
def create_tables():
    app_configuration.repository_create_all_tables()
    app_configuration._add_admin(user_use_case=user_use_case)


if __name__ == '__main__':
    app.run(port=5000)
