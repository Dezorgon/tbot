from datetime import datetime
from ticketsService import db


class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    type = db.relationship('Type', lazy=True)
    count = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, count: int, price: int, concert_id: int, **kwargs):
        self.count = count
        self.price = price
        self.concert_id = concert_id
        super().__init__(**kwargs)

    def to_json(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        del d['type_id']
        d['type'] = self.type.type
        return d


class Sold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    type = db.relationship('Type', lazy=True)
    user_id = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __init__(self, count: int, concert_id: int, user_id: int, **kwargs):
        self.count = count
        self.concert_id = concert_id
        self.user_id = user_id
        super().__init__(**kwargs)

    def to_json(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        del d['type_id']
        d['type'] = self.type.type
        return d


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), nullable=False, unique=True)

    def __init__(self, type: str, **kwargs):
        self.type = type
        super().__init__(**kwargs)


class Concert(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    city = db.Column(db.String(128), nullable=False)
    place = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024))

    tickets = db.relationship('Tickets', lazy=True)
    sold_tickets = db.relationship('Sold', lazy=True)

    def __init__(self, name: str, date: datetime, city: str,
                 place: str, description: str = None, **kwargs):
        self.name = name
        self.date = date
        self.city = city
        self.place = place
        self.description = description
        super().__init__(**kwargs)

    def to_json(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d['date'] = str(d['date'])
        return d


db.create_all()
