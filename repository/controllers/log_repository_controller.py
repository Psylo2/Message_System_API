from typing import Dict, List

from manager import RepositoryManager
from repository.repository import repository
from repository.log_repository import LogRepository
from repository.services import LogRepositoryService


class LogRepositoryController(RepositoryManager, LogRepositoryService):
    def __init__(self):
        super().__init__()

    def save_log(self, log_data: Dict) -> LogRepository:
        """Save Log to DB"""
        log = LogRepository(**log_data)
        log.add_to_repository()
        return log

    def find_by_log_id(self, id: int) -> LogRepository:
        """Find All Logs of a User, order by newest"""
        return LogRepository.query.filter_by(id=id).first()

    def find_all_logs(self) -> List[LogRepository]:
        """Find all Log by id, order by newest"""
        return LogRepository.query.all()

    def find_by_level(self, threat_lvl: str) -> LogRepository:
        """Find all Log by Threat Level, order by newest"""
        return LogRepository.query.filter_by(threat_lvl=threat_lvl).order_by(repository.desc(LogRepository.id)).all()

    def find_user_logs(self, id: int) -> LogRepository:
        """return all user's logs order by newest message"""
        return LogRepository.query.filter_by(user_id=id).order_by(repository.desc(LogRepository.id)).all()

    def insert_timestamp(self) -> float:
        return self.insert_timestamp()

    def convert_timestamp(self, timestamp: float) -> str:
        return self.convert_timestamp(timestamp=timestamp)
