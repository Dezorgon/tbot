import traceback
from ticketService import app
from ticketService import db
from ticketService.tickets_models import Tickets, Type


def create_tickets(count: int, price: int, tickets_type: Type = None, tickets_type_name: str = None):
    try:
        if tickets_type_name:
            _type = Type.query.filter_by(type=tickets_type_name).first()
            if _type is None:
                _type = Type(tickets_type_name)
                Type.query.add(_type)
        elif tickets_type:
            _type = tickets_type
            
        new_tickets = Tickets(count, price, type=_type)
        db.session.add(new_tickets)
        db.session.commit()

        return {'ok': True}

    except Exception as ex:
        stacktrace = traceback.format_exc()
        app.logger.debug(stacktrace)
        db.session.rollback()
        return {'ok': False}


def read_concert_tickets(_id):
    if _id:
        tickets = Tickets.query.filter_by(id=_id).first()
        if tickets:
            return {'ok': True, 'tickets': tickets}
    return {'ok': False}


def read_all_concert_tickets_by_concert_id(_id):
    if _id:
        tickets = Tickets.query.filter_by(concert_id=_id)
        if tickets:
            return {'ok': True, 'tickets': tickets}
    return {'ok': False}


def update_tickets(_id: int, count: int = None, price: int = None, type_id: int = None, tickets_type: str = None):
    if _id:
        tickets = Tickets.query.filter_by(id=_id).first()

        if tickets:
            if count:
                tickets['count'] = count
            if price:
                tickets['price'] = price
            if type_id:
                tickets.type = Type.query.filter_by(id=type_id).first()
            elif tickets_type:
                tickets.type = Type.query.filter_by(type=tickets_type).first()

            tickets.update()
            db.session.commit()

            return {'ok': True}

    return {'ok': False}


def delete_tickets(_id):
    if _id:
        try:
            Tickets.query.filter_by(id=_id).delete()
            db.session.commit()

            return {'ok': True}

        except Exception as ex:
            stacktrace = traceback.format_exc()
            app.logger.debug(stacktrace)
            db.session.rollback()

            return {'ok': False}
