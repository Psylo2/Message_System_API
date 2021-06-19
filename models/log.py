from db.data_base import db, insert_timestamp


class LogModel(db.Model):
    __tablename__ = 'logs'
    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.idx'), nullable=True)
    user = db.relationship('UserModel', foreign_keys=user_id)
    action = db.Column(db.String(65535), nullable=False)
    create_at = db.Column(db.Float, nullable=True)
    threat_lvl = db.Column(db.String(1), nullable=False)

    levels = ['L', 'M', 'H']

    def __init__(self, user_id: int, action: str, threat_lvl: str):
        self.user_id = user_id
        self.action = action
        if threat_lvl in self.levels:
            self.threat_lvl = threat_lvl
        self.create_at = insert_timestamp()

    def json(self):
        return {self.idx: [{"create_at": self.create_at,
                            "user_id": self.user_id,
                            "action": self.action,
                            "threat_lvl": self.threat_lvl}]}

    def save_to_db(self) -> None:
        """Save Log to DB"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Delete Log from DB"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, idx: int) -> "LogModel":
        """Find Log by idx"""
        return cls.query.filter_by(idx=idx).first()

    @classmethod
    def find_by_user_id(cls, user_id: int) -> "LogModel":
        """Find All Logs of a User by user.idx, order by newest"""
        return cls.query.filter_by(user_id=user_id).order_by(db.desc(LogModel.idx)).all()

    @classmethod
    def find_all_logs(cls) -> "LogModel":
        """Find all Log by idx, order by newest"""
        return cls.query.all()

    @classmethod
    def find_by_level(cls, threat_lvl: str) -> "LogModel":
        """Find all Log by Threat Level, order by newest"""
        return cls.query.filter_by(threat_lvl=threat_lvl).order_by(db.desc(LogModel.idx)).all()

    @classmethod
    def find_user_and_level(cls, idx: int, threat_lvl: str) -> "LogModel":
        """return all logs osearch by level of threat and user, order by newest message"""
        return cls.query.filter_by(idx=idx, threat_lvl=threat_lvl).order_by(db.desc(LogModel.idx)).all()
