from typing import Dict, List

from app import repository
from repository.services import LogRepositoryService

class LogSchema(repository.db.Model):
    __tablename__ = 'logs'
    idx = repository.db.Column(repository.db.Integer, primary_key=True, autoincrement=True)
    user_id = repository.db.Column(repository.db.Integer, repository.db.ForeignKey('users.idx'), nullable=True)
    user = repository.db.relationship('UserModel', foreign_keys=user_id)
    action = repository.db.Column(repository.db.String(65535), nullable=False)
    create_at = repository.db.Column(repository.db.Float, nullable=False)
    threat_lvl = repository.db.Column(repository.db.String(1), nullable=False)

    def __init__(self, user_id: int, action: str,  create_at: float, threat_lvl: str):
        self.user_id = user_id
        self.action = action
        self.create_at = create_at
        self.threat_lvl = threat_lvl


class LogRepository(LogRepositoryService):
    def __init__(self):
        pass

    def save_log(self, log_data: Dict) -> LogSchema:
        """Save Log to DB"""
        log = LogSchema(**log_data)
        repository.db.session.add(log)
        repository.db.session.commit()
        return log

    def find_by_log_id(self, idx: int) -> LogSchema:
        """Find All Logs of a User, order by newest"""
        return LogSchema.query.filter_by(idx=idx).first()

    def find_all_logs(self) -> List[LogSchema]:
        """Find all Log by id, order by newest"""
        return LogSchema.query.all()

    def find_by_level(self, threat_lvl: str) -> LogSchema:
        """Find all Log by Threat Level, order by newest"""
        return LogSchema.query.filter_by(threat_lvl=threat_lvl).order_by(repository.db.desc(LogSchema.idx)).all()

    def find_user_logs(self, idx: int) -> LogSchema:
        """return all user's logs order by newest message"""
        return LogSchema.query.filter_by(user_id=idx).order_by(repository.db.desc(LogSchema.idx)).all()

    def insert_timestamp(self) -> float:
        return repository.insert_timestamp()

    def convert_timestamp(self, timestamp: float) -> str:
        return repository.convert_timestamp(timestamp=timestamp)
