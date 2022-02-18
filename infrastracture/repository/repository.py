from flask_sqlalchemy import SQLAlchemy


class Repository:
    def __new__(cls, *args, **kwargs):
        return SQLAlchemy()


repository: SQLAlchemy = Repository()
