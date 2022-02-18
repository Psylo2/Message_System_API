from typing import Dict, List

from manager import RepositoryManager
from infrastracture.repository.repository import repository
from infrastracture.repository.user_repository import UserRepository
from infrastracture.repository.services import UserRepositoryService


class UserRepositoryController(RepositoryManager, UserRepositoryService):
    def __init__(self):
        super().__init__()

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
            if self.decrypt(email, user.email):
                return user

    def find_all_not_u(self, id: int) -> UserRepository:
        return UserRepository.query.filter_by(UserRepository.id != id
                                              ).order_by(repository.desc(UserRepository.id)).all()

    def _update_password(self, user: UserRepository) -> None:
        user.password = self.encrypt(user.password)
        user.query.filter_by(id=UserRepository.id).update(dict(password=user.password))
        user.update_repository()

    def _get_all_users(self) -> List[UserRepository]:
        return UserRepository.query.all()

    def encrypt_fields(self, user_data: Dict) -> None:
        user_data['email'] = super().encrypt(user_data.get('email'))
        user_data['password'] = super().encrypt(user_data.get('password'))

    def insert_timestamp(self) -> float:
        return super().insert_timestamp()

    def convert_timestamp(self, timestamp: float) -> str:
        return super().convert_timestamp(timestamp=timestamp)

    def decrypt(self, x: str, y: bytes) -> bool:
        return super().decrypt(x=x, y=y)
