import os
from datetime import timedelta

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.environ.get('ACCESS_DELTA')))
JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=int(os.environ.get('REFRESH_DELTA')))
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
