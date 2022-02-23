import functools
from typing import Callable
from flask import current_app
from flask_jwt_extended import get_jwt_identity

from infrastracture.repository.queries import UserRepositoryQueries
from application.core import RepositoryManager

__repository_manager_service = RepositoryManager()
__user_repository = UserRepositoryQueries(repository_services=__repository_manager_service)

def requires_admin(fun: Callable) -> Callable:
    @functools.wraps(fun)
    def decorated_function(*args, **kwargs):
        user = __user_repository.find_by_id(id=get_jwt_identity())
        if user.name != current_app.config.get('ADMIN_NAME'):
            return {'message': "Admin privilege required."}, 400
        return fun(*args, **kwargs)
    return decorated_function
