from db.data_base import db, convert_timestamp, insert_timestamp


class MessageModel(db.Model):
    __tablename__ = 'messages'
    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_user = db.Column(db.Integer, db.ForeignKey('users.idx'), nullable=False)
    to_user = db.Column(db.Integer, db.ForeignKey('users.idx'), nullable=False)
    user_fr = db.relationship('UserModel', foreign_keys=from_user)
    user_to = db.relationship('UserModel', foreign_keys=to_user)
    msg_title = db.Column(db.String(600), nullable=False)
    msg_body = db.Column(db.String(65535), nullable=False)
    read_status = db.Column(db.Boolean, default=False, nullable=False)
    create_date = db.Column(db.Float, nullable=True)
    read_at = db.Column(db.Float, nullable=True)
    hash = db.Column(db.String(128), nullable=False)

    def __init__(self, sender: int, receiver: int, msg_title: str, msg_body: str):
        self.from_user = sender
        self.to_user = receiver
        self.msg_title = msg_title
        self.msg_body = msg_body
        self.create_date = insert_timestamp()
        self.hash = self.__gen_hash()

    def __gen_hash(self):
        import hashlib
        sha512 = hashlib.sha512()
        sha512.update((str(self.from_user) +
                       str(self.to_user) +
                       self.msg_title +
                       self.msg_body +
                       convert_timestamp(self.create_date)).encode('UTF-8'))
        return sha512.hexdigest()

    def json_read_msg(self, sender: str, receiver: str):
        """Json MSG TITLE + BODY"""
        self._update_read_status()
        st = "Read" if self.read_status is True else "Unread"
        return {"from_user": sender, "to_user": receiver,
                "msg_status": st, "msg_title": self.msg_title,
                "msg_body": self.msg_body, "create_date": convert_timestamp(self.create_date),
                "read_at": convert_timestamp(self.read_at)}

    def json_only_titles(self, sender: str, receiver: str):
        """Json display pick msg menu for user"""
        st = "Read" if self.read_status is True else "Unread"
        re = convert_timestamp(self.read_at) if self.read_at is not None else "Unread"
        return {self.idx: [{"from_user": sender, "to_user": receiver,
                            "msg_status": st, "msg_title": self.msg_title,
                            "create_date": convert_timestamp(self.create_date), "read_at": re}]
                }

    def save_to_db(self) -> None:
        """Save msg to DB"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Delete msg from DB"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_msg_by_id(cls, idx: int) -> "MessageModel":
        """return all received msg of a user, order by newest message"""
        return cls.query.filter_by(idx=idx).first()

    @classmethod
    def find_all_received(cls, idx: int) -> "MessageModel":
        """return all received msg of a user, order by newest message"""
        return cls.query.filter_by(to_user=idx).order_by(db.desc(MessageModel.idx)).all()

    @classmethod
    def find_all_sent(cls, idx: int) -> "MessageModel":
        """return all delivered msg of a user, order by newest message"""
        return cls.query.filter_by(from_user=idx).order_by(db.desc(MessageModel.idx)).all()

    @classmethod
    def find_all_unread(cls, idx: int) -> "MessageModel":
        """return all unread messages of a user, order by newest message"""
        return cls.query.filter_by(to_user=idx, read_status=False).order_by(db.desc(MessageModel.idx)).all()

    @classmethod
    def find_all_read(cls, idx: int) -> "MessageModel":
        """return all read messages of a user, order by newest message"""
        return cls.query.filter_by(to_user=idx, read_status=True).order_by(db.desc(MessageModel.idx)).all()

    @classmethod
    def find_sent_n_read(cls) -> "MessageModel":
        """return all delivered messages of a user that have been marked READ """
        return cls.query.filter_by(from_user=cls.idx, read_status=True).order_by(db.desc(MessageModel.idx)).all()

    def _update_read_status(self) -> "MessageModel":
        """UPDATE a msg to READ status """
        x = MessageModel.query.filter_by(idx=self.idx).update(dict(read_status=True))
        self.read_at = insert_timestamp()
        db.session.commit()
