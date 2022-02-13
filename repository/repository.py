from flask_sqlalchemy import SQLAlchemy


class Repository:
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        return SQLAlchemy()


repository = Repository()
