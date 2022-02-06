from abc import ABC, abstractmethod
from typing import Dict, List


class MessageHandlerService(ABC):

    @abstractmethod
    def _validate_send_message_inputs(self, message_data: Dict) -> bool:
        ...

    @abstractmethod
    def _send_message(self, user_send: int, user_receive: "UserSchema", message_data: Dict) -> None:
        ...

    @abstractmethod
    def _generate_message_hash_key(self, message: Dict) -> str:
        ...

    @abstractmethod
    def _aggregate_message(self, user_send: int, user_receive: "UserSchema", message_data: Dict) -> Dict:
        ...

    @abstractmethod
    def _is_valid_message(self, message, user_send, user_receive) -> bool:
        ...

    @abstractmethod
    def _convert_messages_to_list(self, messages: List) -> List:
        ...

    @abstractmethod
    def _convert_message_to_dict(self, message: "MessageSchema") -> Dict:
        ...

    @abstractmethod
    def _aggregate_message_to_dict(self, message) -> Dict:
        ...

    @abstractmethod
    def _compare_hush_keys(self, message) -> bool:
        ...