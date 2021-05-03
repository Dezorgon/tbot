import traceback
from ticketService import app
from ticketService import db
from ticketService.tickets_models import Sold


def create_sold_tickets(count: int):
    try:
        new_sold_tickets = Sold(count)
        db.session.add(new_sold_tickets)
        db.session.commit()

        return {'ok': True}

    except Exception as ex:
        stacktrace = traceback.format_exc()
        app.logger.debug(stacktrace)
        db.session.rollback()
        return {'ok': False}


def read_concert_sold_tickets(_id):
    if _id:
        sold_tickets = Sold.query.filter_by(id=_id).first()
        if sold_tickets:
            return {'ok': True, 'sold_tickets': sold_tickets}
    return {'ok': False}


def read_all_concert_sold_tickets_by_concert_id(_id):
    if _id:
        sold_tickets = Sold.query.filter_by(concert_id=_id)
        if sold_tickets:
            return {'ok': True, 'sold_tickets': sold_tickets}
    return {'ok': False}


def read_all_concert_sold_tickets_by_user_id(_id):
    if _id:
        sold_tickets = Sold.query.filter_by(user_id=_id)
        if sold_tickets:
            return {'ok': True, 'sold_tickets': sold_tickets}
    return {'ok': False}


def update_sold_tickets(_id: int, count: int):
    if _id:
        sold_tickets = Sold.query.filter_by(id=_id).first()

        if sold_tickets and count:
            sold_tickets['count'] = count

            sold_tickets.update()
            db.session.commit()

            return {'ok': True}

    return {'ok': False}


def increment_sold_tickets(_id: int):
    if _id:
        tickets = Sold.query.filter_by(id=_id).first()

        if tickets:
            tickets['count'] += 1

            tickets.update()
            db.session.commit()

            return {'ok': True}

    return {'ok': False}


def delete_sold_tickets(_id):
    if _id:
        try:
            Sold.query.filter_by(id=_id).delete()
            db.session.commit()

            return {'ok': True}

        except Exception as ex:
            stacktrace = traceback.format_exc()
            app.logger.debug(stacktrace)
            db.session.rollback()

            return {'ok': False}
