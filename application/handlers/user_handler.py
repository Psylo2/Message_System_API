from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (get_raw_jwt, get_jwt_identity,
                                create_access_token, create_refresh_token)

from typing import Dict, Tuple

from usecases import UserUseCase
from application.services import UserHandlerService
from models import UserModel
from libs.blacklist import BLACKLIST
from libs.inputs_validation import valid_email, valid_username, valid_password, valid_login_inputs


class UserHandler(UserUseCase, UserHandlerService):
    def __init__(self, factory, repository, log_handler):
        self._decrypt_repository = repository.decrypt
        self._user_repository = factory.get_user_repository
        self._log_handler = log_handler

    def user_register(self, user_data: Dict) -> Tuple:
        if not self._is_valid_input(user_data=user_data):
            return {'message': "Credentials error"}, 401

        user = UserModel(name=data['username'], email=data['email'], password=data['password'])

        if self._is_user_name_exist(name=user.name):
            return {'message': "User Name is Already in use"}, 401

        user.create_at = self._user_repository.insert_timestamp()
        self._save_user(user=user)
        return {'message': gettext("user_registered")}, 201

    def user_login(self, user_data: Dict) -> Tuple:
        if not valid_login_inputs(data['username_email'], data['password']):
            return {'message': "Credentials error"}, 401

        user = self._get_user_from_repository(user_data=data['username_email'])
        if not user:
            return {'message': "Credentials error"}, 401

        login_attempt, status_code = self._attempt_login(user=user, password=data['password'])
        return login_attempt, status_code

    def user_logout(self) -> Tuple:
        self._insert_token_to_blacklist()
        self._log_handler.add_low_priority_log(_id=get_jwt_identity(), msg="User Registered Successfully")
        return {"message": gettext("user_logout")}, 200

    def user_refresh_token(self) -> Tuple:
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        self._log_handler.add_high_priority_log(_id=get_jwt_identity(), msg="User has Refreshed an Access Token")
        return {"access_token": new_token}, 200

    def user_forgot_password(self, user_data: Dict) -> Tuple:
        if not self._is_valid_input(user_data=user_data):
            return {'message': "Credentials error"}, 401

        user_name, user_email = self._get_user_name_and_email(name=data['username'],
                                                              email=data['email'])

        if self._is_eligible_data(user_name=user_name, user_email=user_email,
                                  new_password=data['new_password'], re_password=data['re_password']):
            password_attempt, status_code = self._attempt_change_password(user=user, new_password=data['password'])
            return password_attempt, status_code
        else:
            return {'message': gettext("invalid_credentials")}, 400

    def user_delete(self) -> Tuple:
        user = self._get_user_by_id(user_id=get_jwt_identity())
        self._insert_token_to_blacklist()
        self._log_handler.add_high_priority_log(_id=user.idx,
                                                msg="User been Deleted and token been revoked")
        self._user_repository.delete_from_repository(user_data=user)

        return {"message": gettext("user_logout")}, 200

    def _attempt_change_password(self, user, new_password) -> Tuple:
        is_user_admin = user.idx == 1

        if is_user_admin:
            self._log_handler.add_high_priority_log(_id=user.idx,
                                                    msg="ADMIN CANNOT CHANGE PASSWORD")
            return {'message': gettext("admin_password")}, 201

        self.factory.get_user_repository._update_password(new_password)
        self._log_handler.add_high_priority_log(_id=user.idx,
                                                msg=f"User [{user.idx}] has Changed Password successfully")
        return {'message': gettext("password_changed")}, 201

    def _is_valid_input(self, user_data: Dict) -> bool:
        is_valid_username = valid_username(user_data.get('username'))
        is_valid_email = valid_email(user_data.get('email'))
        is_valid_password = valid_password(user_data.get('password'))

        return is_valid_username and is_valid_email and is_valid_password

    def _is_user_name_exist(self, name: str) -> bool:
        if self._user_repository.find_by_username(name):
            return True
        return False

    def _get_user_from_repository(self, user_data: str) -> "UserModel":
        user = self._user_repository.find_by_username(user_data)
        if not user:
            user = self._user_repository.find_by_email(user_data)
        return user

    def _get_user_name_and_email(self, name: str, email: str) -> Tuple:
        name = self._user_repository.find_by_username(name)
        email = self._user_repository.find_by_email(email)
        return name, email

    def _get_user_by_id(self, user_id) -> "UserSchema":
        return self._user_repository.find_by_id(user_id)

    def _save_user(self, user: UserModel) -> 'UserSchema':
        user = self.factory.get_user_repository.save_to_repository(user_data=user.dict())
        self._log_handler.add_low_priority_log(_id=user.idx, msg="User Registered Successfully")
        return user

    def _attempt_login(self, user, password: str) -> Tuple:
        if not self._decrypt_repository(password, user.password):
            return {"message": gettext("invalid_credentials")}, 401

        user.last_login = insert_timestamp()
        user_schema = self._save_user(user=user)
        tokens_payload = self._get_tokens(user_id=user_schema.idx)
        self._log_handler.add_low_priority_log(_id=user_schema.idx,
                                               msg="User Logged in Successfully")
        return tokens_payload, 200

    def _is_eligible_data(self, user_name, user_email, new_password, re_password) -> bool:
        is_password_match = safe_str_cmp(new_password, re_password)
        return user_name and user_email and is_password_match

    def _get_tokens(self, user_id: int) -> Dict:
        access_token = create_access_token(identity=user_id, fresh=True)
        refresh_token = create_refresh_token(user_schema.user_id)
        return {"access_token": access_token, "refresh_token": refresh_token}

    def _insert_token_to_blacklist(self) -> None:
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
