from typing import Dict, Union

from infrastracture.repository.repository import repository
from infrastracture.repository.services import RepositoryService


class MessageRepository(repository.Model, RepositoryService):
    __tablename__ = 'messages'
    id = repository.Column(repository.Integer, primary_key=True, autoincrement=True)
    from_user = repository.Column(repository.Integer, repository.ForeignKey('users.id'), nullable=False)
    to_user = repository.Column(repository.Integer, repository.ForeignKey('users.id'), nullable=False)
    user_fr = repository.relationship('UserRepository', foreign_keys=from_user)
    user_to = repository.relationship('UserRepository', foreign_keys=to_user)
    msg_title = repository.Column(repository.String(600), nullable=False)
    msg_body = repository.Column(repository.String(65535), nullable=False)
    read_status = repository.Column(repository.Boolean, default=False, nullable=False)
    create_date = repository.Column(repository.Float, nullable=True)
    read_at = repository.Column(repository.Float, nullable=True)
    hash = repository.Column(repository.String(128), nullable=False)

    def __init__(self, id: Union[int, None], sender: int, receiver: int, msg_title: str,
                 msg_body: str, hash: str, create_date: float = None, create_at: float = None):
        self.id = id
        self.from_user = sender
        self.to_user = receiver
        self.msg_title = msg_title
        self.msg_body = msg_body
        self.create_date = create_date
        self.create_at = create_at
        self.hash = hash

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
                "from_user": self.from_user,
                "to_user": self.to_user,
                "msg_title": self.msg_title,
                "msg_body": self.msg_body,
                "create_date": self.create_date,
                "create_at": self.create_at,
                "hash": self.hash}
