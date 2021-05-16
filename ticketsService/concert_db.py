import traceback

from ticketsService import app
from ticketsService import db
from ticketsService.tickets_models import Concert, Tickets, Sold
from datetime import datetime


def create_concert(name: str, date: datetime, city: str,
                   place: str, tickets: [Tickets] = None, sold_tickets: [Sold] = None,
                   description: str = None):
    try:
        # if sold_tickets is None:
        #     sold_tickets = []
        #     for t in tickets:
        #         sold_tickets.append(create_sold_tickets(0, t.type))

        new_concert = Concert(name, date, city, place, description)
        if tickets:
            new_concert.tickets = tickets
        if sold_tickets:
            new_concert.sold_tickets = sold_tickets

        db.session.add(new_concert)
        db.session.commit()

        return {'ok': True, 'concert': new_concert}

    except Exception as ex:
        stacktrace = traceback.format_exc()
        app.logger.debug(stacktrace)
        db.session.rollback()
        return {'ok': False}


def read_concert(_id):
    if _id:
        concert = Concert.query.filter_by(id=_id).first()
        if concert:
            return {'ok': True, 'concert': concert}
    return {'ok': False}


def read_top_concerts(count):
    tickets = Concert.query.order_by(Concert.date).limit(count).all()
    if tickets:
        return {'ok': True, 'concerts': tickets}
    return {'ok': False}


def read_concerts_by_city(city):
    if city:
        concerts = Concert.query.filter_by(city=city).all()
        if concerts:
            return {'ok': True, 'concerts': concerts}
    return {'ok': False}


def update_concert(_id: int, name: str = None, date: datetime = None,
                   city: str = None, place: str = None,
                   tickets: [Tickets] = None, sold_tickets: [Sold] = None,
                   description: str = None):
    d = {'name': name, 'date': date, 'city': city, 'place': place,
         'description': description, 'tickets': tickets, 'sold_tickets': sold_tickets}

    if _id:
        concert = Concert.query.filter_by(id=_id).first()

        if concert:
            for k in d:
                if d[k]:
                    concert['k'] = d[k]

            concert.update()
            db.session.commit()

            return {'ok': True, 'concert': concert}

    return {'ok': False}


def delete_concert(_id):
    if _id:
        try:
            Concert.query.filter_by(id=_id).delete()
            db.session.commit()

            return {'ok': True}

        except Exception as ex:
            stacktrace = traceback.format_exc()
            app.logger.debug(stacktrace)
            db.session.rollback()

            return {'ok': False}
