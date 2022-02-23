from application.services import LogUseCaseService
from infrastracture.repository.services import LogRepositoryService


class LogUseCase(LogUseCaseService):
    def __init__(self, logs_repository_service: LogRepositoryService):
        self._logs_repository_service = logs_repository_service

    def low_priority_log(self, id: int, msg: str) -> None:
        create_at = self._logs_repository.insert_timestamp()
        log = LogModel(user_id=id, action=msg, threat_lvl=LogModel.ThreatLevel.LOW.value, create_at=create_at)
        self._logs_repository.save_log(log_data=log.dict())

    def medium_priority_log(self, id: int, msg: str) -> None:
        create_at = self._logs_repository.insert_timestamp()
        log = LogModel(user_id=id, action=msg, threat_lvl=LogModel.ThreatLevel.MEDIUM.value, create_at=create_at)
        self._logs_repository.save_log(log_data=log.dict())

    def high_priority_log(self, id: int, msg: str) -> None:
        create_at = self._logs_repository.insert_timestamp()
        log = LogModel(user_id=id, action=msg, threat_lvl=LogModel.ThreatLevel.HIGH.value, create_at=create_at)
        self._logs_repository.save_log(log_data=log.dict())
