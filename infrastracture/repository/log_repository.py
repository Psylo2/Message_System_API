from typing import Dict, Union

from infrastracture.repository.repository import repository
from infrastracture.repository.services import RepositoryService

class LogRepository(repository.Model, RepositoryService):
    __tablename__ = 'logs'
    id = repository.Column(repository.Integer, primary_key=True, autoincrement=True)
    user_id = repository.Column(repository.Integer, repository.ForeignKey('users.id'), nullable=True)
    user = repository.relationship('UserRepository', foreign_keys=user_id)
    action = repository.Column(repository.String(65535), nullable=False)
    create_at = repository.Column(repository.Float, nullable=False)
    threat_lvl = repository.Column(repository.String(1), nullable=False)

    def __init__(self,  id: Union[int, None], user_id: int, action: str,  create_at: float, threat_lvl: str):
        self.id = id
        self.user_id = user_id
        self.action = action
        self.create_at = create_at
        self.threat_lvl = threat_lvl

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
                "user_id": self.user_id,
                "action": self.action,
                "create_at": self.create_at,
                "threat_lvl": self.threat_lvl}
