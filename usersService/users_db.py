import traceback
from datetime import datetime

from usersService import app
from usersService import db
from usersService.users_models import User, Permission


def read_user(_id):
    if _id:
        user = User.query.filter_by(id=_id).first()
        if user:
            return {'ok': True, 'user': user}
    return {'ok': False}


def read_users():
    users = User.query.all()
    if users:
        return {'ok': True, 'users': users}
    return {'ok': False}


def read_user_by_external_id(external_id):
    if external_id:
        user = User.query.filter_by(external_id=external_id).first()
        if user:
            return {'ok': True, 'user': user}
    return {'ok': False}


def create_user(external_id: int = None, password_hash: str = None, first_name: str = None,
                last_name: str = None, phone: str = None, date: datetime = None,
                permission_id: int = None, permission_name: str = None):
    try:
        permission = None
        if permission_name:
            permission = Permission.query.filter_by(type=permission_name).first()
            if permission is None:
                permission = Permission(permission_name)
                db.session.add(permission)
        if permission_id:
            permission = Permission.query.filter_by(id=permission_id).first()
        new_user = User(first_name, last_name, phone, external_id, password_hash, date, permission=permission)

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
