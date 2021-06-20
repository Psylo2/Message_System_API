""""This file is made in order to:
    [*] Not importing DB
    [*] Not recreate DB
    [*] Save Admin identity
when we running the App"""
import os

from db.database import db, insert_timestamp
from app import app
from models.user import UserModel

db.init_app(app)

def __admin_priv():
    """Grant admin privileges on create app"""
    admin = UserModel(name=os.environ.get('ADMIN_NAME'),
                      email=os.environ.get('ADMIN_EMAIL'),
                      password=os.environ.get('ADMIN_PASSWORD'))
    admin.create_at = insert_timestamp()
    admin.save_to_db()

@app.before_first_request
def create_tables():
    """Create tables and save Admin identity"""
    db.create_all()
    __admin_priv()
