
from typing import Dict, Tuple, List

from usecases import MessageUseCase
from application.services import MessageHandlerService
from models import MessageModel

from libs.inputs_validation import valid_msg_inputs


class MessageHandler(MessageUseCase, MessageHandlerService):
    def __init__(self, factory, log_handler):
        self._message_repository = factory.get_message_repository()
        self._user_repository = factory.get_user_repository()
        self._log_handler = log_handler

    def send_message(self, user_id: int, message_data: Dict) -> Tuple:

        if not self._validate_send_message_inputs(message_data=message_data):
            return {'message': gettext("input_error")}, 400

        user_receive = self._user_repository.find_by_username(name=message_data.get('send_to'))
        if not user_receive:
            return {'message': gettext("user_not_found")}, 401

        self._send_message(user_send=user_id, user_receive=user_receive, message_data=message_data)
        return {'message': "message sent."}, 200

    def read_message(self, user_id: int, message_id: int) -> Tuple:
        message = self._message_repository.find_msg_by_id(idx=message_id)
        user_send = self._user_repository.find_by_id(msg.from_user)
        user_receive = self._user_repository.find_by_id(msg.to_user)

        is_valid_message = self._is_valid_message(message=message, user_send=user_send, user_receive=user_receive)
        if not is_valid_message:
            return {"message": gettext("invalid_credentials")}, 401

        if user_id == sender.idx:
            self._log_handler.high_priority_log(_id=user_id, msg=f"Read Msg to User: [{receiver.idx}]")
            return msg.json_read_msg(sender.name, receiver.name, False), 200

        if user_id == receiver.idx:
            self._log_handler.high_priority_log(_id=user_id, msg=f"Read Msg from User: [{sender.idx}], Mark as READ")
            return msg.json_read_msg(sender.name, receiver.name, True), 200

    def get_all_unread_messages(self, user_id: int) -> Tuple:
        all_messages = self._message_repository.find_all_unread(idx=user_id)
        self._log_handler.low_priority_log(_id=user_id, msg="Display all Unread messages titles")
        all_messages_list = self._convert_messages_to_list(messages=all_messages)
        return all_messages_list, 204

    def get_all_read_messages(self, user_id: int) -> Tuple:
        all_messages = self._message_repository.find_all_read(idx=user_id)
        self._log_handler.low_priority_log(_id=user_id, msg="Display all Read messages titles")
        all_messages_list = self._convert_messages_to_list(messages=all_messages)
        return all_messages_list, 204

    def get_all_received_messages(self, user_id: int) -> Tuple:
        all_messages = self._message_repository.find_all_received(idx=user_id)
        self._log_handler.low_priority_log(_id=user_id, msg="Display all Received messages titles")
        all_messages_list = self._convert_messages_to_list(messages=all_messages)
        return all_messages_list, 204

    def get_all_sent_messages(self, user_id: int) -> Tuple:
        all_messages = self._message_repository.find_all_sent(idx=user_id)
        self._log_handler.low_priority_log(_id=user_id, msg="Display all Sent messages titles")
        all_messages_list = self._convert_messages_to_list(messages=all_messages)
        return all_messages_list, 204

    def get_all_read_by_receiver_messages(self, user_id: int) -> Tuple:
        all_messages = self._message_repository.find_sent_n_read(idx=user_id)
        self._log_handler.low_priority_log(_id=user_id, msg="Display all Sent messages titles")
        all_messages_list = self._convert_messages_to_list(messages=all_messages)
        return all_messages_list, 204

    def _convert_messages_to_list(self, messages: List) -> List:
        return [self._convert_message_to_dict(message=message) for message in messages]

    def _convert_message_to_dict(self, message: "MessageSchema") -> Dict:
        """Json display pick msg menu for user"""

        is_message_checksum_valid = self._compare_hush_keys(message=message)
        if not is_message_checksum_valid:
            self._log_handler.high_priority_log(_id=message.from_user, msg=f'Message {message.idx} Been TAMPERED')
            return {message.idx: 'Message Been TAMPERED'}
        message = self._aggregate_message_to_dict(message=message)
        self._log_handler.low_priority_log(_id=message.idx, msg=f"{message.idx} MESSAGE CHECKSUM: TRUE")
        return  message

    def _aggregate_message_to_dict(self, message) -> Dict:
        read_status = "Read" if message.read_status else "Unread"
        read_at = self._message_repository.convert_timestamp(message.read_at) if message.read_at else "Unread"
        create_date = self._message_repository.convert_timestamp(message.create_date)

        message_to_dict = {self.idx: [{"from_user": message.from_user, "to_user": message.to_user,
                                       "msg_status": read_status, "msg_title": message.msg_title,
                                       "create_date": create_date, "read_at": read_at}]}
        return message_to_dict

    def _compare_hush_keys(self, message) -> bool:
        hash_key = self._message_repository.generate_message_hush_key(user_send=message.from_user,
                                                                      user_receive=message.to_user,
                                                                      message_title=message.msg_title,
                                                                      message_body=message.msg_body,
                                                                      created_date=message.create_at)
        return safe_str_cmp(hash_key, message.hash)

    def _is_valid_message(self, message, user_send, user_receive) -> bool:
        if message and user_send and user_receive:
            return True
        return False

    def _validate_send_message_inputs(self, message_data: Dict) -> bool:
        is_valid_title = valid_msg_inputs(message_data.get('title'))
        is_valid_body = valid_msg_inputs(message_data.get('body'))
        return is_valid_body and is_valid_title

    def _send_message(self, user_send: int, user_receive: "UserSchema", message_data: Dict) -> None:
        message = self._aggregate_message(user_send=user_send, user_receive=user_receive, message_data=message_data)
        message_dict_model = MessageModel(**message)
        self._message_repository.save_message(message=message_dict_model)
        self._log_handler.low_priority_log(_id=user_send, msg=f"Msg Sent to User: [{user_receive.idx}]")

    def _aggregate_message(self, user_send: int, user_receive: "UserSchema", message_data: Dict) -> Dict:
        message_schema = {"from_user": user_send,
                          "to_user": user_receive.idx,
                          "msg_title": message_data.get('title'),
                          "msg_body": message_data.get('body'),
                          "create_date": self._message_repository.insert_timestamp(),
                          "hash": None}
        message_schema['hash'] = self._generate_message_hash_key(message=message_schema)
        return message_schema

    def _generate_message_hash_key(self, message: Dict) -> str:
        hash_key = self._message_repository.generate_message_hush_key(user_send=message.get('from_user'),
                                                                      user_receive=message.get('from_user'),
                                                                      message_title=message.get('msg_title'),
                                                                      message_body=message.get('msg_body'),
                                                                      created_date=message.get('create_date'))
        return hash_key
