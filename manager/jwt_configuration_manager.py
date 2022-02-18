from flask_jwt_extended import JWTManager


from manager.blacklist_manager import BLACKLIST


class JWTConfigurationManager:
    def __init__(self, jwt: JWTManager):

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