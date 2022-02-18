from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (get_raw_jwt, get_jwt_identity,
                                create_access_token, create_refresh_token)

from typing import Dict, Tuple

from application.usecases import UserUseCase
from application.services import UserHandlerService
from domain.models import UserModel


class UserHandler(UserUseCase, UserHandlerService):
    def __init__(self, factory, log_handler, black_list):
        self._user_repository = factory.get_user_repository()
        self._field_validation = factory.get_field_validation()
        self._string_manager = factory.get_string_manager()
        self._log_handler = log_handler
        self.__black_list = black_list

    def user_register(self, user_data: Dict) -> Tuple:
        if not self._is_valid_input(user_data=user_data):
            return {'message': self._string_manager.gettext("invalid_credentials")}, 401

        if self._is_user_name_exist(name=user_data['name']):
            return {'message': self._string_manager.gettext("user_name_exists")}, 401

        self._user_register(user_data=user_data)

        return {'message': self._string_manager.gettext("user_registered")}, 201

    def user_login(self, user_data: Dict) -> Tuple:
        if not self._field_validation.is_valid_login_inputs(user_data['username_email'], user_data['password']):
            return {'message': self._string_manager.gettext("invalid_credentials")}, 401

        user = self._get_user_from_repository(user_data=user_data['username_email'])
        if not user:
            return {'message': self._string_manager.gettext("invalid_credentials")}, 401

        login_attempt, status_code = self._attempt_login(user=user, password=user_data['password'])
        return login_attempt, status_code

    def user_logout(self) -> Tuple:
        self._insert_token_to_blacklist()
        user = self._user_repository.find_by_id(id=get_jwt_identity())
        self._log_handler.low_priority_log(id=user.id, msg="User Logout Successfully")

        return {"message": self._string_manager.gettext("user_logout")}, 200

    def user_refresh_token(self) -> Tuple:
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        self._log_handler.high_priority_log(id=get_jwt_identity(), msg="User has Refreshed an Access Token")
        return {"access_token": new_token}, 200

    def user_forgot_password(self, user_data: Dict) -> Tuple:
        if not self._is_valid_input(user_data=user_data):
            return {'message': self._string_manager.gettext("invalid_credentials")}, 401

        user_by_name, user_by_email = self._get_user_name_and_email(name=user_data['name'],
                                                                    email=user_data['email'])

        if self._is_eligible_data(user_name=user_by_name, user_email=user_by_email,
                                  new_password=user_data['new_password'], re_password=user_data['re_password']):
            password_attempt, status_code = self._attempt_change_password(user=user_by_name,
                                                                          new_password=user_data['new_password'])
            return password_attempt, status_code
        else:
            return {'message': self._string_manager.gettext("invalid_credentials")}, 400

    def user_delete(self) -> Tuple:
        user = self._get_user_by_id(user_id=get_jwt_identity())
        self._insert_token_to_blacklist()
        self._log_handler.high_priority_log(id=user.id,
                                            msg="User been Deleted and token been revoked")
        self._user_repository.delete_from_repository(user_data=user)

        return {"message": self._string_manager.gettext("user_logout")}, 200

    def _user_register(self, user_data: Dict) -> None:
        self._user_repository.encrypt_fields(user_data=user_data)
        user = UserModel(**user_data)
        saved_user = self._save_user(user=user)
        self._log_handler.low_priority_log(id=saved_user.id, msg="User Registered Successfully")

    def _attempt_change_password(self, user, new_password) -> Tuple:
        is_user_admin = user.id == 1

        if is_user_admin:
            self._log_handler.high_priority_log(id=user.id,
                                                msg="ADMIN CANNOT CHANGE PASSWORD")
            return {'message': self._string_manager.gettext("admin_password")}, 201

        user.password = new_password
        self._user_repository._update_password(user=user)
        self._log_handler.high_priority_log(id=user.id,
                                            msg=f"User [{user.id}] has Changed Password successfully")
        return {'message': self._string_manager.gettext("password_changed")}, 201

    def _is_valid_input(self, user_data: Dict) -> bool:
        is_valid_username = self._field_validation.is_valid_username(user_data.get('name'))
        is_valid_email = self._field_validation.is_valid_email(user_data.get('email'))
        is_valid_password = self._field_validation.is_valid_password(user_data.get('password') or
                                                                     user_data.get('new_password') )

        return is_valid_username and is_valid_email and is_valid_password

    def _is_user_name_exist(self, name: str) -> bool:
        if self._user_repository.find_by_username(name):
            return True
        return False

    def _get_user_from_repository(self, user_data: str) -> "UserRepository":
        user = self._user_repository.find_by_username(user_data)
        if not user:
            user = self._user_repository.find_by_email(user_data)
        return user

    def _get_user_name_and_email(self, name: str, email: str) -> Tuple:
        name = self._user_repository.find_by_username(name)
        email = self._user_repository.find_by_email(email)
        return name, email

    def _get_user_by_id(self, user_id) -> "UserRepository":
        return self._user_repository.find_by_id(user_id)

    def _save_user(self, user: UserModel) -> 'UserRepository':
        user.last_login = self._user_repository.insert_timestamp()
        user = self._user_repository.save_user(user_data=user.dict())
        return user

    def _attempt_login(self, user, password: str) -> Tuple:
        if not self._user_repository.decrypt(password, user.password):
            return {"message": self._string_manager.gettext("invalid_credentials")}, 401

        token_login = self._get_tokens(user_id=user.id)
        self._log_handler.low_priority_log(id=user.id,
                                           msg="User Logged in Successfully")
        return token_login, 200


    def _is_eligible_data(self, user_name, user_email, new_password, re_password) -> bool:
        is_password_match = safe_str_cmp(new_password, re_password)
        return user_name and user_email and is_password_match

    def _get_tokens(self, user_id: int) -> Dict:
        access_token = create_access_token(identity=user_id, fresh=True)
        refresh_token = create_refresh_token(identity=user_id)
        return {"access_token": access_token, "refresh_token": refresh_token}

    def _insert_token_to_blacklist(self) -> None:
        jti = get_raw_jwt()["jti"]
        self.__black_list.add(jti)
