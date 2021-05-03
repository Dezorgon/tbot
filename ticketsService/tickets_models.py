from datetime import datetime
from ticketService import db


class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    type = db.relationship('Type', lazy=True)
    count = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, count: int, price: int, **kwargs):
        self.count = count
        self.price = price
        super().__init__(**kwargs)


class Sold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    type = db.relationship('Type', lazy=True)
    user_id = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __init__(self, count: int, **kwargs):
        self.count = count
        super().__init__(**kwargs)


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

    def __repr__(self):
        return f'concert {self.id}'

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


db.create_all()
