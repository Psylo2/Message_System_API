from typing import Dict, List

from manager.services import RepositoryService
from infrastracture.repository.repository import repository
from infrastracture.repository.user_repository import UserRepository
from infrastracture.repository.services import UserRepositoryService


class UserRepositoryQueries(UserRepositoryService):
    def __init__(self, repository_services: RepositoryService):
        self._repository_services = repository_services

    def save_user(self, user_data: Dict) -> UserRepository:
        user = UserRepository(**user_data)
        user.add_to_repository()
        return user

    def delete_user(self, user: UserRepository) -> None:
        user.active = False
        user.add_to_repository()

    def find_by_id(self, id: int) -> UserRepository:
        return UserRepository.query.filter_by(id=id).first()

    def find_by_username(self, name: str) -> UserRepository:
        return UserRepository.query.filter_by(name=name).first()

    def find_by_email(self, email: str) -> UserRepository:
        for user in self._get_all_users():
            if self._repository_services.decrypt(email, user.email):
                return user

    def find_all_not_u(self, id: int) -> UserRepository:
        return UserRepository.query.filter_by(UserRepository.id != id
                                              ).order_by(repository.desc(UserRepository.id)).all()

    def _update_password(self, user: UserRepository) -> None:
        user.password = self._repository_services.encrypt(user.password)
        user.query.filter_by(id=UserRepository.id).update(dict(password=user.password))
        user.update_repository()

    def _get_all_users(self) -> List[UserRepository]:
        return UserRepository.query.all()

    def encrypt_fields(self, user_data: Dict) -> None:
        user_data['email'] = self._repository_services.encrypt(user_data.get('email'))
        user_data['password'] = self._repository_services.encrypt(user_data.get('password'))

    def insert_timestamp(self) -> float:
        return self._repository_services.insert_timestamp()

    def convert_timestamp(self, timestamp: float) -> str:
        return self._repository_services.convert_timestamp(timestamp=timestamp)

    def decrypt(self, x: str, y: bytes) -> bool:
        return self._repository_services.decrypt(x=x, y=y)
