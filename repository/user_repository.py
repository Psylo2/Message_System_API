from typing import Dict, List

from app import repository
from repository.services import UserRepositoryService


class UserSchema(repository.db.Model):
    __tablename__ = 'users'
    idx = repository.db.Column(repository.db.Integer, primary_key=True, autoincrement=True)
    name = repository.db.Column(repository.db.String(), unique=True, nullable=False)
    email = repository.db.Column(repository.db.LargeBinary, nullable=False)
    password = repository.db.Column(repository.db.LargeBinary, nullable=False)
    create_at = repository.db.Column(repository.db.Float, nullable=True)
    last_login = repository.db.Column(repository.db.Float, nullable=True)
    active = repository.db.Column(repository.db.Boolean, default=False, nullable=False)

    def __init__(self, name: str, email: str,
                 password: str, active: bool,
                 create_at: float = None, last_login: float = None):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.create_at = create_at
        self.last_login = last_login


class UserRepository(UserRepositoryService):
    def __init__(self):
        pass

    def save_user(self, user_data: Dict) -> UserSchema:
        self._encrypt_fields(user_data=user_data)

        user = UserSchema(**user_data)
        repository.db.session.add(user)
        repository.db.session.commit()
        return user

    def delete_user(self, user) -> None:
        repository.db.session.delete(user)
        repository.db.session.commit()

    def find_by_id(self, idx: int) -> UserSchema:
        return UserSchema.query.filter_by(idx=idx, active=True).first()

    def find_by_username(self, name: str) -> UserSchema:
        return UserSchema.query.filter_by(name=name, active=True).first()

    def find_by_email(self, email: str) -> UserSchema:
        x = UserSchema.query.with_entities(email, UserSchema.idx, UserSchema.active == True).all()
        for em in x:
            if repository.decrypt(super(), email, em[0]):
                return self.find_by_id(em[1])

    def find_all_not_u(self, idx: int) -> UserSchema:
        return UserSchema.query.filter_by(UserSchema.idx != idx).order_by(repository.db.desc(UserSchema.idx)).all()

    def _update_password(self, new: str) -> None:
        encrypted_new_password = repository.encrypt(new)
        UserSchema.query.filter_by(idx=UserSchema.idx).update(dict(password=encrypted_new_password))
        repository.db.session.commit()

    def _get_all_users(self) -> List[UserSchema]:
        return UserSchema.query.all()

    def _encrypt_fields(self, user_data: Dict) -> None:
        user_data['email'] = repository.encrypt(user_data.get('email'))
        user_data['password'] = repository.encrypt(user_data.get('password'))

    def insert_timestamp(self) -> float:
        return repository.insert_timestamp()

    def convert_timestamp(self, timestamp: float) -> str:
        return repository.convert_timestamp(timestamp=timestamp)
