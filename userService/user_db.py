import traceback
from userService import app
from userService import db
from userService.user_models import User, Permission


def read_user(_id):
    if _id:
        user = User.query.filter_by(id=_id).first()
        if user:
            return {'ok': True, 'user': user}
    return {'ok': False}


def read_user_by_chat_id(chat_id):
    if chat_id:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            return {'ok': True, 'user': user}
    return {'ok': False}


def create_user(permission_id: int, password_hash: str, first_name: str, last_name: str, phone: str, chat_id: int):
    try:
        permission = Permission.query.filter_by(id=permission_id).first()
        new_user = User(first_name, last_name, phone, chat_id, password_hash, permission=permission)

        db.session.add(new_user)
        db.session.commit()

        return {'ok': True}

    except Exception as ex:
        stacktrace = traceback.format_exc()
        app.logger.debug(stacktrace)
        db.session.rollback()
        return {'ok': False}


def update_user(_id, permission_id: int, password_hash: str, first_name: str, last_name: str, phone: str):
    raise NotImplemented


def delete_user(_id):
    if _id:
        try:
            User.query.filter_by(id=_id).delete()
            db.session.commit()

            return {'ok': True}

        except Exception as ex:
            stacktrace = traceback.format_exc()
            app.logger.debug(stacktrace)
            db.session.rollback()

            return {'ok': False}

