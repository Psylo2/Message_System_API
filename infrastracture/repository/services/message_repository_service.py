from abc import ABC, abstractmethod
from typing import List, Dict


class MessageRepositoryService(ABC):

    @abstractmethod
    def save_message(self, message_data: Dict) -> None:
        ...

    @abstractmethod
    def insert_timestamp(self) -> float:
        ...

    @abstractmethod
    def convert_timestamp(self, timestamp: float) -> str:
        ...

    @abstractmethod
    def find_msg_by_id(self, id: int) -> "MessageSchema":
        ...

    @abstractmethod
    def find_all_received(self, id: int) -> List["MessageSchema"]:
        ...

    @abstractmethod
    def find_all_sent(self, id: int) -> List["MessageSchema"]:
        """return all delivered msg of a user, order by newest message"""
        ...

    @abstractmethod
    def find_all_unread(self, id: int) -> List["MessageSchema"]:
        """return all unread messages of a user, order by newest message"""
        ...

    @abstractmethod
    def find_all_read(self, id: int) -> List["MessageSchema"]:
        """return all read messages of a user, order by newest message"""
        ...

    @abstractmethod
    def find_sent_n_read(self, id: int) -> List["MessageSchema"]:
        """return all delivered messages of a user that have been marked READ """
        ...

    @abstractmethod
    def _update_read_status(self, id: int) -> None:
        """UPDATE a msg to READ status """
        ...

    @abstractmethod
    def generate_message_hash_key(self, user_send: int, user_receive: int, message_title: str, message_body: str,
                                  created_date: float) -> str:
        ...
