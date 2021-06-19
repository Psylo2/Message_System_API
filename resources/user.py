from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (jwt_required, get_raw_jwt,
                                get_jwt_identity, create_access_token,
                                jwt_refresh_token_required,
                                create_refresh_token)
from flask_restful import Resource, reqparse
from libs.blacklist import BLACKLIST
from libs.strings import gettext, lang_change
from libs.inputs_validation import (valid_email, valid_username,
                                    valid_password, valid_login_inputs,
                                    valid_msg_inputs)
from db.data_base import insert_timestamp
from models.user import UserModel
from models.log import LogModel

"""User:      [*] Register
              [*] Login
              [*] Logout
              [*] Refresh Access Token
              [*] Change Password"""


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help=gettext("field_not_blank"))
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help=gettext("field_not_blank"))
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help=gettext("field_not_blank"))

    @classmethod
    def post(cls):
        """Register: [*] Validate inputs
                     [*] Confirm user not already exists
                     [*] Save user to DB"""
        data = UserRegister.parser.parse_args()
        if not valid_username(data['username']):
            return {'message': gettext("username_error")}, 400
        if not valid_email(data['email']):
            return {'message': gettext("email_error")}, 400
        if not valid_password(data['password']):
            return {'message': gettext("password_error")}, 400
        if UserModel.find_by_username(data['username']):
            return {'message': gettext("user_name_exists")}, 400
        if UserModel.find_by_email(data['email']):
            return {'message': gettext("user_email_taken")}, 400
        user = UserModel(data['username'],
                         data['email'],
                         data['password'])
        user.create_at = insert_timestamp()
        user.save_to_db()
        LogModel(user.idx,
                 "User Registered Successfully",
                 'L').save_to_db()
        return {'message': gettext("user_registered")}, 201


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username_email',
                        type=str,
                        required=True,
                        help=gettext("field_not_blank")
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help=gettext("field_not_blank")
                        )

    def post(self):
        """Login:     [*] Validate inputs
                      [*] Confirm user exists by name or email, and password
                      [*] Save user to DB
                      [*] Create Access % Refresh Tokens by user.idx as identity """
        data = UserLogin.parser.parse_args()
        if not valid_login_inputs(data['username_email'], data['password']):
            return {'message': gettext("input_error")}, 400

        user = UserModel.find_by_username(data['username_email'])
        if user is None:
            user = UserModel.find_by_email(data['username_email'])

        if user and user.decrypt(
                data['password'], user.password):
            user.last_login = insert_timestamp()
            try:
                user.save_to_db()
                access_token = create_access_token(
                    identity=user.idx,
                    fresh=True)
                refresh_token = create_refresh_token(user.idx)
                LogModel(user.idx,
                         f"User Logged in Successfully",
                         'L').save_to_db()
                return {"access_token": access_token,
                        "refresh_token": refresh_token}, 200
            except Exception as e:
                LogModel(user.idx,
                         e,
                         'M').save_to_db()
        return {"message": gettext("invalid_credentials")}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        """Logout:    [*] User must possess Access Token
                      [*] Take user uuid token identity
                      [*] Insert to Black list for revoke Token"""
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        LogModel(get_jwt_identity(),
                 f'User Token have been Revoked Successfully',
                 'L').save_to_db()
        return {"message": gettext("user_logout")}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def get(cls):
        """Token Refresh:
                          [*] Recreate Access Token by user Identity"""
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        LogModel(get_jwt_identity(),
                 f"User has Refreshed an Access Token",
                 'H').save_to_db()
        return {"access_token": new_token}, 200


class UserForgetPassword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help=gettext("field_not_blank")
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help=gettext("field_not_blank")
                        )
    parser.add_argument('new_password',
                        type=str,
                        required=True,
                        help=gettext("field_not_blank")
                        )
    parser.add_argument('re_password',
                        type=str,
                        required=True,
                        help=gettext("field_not_blank")
                        )

    def post(self):
        """Retrive Password:     [*] Validate inputs
                                 [*] Confirm user exists by name or email
                                 [*] Verify Password
                                 [*] Update user.password to DB"""

        data = UserForgetPassword.parser.parse_args()
        if not valid_username(data['username']):
            return {'message': gettext("username_error")}, 400
        if not valid_email(data['email']):
            return {'message': gettext("email_error")}, 400
        if not valid_password(data['new_password']):
            return {'message': gettext("password_error")}, 400
        if not valid_password(data['re_password']):
            return {'message': gettext("password_error")}, 400

        user = UserModel.find_by_email(data['email'])
        user2 = UserModel.find_by_username(data['username'])

        if user and user2 and safe_str_cmp(data['new_password'],
                                           data['re_password']):

            if user.idx != 1:
                user._update_password(data['new_password'])
                LogModel(user.idx,
                         f"User [{user.idx}] has Changed Password successfully",
                         'M').save_to_db()
                return {'message': gettext("password_changed")}, 201
            else:
                LogModel(user.idx,
                         "ADMIN CANNOT CHANGE PASSWORD",
                         'H').save_to_db()
                return {'message': gettext("admin_password")}, 201
        else:
            return {'message': gettext("invalid_credentials")}, 400
