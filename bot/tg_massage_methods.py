import requests
import os

from bot.telegram_models.tg_models import Message

# token = os.environ['TOKEN']
token = '1801411028:AAE0FzT5Ntxm0o2jMNACLcKXMlaOkz0r5nU'
url = f"https://api.telegram.org/bot{token}/"


def send_message(chat_id, text, reply_markup=None):
    method = "sendMessage"
    m = Message(chat_id, text, reply_markup=reply_markup)
    data = m.to_json()
    response = requests.post(url + method, data=data)
    return response


def edit_message(chat_id, message_id, text, reply_markup=None):
    method = "editMessageText"
    m = Message(chat_id, text, reply_markup=reply_markup)
    data = m.to_json()
    data['message_id'] = message_id
    response = requests.post(url + method, data=data)


def delete_message(chat_id, message_id):
    method = "deleteMessage"
    data = {'chat_id': chat_id, 'message_id': message_id}
    response = requests.post(url + method, data=data)
