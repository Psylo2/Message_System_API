from typing import Dict, List

from application.core.services import RepositoryService
from infrastracture.repository.repository import repository
from infrastracture.repository.log_repository import LogRepository
from infrastracture.repository.services import LogRepositoryService


class LogRepositoryQueries(LogRepositoryService):
    def __init__(self, repository_services: RepositoryService):
        self.repository_services = repository_services

    def save_log(self, log_data: Dict) -> LogRepository:
        log = LogRepository(**log_data)
        log.add_to_repository()
        return log

    def find_by_log_id(self, id: int) -> LogRepository:
        return LogRepository.query.filter_by(id=id).first()

    def find_all_logs(self) -> List[LogRepository]:
        return LogRepository.query.all()

    def find_by_level(self, threat_lvl: str) -> LogRepository:
        return LogRepository.query.filter_by(threat_lvl=threat_lvl).order_by(repository.desc(LogRepository.id)).all()

    def find_user_logs(self, id: int) -> LogRepository:
        return LogRepository.query.filter_by(user_id=id).order_by(repository.desc(LogRepository.id)).all()

    def insert_timestamp(self) -> float:
        return self.repository_services.insert_timestamp()

    def convert_timestamp(self, timestamp: float) -> str:
        return self.repository_services.convert_timestamp(timestamp=timestamp)
