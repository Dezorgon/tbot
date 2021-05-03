import traceback
from ticketService import app
from ticketService import db
from ticketService.tickets_models import Concert, Tickets, Sold
from ticketService.sold_tickets_db import create_sold_tickets
from datetime import datetime


def create_concert(name: str, date: datetime, city: str,
                   place: str, tickets: [Tickets], sold_tickets: [Sold] = None,
                   description: str = None):
    try:
        if sold_tickets is None:
            for t in tickets:
                sold_tickets = create_sold_tickets(0, type=t.type)
        new_concert = Concert(name, date, city, place, description,
                              tickets=tickets, sold_tickets=sold_tickets)
        db.session.add(new_concert)
        db.session.commit()

        return {'ok': True}

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

            return {'ok': True}

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
