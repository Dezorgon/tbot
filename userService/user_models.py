from datetime import datetime
from userService import db


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return f'permission {self.type}'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))
    permission = db.relationship('Permission', lazy=True)
    chat_id = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    phone = db.Column(db.String(128))

    def __init__(self, first_name: str, last_name: str, phone: str,
                 chat_id: int, password_hash: str, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.chat_id = chat_id
        self.password_hash = password_hash
        super().__init__(**kwargs)

    def __repr__(self):
        return f'user {self.id}'

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


db.create_all()
