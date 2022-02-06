from typing import Optional
from pydantic import BaseModel, validator


class MessageModel(BaseModel):
    from_user: int
    to_user: int
    msg_title: str
    msg_body: str
    read_status: bool = False
    create_date: Optional[float]
    read_at: Optional[float]
    hash: str

    @validator('from_user', 'to_user')
    def validate_int(cls, int_) -> int:
        if not isinstance(int, int_):
            raise TypeError("Type must be int")
        return int_

    @validator('read_status')
    def validate_bool(cls, bool_) -> bool:
        if not isinstance(bool, bool_):
            raise TypeError("Type must be float")
        return bool_

    @validator('msg_title', 'msg_body', 'hash')
    def validate_str(cls, str_) -> str:
        if not isinstance(str, str_):
            raise TypeError("Type must be str")
        return str_









    def __gen_hash(self):
        import hashlib
        sha512 = hashlib.sha512()
        sha512.update((str(self.from_user) +
                       str(self.to_user) +
                       self.msg_title +
                       self.msg_body +
                       convert_timestamp(self.create_date)).encode('UTF-8'))
        return sha512.hexdigest()

    def json_read_msg(self, sender: str, receiver: str, update: bool):
        """Json MSG TITLE + BODY"""
        self._update_read_status() if update else None
        st = "Read" if self.read_status else "Unread"
        re = convert_timestamp(self.read_at) if self.read_at is not None else "Unread"

        if safe_str_cmp(self.__gen_hash(), self.hash):
            LogModel(self.idx,
                     f"[{self.idx}] MESSAGE CHECKSUM: TRUE",
                     'L').save_to_db()
            return {"from_user": sender, "to_user": receiver,
                    "msg_status": st, "msg_title": self.msg_title,
                    "msg_body": self.msg_body, "create_date": convert_timestamp(self.create_date),
                    "read_at": re}

        LogModel(self.idx,
                 f"[{self.idx}] MESSAGE -  BEEN TEMPERED",
                 'H').save_to_db()
        return {self.idx: 'Message Been TAMPERED'}


    def json_only_titles(self, sender: str, receiver: str):
        """Json display pick msg menu for user"""
        st = "Read" if self.read_status else "Unread"
        re = convert_timestamp(self.read_at) if self.read_at is not None else "Unread"

        if safe_str_cmp(self.__gen_hash(), self.hash):
            LogModel(self.idx,
                     f"[{self.idx}] MESSAGE CHECKSUM: TRUE",
                     'L').save_to_db()
            return {self.idx: [{"from_user": sender, "to_user": receiver,
                                "msg_status": st, "msg_title": self.msg_title,
                                "create_date": convert_timestamp(self.create_date), "read_at": re}]
                    }
        LogModel(self.idx,
                 f"[{self.idx}] MESSAGE -  BEEN TEMPERED",
                 'H').save_to_db()
        return {self.idx: 'Message Been TAMPERED'}

    def save_to_db(self) -> None:
        """Save msg to DB"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Delete msg from DB"""
        db.session.delete(self)
        db.session.commit()
