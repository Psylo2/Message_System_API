""""This file is made in order to:
    [*] Not importing DB
    [*] Not recreate DB
    [*] Save Admin identity
when we running the App"""
import os

from db.data_base import db
from app import app
from models.user import UserModel

db.init_app(app)


@app.before_first_request
def create_tables():
    """Create tables and save Admin identity"""
    db.create_all()
    admin = UserModel(os.environ.get('ADMIN_NAME'),
                      os.environ.get('ADMIN_EMAIL'),
                      os.environ.get('ADMIN_PASSWORD'))
    admin.save_to_db()


