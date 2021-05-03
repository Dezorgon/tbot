from datetime import datetime
from notificationService import db


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscription = db.relationship('Subscription', backref='subscribers', lazy=True, nullable=False)

    def __repr__(self):
        return 'sub'


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscriber_id = db.Column(db.Integer, db.ForeignKey('subscriber.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    type = db.relationship('Type', backref='subscriptions', lazy=True)
    webhook_id = db.Column(db.Integer, db.ForeignKey('webhook.id'), nullable=False)
    webhook = db.relationship('Webhook', backref='subscriptions', lazy=True)

    def __repr__(self):
        return 'podps'


class Webhook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1024), nullable=False)

    def __repr__(self):
        return self.url


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return 'type'


# db.create_all()
