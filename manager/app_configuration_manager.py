import os

from manager.jwt_configuration_manager import JWTConfigurationManager
from manager.services import AppConfigurationService


class AppConfigurations(AppConfigurationService):
    def __init__(self, app, repository):
        self._app = app
        self._repository = repository

        self.add_configurations()
        self.repository_init_app()

    @property
    def app(self):
        return self._app

    @property
    def repository(self):
        return self._repository.repository

    def add_configurations(self) -> None:
        self.app.config.from_object("manager.application_settings.application_settings")
        self.app.config.from_envvar("APPLICATION_SETTINGS")

    def repository_init_app(self) -> None:
        self.repository.init_app(app=self.app)

    def repository_create_all_tables(self) -> None:
        self.repository.create_all(app=self.app)

    def jwt_configuration(self, jwt) -> None:
        JWTConfigurationManager(jwt=jwt)

    def _add_admin(self, user_use_case) -> None:
        admin_name = os.environ.get('ADMIN_NAME')
        if not user_use_case._is_user_name_exist(name=admin_name):

            admin = {"id": 1,
                     "name": admin_name,
                     "email": os.environ.get('ADMIN_EMAIL'),
                     "password": os.environ.get('ADMIN_PASSWORD')}
            user_use_case._user_register(user_data=admin)
