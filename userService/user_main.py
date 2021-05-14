import traceback
from datetime import datetime

from flask import request, jsonify
from userService import app, db
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import user_db


@app.route("/", methods=["GET", "POST"])
def index():
    return jsonify('userService')


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

    response = user_db.create_user(permission_name=permission, password_hash=password_hash,
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
        response = user_db.read_user_by_external_id(external_id)

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
        response = user_db.read_user_by_external_id(_id)
    else:
        response = user_db.read_user(_id)

    if 'user' in response:
        response['user'] = response['user'].to_json()
    return jsonify(response)


# @app.route("/user/chat_id/<chat_id>", methods=["GET"])
# def get_user_by_chat_id(chat_id):
#     response = user_db.read_user_by_chat_id(chat_id)
#     if 'user' in response:
#         response['user'] = response['user'].to_json()
#     return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=81)
