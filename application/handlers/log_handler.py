from usecases import LogUseCase
from models import LogModel

class LogHandler(LogUseCase):
    def __init__(self, factory):
        self._logs_repository = factory.get_log_repository()
        self._high_priority = LogModel.ThreatLevel.HIGH
        self._medium_priority = LogModel.ThreatLevel.MEDIUM
        self._low_priority = LogModel.ThreatLevel.LOW

    def low_priority_log(self, _id: int, msg: str) -> None:
        create_at = self._logs_repository.insert_timestamp()
        log = LogModel(user=_id, action=msg, threat_lvl=self._low_priority, create_at=create_at)
        self._logs_repository.save_log(log_data=log)

    def medium_priority_log(self, _id: int, msg: str) -> None:
        create_at = self._logs_repository.insert_timestamp()
        log = LogModel(user=_id, action=msg, threat_lvl=self._medium_priority, create_at=create_at)
        self._logs_repository.save_log(log_data=log)

    def high_priority_log(self, _id: int, msg: str) -> None:
        create_at = self._logs_repository.insert_timestamp()
        log = LogModel(user=_id, action=msg, threat_lvl=self._low_priority, create_at=create_at)
        self._logs_repository.save_log(log_data=log)


