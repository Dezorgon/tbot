import requests

from bot import app
from bot.tg_models import Message


url = f"https://api.telegram.org/bot{token}/"


def send_message(chat_id, text, reply_markup=None):
    method = "sendMessage"
    m = Message(chat_id, text, reply_markup=reply_markup)
    data = m.to_json()
    app.logger.debug(data)
    response = requests.post(url + method, data=data)
    return response


def edit_message(chat_id, message_id, text, reply_markup=None):
    method = "editMessageText"
    m = Message(chat_id, text, reply_markup=reply_markup)
    data = m.to_json()
    data['message_id'] = message_id
    app.logger.debug(data)
    requests.post(url + method, data=data)


def delete_message(chat_id, message_id):
    method = "deleteMessage"
    data = {'chat_id': chat_id, 'message_id': message_id}
    requests.post(url + method, data=data)
