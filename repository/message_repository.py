import hashlib
from typing import Dict, List

from app import repository
from repository.services import MessageRepositoryService

class MessageSchema(repository.db.Model):
    __tablename__ = 'messages'
    idx = repository.db.Column(repository.db.Integer, primary_key=True, autoincrement=True)
    from_user = repository.db.Column(repository.db.Integer, repository.db.ForeignKey('users.idx'), nullable=False)
    to_user = repository.db.Column(repository.db.Integer, repository.db.ForeignKey('users.idx'), nullable=False)
    user_fr = repository.db.relationship('UserModel', foreign_keys=from_user)
    user_to = repository.db.relationship('UserModel', foreign_keys=to_user)
    msg_title = repository.db.Column(repository.db.String(600), nullable=False)
    msg_body = repository.db.Column(repository.db.String(65535), nullable=False)
    read_status = repository.db.Column(repository.db.Boolean, default=False, nullable=False)
    create_date = repository.db.Column(repository.db.Float, nullable=True)
    read_at = repository.db.Column(repository.db.Float, nullable=True)
    hash = repository.db.Column(repository.db.String(128), nullable=False)

    def __init__(self, sender: int, receiver: int, msg_title: str, msg_body: str, hash: str, create_date: float = None,
                 create_at: float = None):

        self.from_user = sender
        self.to_user = receiver
        self.msg_title = msg_title
        self.msg_body = msg_body
        self.create_date = create_date
        self.create_at = create_at
        self.hash = hash


class MessageRepository(MessageRepositoryService):
    def __init__(self):
        pass

    def save_message(self, message_data: Dict) -> None:
        message = MessageSchema(**message_data)
        message.create_at = repository.convert_timestamp(timestamp=created_date)
        repository.db.session.add(message)
        repository.db.session.commit()

    def insert_timestamp(self) -> float:
        return repository.insert_timestamp()

    def convert_timestamp(self, timestamp: float) -> str:
        return repository.convert_timestamp(timestamp=timestamp)

    def generate_message_hush_key(self, user_send: int, user_receive: int, message_title: str, message_body: str,
                                  created_date: float) -> str:
        created_date = repository.convert_timestamp(timestamp=created_date)
        aggregate_context = f"{str(user_send)}{str(user_receive)}{message_title}{message_body}{created_date}"
        sha512 = hashlib.sha512()
        sha512.update(aggregate_context.encode('UTF-8'))
        return sha512.hexdigest()

    def find_msg_by_id(self, idx: int) -> "MessageSchema":
        return MessageSchema.query.filter_by(idx=idx).first()

    def find_all_received(self, idx: int) -> List["MessageSchema"]:
        return MessageSchema.query.filter_by(to_user=idx
                                             ).order_by(repository.db.desc(MessageSchema.idx)).all()

    def find_all_sent(self, idx: int) -> List["MessageSchema"]:
        return MessageSchema.query.filter_by(from_user=idx
                                             ).order_by(repository.db.desc(MessageSchema.idx)).all()

    def find_all_unread(self, idx: int) -> List["MessageSchema"]:
        return MessageSchema.query.filter_by(to_user=idx,
                                             read_status=False).order_by(repository.db.desc(MessageSchema.idx)).all()

    def find_all_read(self, idx: int) -> List["MessageSchema"]:
        return MessageSchema.query.filter_by(to_user=idx,
                                             read_status=True).order_by(repository.db.desc(MessageSchema.idx)).all()

    def find_sent_n_read(self, idx: int) -> List["MessageSchema"]:
        return MessageSchema.query.filter_by(from_user=idx,
                                             read_status=True).order_by(repository.db.desc(MessageSchema.idx)).all()

    def _update_read_status(self, idx: int) -> None:
        x = MessageSchema.query.filter_by(idx=idx).update(dict(read_status=True))
        MessageSchema.read_at = repository.insert_timestamp()
        repository.db.session.commit()

