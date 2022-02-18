from typing import Dict, Union

from infrastracture.repository.repository import repository
from infrastracture.repository.services import RepositoryService


class UserRepository(repository.Model, RepositoryService):
    __tablename__ = 'users'
    id = repository.Column(repository.Integer, primary_key=True, autoincrement=True)
    name = repository.Column(repository.String(), unique=True, nullable=False)
    email = repository.Column(repository.LargeBinary, nullable=False)
    password = repository.Column(repository.LargeBinary, nullable=False)
    create_at = repository.Column(repository.Float, nullable=True)
    last_login = repository.Column(repository.Float, nullable=True)

    def __init__(self, id: Union[int, None],  name: str, email: str,
                 password: str, create_at: float = None, last_login: float = None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.create_at = create_at
        self.last_login = last_login

    def add_to_repository(self) -> None:
        repository.session.add(self)
        self.update_repository()

    def remove_from_repository(self) -> None:
        repository.session.delete(self)
        self.update_repository()

    def update_repository(self) -> None:
        repository.session.commit()

    def dict(self) -> Dict:
        return {"id": self.id,
                "name": self.name,
                "email": self.email,
                "password": self.password,
                "create_at": self.create_at,
                "last_login": self.last_login}
