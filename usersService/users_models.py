from datetime import datetime
from usersService import db


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), nullable=False, unique=True)

    def __init__(self, type_name: str):
        self.type = type_name

    def __repr__(self):
        return f'{self.type}'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))
    permission = db.relationship('Permission', lazy=True)
    external_id = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    date = db.Column(db.DateTime)
    phone = db.Column(db.String(128))

    def __init__(self, first_name: str, last_name: str, phone: str,
                 external_id: int, password_hash: str, date: datetime, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.external_id = external_id
        self.password_hash = password_hash
        self.date = date
        super().__init__(**kwargs)

    def __repr__(self):
        return f'user {self.id}'

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns
                if getattr(self, c.name) is not None}


db.create_all()
