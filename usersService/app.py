import traceback
from datetime import datetime

from flask import request, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from usersService import app, db
from usersService.users_models import User, Permission
import users_db


admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Permission, db.session))


@app.route("/", methods=["GET", "POST"])
def index():
    return jsonify('usersService')


@app.route("/signup", methods=["POST"])
def signup():
    app.logger.debug(request.json)
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    permission = request.json.get('permission')
    phone = request.json.get('phone')
    password_hash = request.json.get('password_hash')
    external_id = request.json.get('external_id')
    date = datetime.strptime(request.json.get('date'), '%d.%m.%Y')

    response = users_db.create_user(permission_name=permission, password_hash=password_hash,
                                    first_name=first_name, last_name=last_name, phone=phone,
                                    external_id=external_id, date=date)

    if response['ok']:
        response = dict(**response, **{'message': 'signup'})

    return jsonify(response)


@app.route("/login", methods=["POST"])
def login():
    app.logger.debug(request.json)
    try:
        external_id = request.json['external_id']
        password_hash = request.json.get('password_hash')
        response = users_db.read_user_by_external_id(external_id)

        if response['ok']:
            user = response['user']

            if password_hash:
                if user.password_hash == password_hash:
                    response = dict(**response, **{'massage': 'login'})
                else:
                    response = dict(**response, **{'massage': 'wrong password'})

            response['user'] = user.to_json()
            response['user']['permission'] = str(user.permission)
            response['user']['date'] = user.date.strftime('%d.%m.%Y')
            # del response['user']['permission_id']
        else:
            response['ok'] = False
            response = dict(**response, **{'massage': 'user is not registered'})

        return jsonify(response)

    except Exception as ex:
        stacktrace = traceback.format_exc()
        app.logger.debug(stacktrace)
        db.session.rollback()
        return jsonify({'ok': False})


@app.route("/user/<_id>", methods=["GET"])
def get_user(_id):
    if 'chat_id' in request.json:
        response = users_db.read_user_by_external_id(_id)
    else:
        response = users_db.read_user(_id)

    if 'user' in response:
        response['user'] = response['user'].to_json()
    return jsonify(response)


@app.route("/user", methods=["GET"])
def get_users():
    response = users_db.read_users()

    if 'users' in response:
        for i in range(len(response['users'])):
            response['users'][i] = response['users'][i].to_json()
    return jsonify(response)

