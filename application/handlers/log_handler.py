from usecases import LogUseCase
from models import LogModel

class LogHandler(LogUseCase):
    def __init__(self, factory):
        self._logs_repository = factory.get_log_repository()

    def low_priority_log(self, id: int, msg: str) -> None:
        create_at = self._logs_repository.insert_timestamp()
        log = LogModel(user=id, action=msg, threat_lvl=LogModel.ThreatLevel.LOW, create_at=create_at)
        self._logs_repository.save_log(log_data=log)

    def medium_priority_log(self, id: int, msg: str) -> None:
        create_at = self._logs_repository.insert_timestamp()
        log = LogModel(user=id, action=msg, threat_lvl=LogModel.ThreatLevel.MEDIUM, create_at=create_at)
        self._logs_repository.save_log(log_data=log)

    def high_priority_log(self, id: int, msg: str) -> None:
        create_at = self._logs_repository.insert_timestamp()
        log = LogModel(user=id, action=msg, threat_lvl=LogModel.ThreatLevel.HIGH, create_at=create_at)
        self._logs_repository.save_log(log_data=log)


