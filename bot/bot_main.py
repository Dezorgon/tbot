import json
from flask import Flask, request
import requests

from bot.message_handler import message_handler
from bot.tg_models import *
from bot import app


token = "1783536914:AAGKrclSrCaPUZCsZt-8I3qiPmjIf24cCu0"
url = f"https://api.telegram.org/bot{token}/"


def receive_update():
    if request.method == "POST":
        app.logger.debug(request.json)
        # if request.json["message"]["entities"]["type"] == "bot_command":
        # process_commands()
        chat_id = request.json["message"]["chat"]["id"]
        send_message(chat_id, "qwerty")
    return {"ok": True}


def send_message(chat_id, text, reply_markup):
    method = "sendMessage"
    m = Message(chat_id, text, reply_markup=reply_markup)
    data = m.to_json()
    app.logger.debug(data)
    requests.post(url + method, data=data)


def edit_message(chat_id, message_id, text, reply_markup=None):
    method = "editMessageText"
    m = Message(chat_id, text, reply_markup=reply_markup)
    data = m.to_json()
    data['message_id'] = message_id
    app.logger.debug(data)
    requests.post(url + method, data=data)


@message_handler(commands=['/start', '/help'])
def process_commands():
    chat_id = request.json["message"]["chat"]["id"]
    b1 = KeyboardButton('Посмотреть концерты в моем городе')
    b2 = KeyboardButton('2')
    rm = ReplyKeyboardMarkup([[b1], [b2]])
    send_message(chat_id, "Здесь ты можешь купить билеты", rm)
    return {"ok": True}


@message_handler(message=['Посмотреть концерты в моем городе'])
def process_commands():
    chat_id = request.json["message"]["chat"]["id"]
    b1 = InlineKeyboardButton('123', callback_data='123')
    b2 = InlineKeyboardButton('456', callback_data='456')
    rm = InlineKeyboardMarkup([[b1], [b2]])
    send_message(chat_id, "на", rm)
    return {"ok": True}


@message_handler(callback=['123'])
def process_commands():
    app.logger.debug('123')
    chat_id = request.json["callback_query"]["message"]["chat"]["id"]
    message_id = request.json["callback_query"]["message"]["message_id"]
    b1 = InlineKeyboardButton('kek', callback_data='1')
    b2 = InlineKeyboardButton('lol', callback_data='2')
    rm = InlineKeyboardMarkup([[b1], [b2]])
    edit_message(chat_id, message_id, "not", rm)
    return {"ok": True}


if __name__ == '__main__':
    app.run(debug=True)
