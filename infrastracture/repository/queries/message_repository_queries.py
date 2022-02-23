import hashlib
from typing import Dict, List

from manager.services import RepositoryService
from infrastracture.repository.repository import repository
from infrastracture.repository.message_repository import MessageRepository
from infrastracture.repository.services import MessageRepositoryService

class MessageRepositoryQueries(MessageRepositoryService):
    def __init__(self, repository_services: RepositoryService):
        self._repository_services = repository_services

    def save_message(self, message_data: Dict) -> None:
        message = MessageRepository(**message_data)
        message.create_at = self._repository_services.convert_timestamp(timestamp=message.create_date)
        message.add_to_repository()

    def insert_timestamp(self) -> float:
        return self._repository_services.insert_timestamp()

    def convert_timestamp(self, timestamp: float) -> str:
        return self._repository_services.convert_timestamp(timestamp=timestamp)

    def generate_message_hash_key(self, user_send: int, user_receive: int, message_title: str, message_body: str,
                                  created_date: float) -> str:
        created_date = self._repository_services.convert_timestamp(timestamp=created_date)
        aggregate_context = f"{str(user_send)}{str(user_receive)}{message_title}{message_body}{created_date}"
        sha512 = hashlib.sha512()
        sha512.update(aggregate_context.encode('UTF-8'))
        return sha512.hexdigest()

    def find_msg_by_id(self, id: int) -> MessageRepository:
        return MessageRepository.query.filter_by(id=id).first()

    def find_all_received(self, id: int) -> List[MessageRepository]:
        return MessageRepository.query.filter_by(to_user=id
                                             ).order_by(repository.desc(MessageRepository.id)).all()

    def find_all_sent(self, id: int) -> List[MessageRepository]:
        return MessageRepository.query.filter_by(from_user=id
                                             ).order_by(repository.desc(MessageRepository.id)).all()

    def find_all_unread(self, id: int) -> List[MessageRepository]:
        return MessageRepository.query.filter_by(to_user=id,
                                             read_status=False).order_by(repository.desc(MessageRepository.id)).all()

    def find_all_read(self, id: int) -> List[MessageRepository]:
        return MessageRepository.query.filter_by(to_user=id,
                                             read_status=True).order_by(repository.desc(MessageRepository.id)).all()

    def find_sent_n_read(self, id: int) -> List[MessageRepository]:
        return MessageRepository.query.filter_by(from_user=id,
                                             read_status=True).order_by(repository.desc(MessageRepository.id)).all()

    def _update_read_status(self, id: int) -> None:
        message = MessageRepository.query.filter_by(id=id).update(dict(read_status=True))
        message.read_at = self._repository_services.insert_timestamp()
        message.update_in_repository()
