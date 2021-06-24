import os
import bcrypt
from typing import Union, Any

from db.database import db, convert_timestamp


class UserModel(db.Model):
    __tablename__ = 'users'
    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.LargeBinary, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    create_at = db.Column(db.Float, nullable=True)
    last_login = db.Column(db.Float, nullable=True)
    active = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, name: str, email: str, password):
        self.name = name
        self.email = self.__encrypt(email)
        self.password = self.__encrypt(password)

    def json(self) -> dict[int, list[dict[str, Union[str, Any]]]]:
        return {self.idx: [{
            "name": self.name, "create_at": convert_timestamp(self.create_at)}]
        }

    def save_to_db(self) -> None:
        """Save user to DB"""
        self.active = True
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Delete user from DB"""
        self.active = False
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, idx: int) -> "UserModel":
        """Find user by idx"""
        return cls.query.filter_by(idx=idx, active=True).first()

    @classmethod
    def find_by_username(cls, name: str) -> "UserModel":
        """Find user by name"""
        return cls.query.filter_by(name=name, active=True).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        """Find user by email, Because email encrypted, decrypt"""
        x = cls.query.with_entities(UserModel.email, UserModel.idx, UserModel.active == True).all()
        for em in x:
            if cls.decrypt(UserModel, email, em[0]):
                return cls.find_by_id(em[1])

    @classmethod
    def find_all_not_u(cls, idx: int) -> "UserModel":
        """Display available Users for send MSG"""
        return cls.query.filter_by(UserModel.idx != idx).order_by(db.desc(UserModel.idx)).all()

    def _update_password(self, new: str) -> None:
        """UPDATE a msg to READ status """
        x = UserModel.query.filter_by(idx=self.idx).update(dict(password=self.__encrypt(new)))
        db.session.commit()

    def __encrypt(self, string: str) -> bytes:
        """Encrypt given string"""
        key = int(os.environ.get('SALT_KEY'))
        return bcrypt.hashpw(string.encode("UTF-8"), bcrypt.gensalt(key))

    def decrypt(self, x: bytes, y: bytes) -> bool:
        """Match 2 hash to Verify string context """
        return bcrypt.checkpw(x.encode("UTF-8"), y)
