import os

from app import app, repository, factory


repository.init_app(app=app)

def __admin_privileges():
    user_repository = factory.get_user_repository()
    """Grant admin privileges on create app"""
    admin = user_repository.find_by_username(name=os.environ.get('ADMIN_NAME'))
    if not admin:
        admin = {"name": os.environ.get('ADMIN_NAME'),
                 "email": os.environ.get('ADMIN_EMAIL'),
                 "password": os.environ.get('ADMIN_PASSWORD')}
        user_repository.save_user(user_data=admin)


@app.before_first_request
def create_tables():
    """Create tables and save Admin identity"""
    repository.create_all()
    __admin_privileges()
