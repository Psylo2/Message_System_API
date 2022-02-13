from typing import Dict, List


from repository.repository import repository
from repository.user_repository import UserRepository
from repository.services import UserRepositoryService
from manager import RepositoryManager

class UserRepositoryController(RepositoryManager, UserRepositoryService):
    def __init__(self):
        super().__init__()

    def save_user(self, user_data: Dict) -> UserRepository:
        self._encrypt_fields(user_data=user_data)

        user = UserRepository(**user_data)
        user.add_to_repository()
        return user

    def delete_user(self, user: UserRepository) -> None:
        user.remove_from_repository()

    def find_by_id(self, id: int) -> UserRepository:
        return UserRepository.query.filter_by(id=id, active=True).first()

    def find_by_username(self, name: str) -> UserRepository:
        return UserRepository.query.filter_by(name=name, active=True).first()

    def find_by_email(self, email: str) -> UserRepository:
        x = UserRepository.query.with_entities(email, UserRepository.id, UserRepository.active == True).all()
        for em in x:
            if self.decrypt(email, em[0]):
                return self.find_by_id(em[1])

    def find_all_not_u(self, id: int) -> UserRepository:
        return UserRepository.query.filter_by(UserRepository.id != id
                                              ).order_by(repository.desc(UserRepository.id)).all()

    def _update_password(self, user: UserRepository) -> None:
        user.password = self.encrypt(user.password)
        user.query.filter_by(id=UserRepository.id).update(dict(password=user.password))
        user.update_repository()

    def _get_all_users(self) -> List[UserRepository]:
        return UserRepository.query.all()

    def _encrypt_fields(self, user_data: Dict) -> None:
        user_data['email'] = self.encrypt(user_data.get('email'))
        user_data['password'] = self.encrypt(user_data.get('password'))

    def insert_timestamp(self) -> float:
        return self.insert_timestamp()

    def convert_timestamp(self, timestamp: float) -> str:
        return self.convert_timestamp(timestamp=timestamp)

    def decrypt(self, x: str, y: bytes) -> bool:
        return self.decrypt(x=x, y=y)
