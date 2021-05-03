import traceback
from flask import request, jsonify
from userService import app, db
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import user_db


@app.route("/", methods=["GET", "POST"])
def index():
    return jsonify('userService')


@app.route("/signup", methods=["POST"])
def signup():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    permission = request.json['permission']
    phone = request.json['phone']
    password_hash = request.json['password_hash']
    chat_id = request.json['chat_id']

    response = user_db.create_user(permission, password_hash, first_name, last_name, phone, chat_id)

    if response['ok']:
        response = dict(**response, **{'message': 'signup'})

    return jsonify(response)


@app.route("/login", methods=["POST"])
def login():
    try:
        chat_id = request.json['chat_id']
        password_hash = request.json['password_hash']
        user = user_db.read_user_by_chat_id(chat_id)

        response = {'ok': True}

        if user:
            if user.password_hash == password_hash:
                response = dict(**response, **{'massage': 'login'})
            else:
                response = dict(**response, **{'massage': 'wrong password'})
        else:
            response['ok'] = False
            response = dict(**response, **{'massage': 'user is not registered'})

        return jsonify(response)

    except Exception as ex:
        stacktrace = traceback.format_exc()
        app.logger.debug(stacktrace)
        db.session.rollback()
        return jsonify({'ok': False})


@app.route("/getuser/<_id>", methods=["GET"])
def get_user(_id):
    response = user_db.read_user(_id)
    if 'user' in response:
        response['user'] = response['user'].to_json()
    return jsonify(response)


@app.route("/getuser/chat_id/<chat_id>", methods=["GET"])
def get_user_by_chat_id(chat_id):
    response = user_db.read_user_by_chat_id(chat_id)
    if 'user' in response:
        response['user'] = response['user'].to_json()
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
