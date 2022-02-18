from abc import ABC, abstractmethod
from typing import Dict, Tuple

class MessageUseCase(ABC):

    @abstractmethod
    def send_message(self, user_id: int, message_data: Dict) -> Tuple:
        ...

    @abstractmethod
    def read_message(self, user_id: int, message_id: int) -> Tuple:
        ...

    @abstractmethod
    def get_all_unread_messages(self, user_id: int) -> Tuple:
        ...

    @abstractmethod
    def get_all_read_messages(self, user_id: int) -> Tuple:
        ...

    @abstractmethod
    def get_all_received_messages(self, user_id: int) -> Tuple:
        ...

    @abstractmethod
    def get_all_sent_messages(self, user_id: int) -> Tuple:
        ...

    @abstractmethod
    def get_all_read_by_receiver_messages(self, user_id: int) -> Tuple:
        ...