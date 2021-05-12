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
    m = Message(chat_id, text, reply_markup=reply_markup)
    method = "sendMessage"
    data = m.to_json()
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
    app.logger.debug('123')
    chat_id = request.json["message"]["chat"]["id"]
    # b1 = KeyboardButton('Посмотреть концерты в моем городе')
    # b2 = KeyboardButton('2')
    # rm = ReplyKeyboardMarkup([[b1], [b2]])
    b1 = InlineKeyboardButton('123', callback_data='1')
    b2 = InlineKeyboardButton('456', callback_data='2')
    rm = InlineKeyboardMarkup([[b1], [b2]])
    send_message(chat_id, "на", rm)
    return {"ok": True}


if __name__ == '__main__':
    app.run(debug=True)
