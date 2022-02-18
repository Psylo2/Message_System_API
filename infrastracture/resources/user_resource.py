from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import jwt_required, jwt_refresh_token_required


class UserRegister(Resource):
    def __init__(self, *args, handler, **kwargs):
        self._handler = handler
        self._parser = RequestParser()
        super().__init__(*args, **kwargs)

    def post(self):
        """Register: [*] Validate inputs
                     [*] Confirm user not already exists
                     [*] Save user to DB"""

        self._parser.add_argument('name',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank.")
        self._parser.add_argument('password',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank.")
        self._parser.add_argument('email',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank.")

        try:
            data = self._parser.parse_args()
            response, status_code = self._handler.user_register(user_data=data)
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400


class UserLogin(Resource):
    def __init__(self, *args, handler, **kwargs):
        self._handler = handler
        self._parser = RequestParser()
        super().__init__(*args, **kwargs)

    def post(self):
        """Login:     [*] Validate inputs
                      [*] Confirm user exists by name or email, and password
                      [*] Save user to DB
                      [*] Create Access % Refresh Tokens by user.idx as identity """

        self._parser.add_argument('username_email',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank.")
        self._parser.add_argument('password',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank.")

        try:
            data = self._parser.parse_args()
            response, status_code = self._handler.user_login(user_data=data)
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400


class UserLogout(Resource):
    def __init__(self, *args, handler, **kwargs):
        self._handler = handler
        super().__init__(*args, **kwargs)

    @jwt_required
    def post(self):
        """Logout:    [*] User must possess Access Token
                      [*] Take user uuid token identity
                      [*] Insert to Black list for revoke Token"""
        try:
            response, status_code = self._handler.user_logout()
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400


class TokenRefresh(Resource):
    def __init__(self, *args, handler, **kwargs):
        self._handler = handler
        super().__init__(*args, **kwargs)

    @jwt_refresh_token_required
    def get(self):
        """Token Refresh:
                          [*] Recreate Access Token by user Identity"""
        try:
            response, status_code = self._handler.user_refresh_token()
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400


class UserForgetPassword(Resource):
    def __init__(self, *args, handler, **kwargs):
        self._handler = handler
        self._parser = RequestParser()
        super().__init__(*args, **kwargs)

    def post(self):
        """Retrive Password:     [*] Validate inputs
                                 [*] Confirm user exists by name or email
                                 [*] Verify Password
                                 [*] Update user.password to DB"""

        self._parser.add_argument('name',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank.")
        self._parser.add_argument('email',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank.")
        self._parser.add_argument('new_password',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank.")
        self._parser.add_argument('re_password',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank.")

        data = self._parser.parse_args()
        try:
            response, status_code = self._handler.user_forgot_password(user_data=data)
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400


class UserDelete(Resource):
    def __init__(self, *args, handler, **kwargs):
        self._handler = handler
        super().__init__(*args, **kwargs)

    @jwt_required
    def post(self):
        """Logout:    [*] User must possess Access Token
                      [*] Take user uuid token identity
                      [*] Insert to Black list for revoke Token"""

        try:
            response, status_code = self._handler.user_delete()
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400
