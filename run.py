import os

from app import app, repository
from repository.user_repository import UserRepository
from models.user import UserModel

repository.db.init_app(app)

def __admin_privileges():
    """Grant admin privileges on create app"""
    admin = UserRepository().find_by_username(name=os.environ.get('ADMIN_NAME'))
    if not admin:
        admin = UserModel(name=os.environ.get('ADMIN_NAME'),
                          email=os.environ.get('ADMIN_EMAIL'),
                          password=os.environ.get('ADMIN_PASSWORD'))
        admin.create_at = repository.insert_timestamp()
        UserRepository().save_to_db(user_data=admin.dict())

@app.before_first_request
def create_tables():
    """Create tables and save Admin identity"""
    repository.db.create_all()
    __admin_privileges()
