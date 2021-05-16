import traceback

from ticketsService import app
from ticketsService import db
from ticketsService.tickets_models import Sold, Type


def create_sold_tickets(count: int, concert_id: int, user_id: int,
                        tickets_type: Type = None, tickets_type_name: str = None):
    try:
        _type = None
        if tickets_type_name:
            _type = Type.query.filter_by(type=tickets_type_name).first()
            if _type is None:
                _type = Type(tickets_type_name)
                Type.query.add(_type)
        elif tickets_type:
            _type = tickets_type

        new_sold_tickets = Sold(count, concert_id, user_id)
        if _type:
            new_sold_tickets.type = _type

        db.session.add(new_sold_tickets)
        db.session.commit()

        return {'ok': True, 'sold_ticket': new_sold_tickets}

    except Exception as ex:
        stacktrace = traceback.format_exc()
        app.logger.debug(stacktrace)
        db.session.rollback()
        return {'ok': False}


def read_concert_sold_tickets(_id):
    if _id:
        sold_tickets = Sold.query.filter_by(id=_id).first()
        if sold_tickets:
            return {'ok': True, 'sold_ticket': sold_tickets}
    return {'ok': False}


def filter_sold_tickets(concert_id=None, user_id=None, type_id=None, type_name=None):
    _type = None
    if type_name:
        _type = Type.query.filter_by(type=type_name).first()
        if _type is None:
            _type = Type(type_name)
            db.session.add(_type)

    if type_id is None and _type:
        type_id = _type.id

    sold_tickets = None
    if concert_id:
        sold_tickets = Sold.query.filter_by(concert_id=concert_id).all()
    if user_id:
        sold_tickets = Sold.query.filter_by(user_id=user_id).all()
    if type_id:
        sold_tickets = Sold.query.filter_by(type_id=type_id).all()

    if sold_tickets:
        return {'ok': True, 'sold_tickets': sold_tickets}
    return {'ok': False}


# def read_all_concert_sold_tickets_by_concert_id(_id):
#     if _id:
#         sold_tickets = Sold.query.filter_by(concert_id=_id).all()
#         if sold_tickets:
#             return {'ok': True, 'all_sold_tickets': sold_tickets}
#     return {'ok': False}
#
#
# def read_all_concert_sold_tickets_by_user_id(_id):
#     if _id:
#         sold_tickets = Sold.query.filter_by(user_id=_id).all()
#         if sold_tickets:
#             return {'ok': True, 'all_sold_tickets': sold_tickets}
#     return {'ok': False}


def update_sold_tickets(_id: int, count: int = None, concert_id: int = None, user_id: int = None):
    if _id:
        sold_tickets = Sold.query.filter_by(id=_id).first()

        if sold_tickets:
            if count:
                sold_tickets.count = count
            if concert_id:
                sold_tickets.concert_id = concert_id
            if user_id:
                sold_tickets.user_id = user_id

            db.session.add(sold_tickets)
            db.session.commit()

            return {'ok': True, 'sold_tickets': sold_tickets}

    return {'ok': False}


# def increment_sold_tickets(_id: int):
#     if _id:
#         sold_tickets = Sold.query.filter_by(id=_id).first()
#
#         if sold_tickets:
#             sold_tickets['count'] += 1
#
#             sold_tickets.update()
#             db.session.commit()
#
#             return {'ok': True, 'sold_tickets': sold_tickets}
#
#     return {'ok': False}
#
#
# def increment_sold_tickets_by_user_id(user_id: int):
#     if user_id:
#         sold_tickets = Sold.query.filter_by(user_id=user_id).first()
#
#         if sold_tickets:
#             sold_tickets['count'] += 1
#
#             sold_tickets.update()
#             db.session.commit()
#
#             return {'ok': True, 'sold_tickets': sold_tickets}
#
#     return {'ok': False}


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
