from flask import request
import requests

from bot.models.user import User
from bot.tg_models import *
from bot import app
from bot.message_handler import Handler
from bot.models.concert_pagination import ConcertPagination
from bot.models.ticket_pagination import TicketPagination

token = "1783536914:AAGKrclSrCaPUZCsZt-8I3qiPmjIf24cCu0"
url = f"https://api.telegram.org/bot{token}/"

handler = Handler()  # сессии
concert_pagination = ConcertPagination()
ticket_pagination = TicketPagination()
current_user = User()

b1 = InlineKeyboardButton('<', callback_data='previous_concert')
b2 = InlineKeyboardButton('>', callback_data='next_concert')
b3 = InlineKeyboardButton('купить билет', callback_data='buy')
concert_markup = InlineKeyboardMarkup([[b1, b2], [b3]])

b1 = InlineKeyboardButton('<', callback_data='previous_ticket')
b2 = InlineKeyboardButton('>', callback_data='next_ticket')
b3 = InlineKeyboardButton('купить', callback_data='buy_ticket')
ticket_markup = InlineKeyboardMarkup([[b1, b2], [b3]])


@app.route('/', methods=["GET", "POST"])
def main():
    return handler.send_message()


def send_message(chat_id, text, reply_markup=None):
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


@handler.message_handler(commands=['/start', '/help'])
def process_commands():
    chat_id = request.json["message"]["chat"]["id"]
    b1 = KeyboardButton('Посмотреть концерты в моем городе')
    b2 = KeyboardButton('Ближайшие концерты')
    rm = ReplyKeyboardMarkup([[b1], [b2]])
    send_message(chat_id, "Здесь ты можешь купить билеты", rm)
    return {"ok": True}


def input_registration_data():
    data = request.json["message"]["text"]
    data = data.split()
    current_user.set(data[1], data[0], data[3])


def login():
    # проверка id в бд и запись в user
    response = requests.post('http://127.0.0.1:81/login', data={'chat_id': id})
    response = response.json()

    if response['ok']:
        current_user.set()
    else:
        register()


@handler.message_handler(message=['Регистрация'], next_func=input_registration_data)
def register():
    # запись в бд и login  и запись в user
    chat_id = request.json["message"]["chat"]["id"]
    send_message(chat_id, "Фамилия Имя Дата рождения\nИванов Иван 16.03.1998")
    return {"ok": True}


@handler.message_handler(callback=['buy_ticket'])
def buy_ticket():
    if current_user.is_authenticated:
        pass
    # chat_id = request.json["callback_query"]["message"]["chat"]["id"]
    # message_id = request.json["callback_query"]["message"]["message_id"]
    #
    # concert = concert_pagination.current()
    # response = requests.get('http://127.0.0.1:80/concerts/' + str(concert.id) + '/tickets')
    # response = response.json()
    #
    # if not response['ok']:
    #     send_message(chat_id, "Видимо на этот концерт еще нет билетов")
    #     return {"ok": False}
    #
    # ticket_pagination.set(response['all_tickets'])
    #
    # b1 = InlineKeyboardButton('<', callback_data='previous_ticket')
    # b2 = InlineKeyboardButton('>', callback_data='next_ticket')
    # b3 = InlineKeyboardButton('купить', callback_data='buy_ticket')
    # markup = InlineKeyboardMarkup([[b1, b2], [b3]])
    #
    # send_message(chat_id, ticket_pagination.current(), markup)
    return {"ok": True}


@handler.message_handler(callback=['next_ticket', 'previous_ticket'])
def represent_ticket_by_concert_id():
    chat_id = request.json["callback_query"]["message"]["chat"]["id"]
    message_id = request.json["callback_query"]["message"]["message_id"]
    callback = request.json["callback_query"]["data"]

    ticket = None
    if callback == 'next_concert':
        ticket = ticket_pagination.next()
    if callback == 'previous_concert':
        ticket = ticket_pagination.prev()

    edit_message(chat_id, message_id, ticket, ticket_markup)
    return {"ok": True}


@handler.message_handler(callback=['buy'])
def find_ticket_by_concert_id():
    chat_id = request.json["callback_query"]["message"]["chat"]["id"]
    message_id = request.json["callback_query"]["message"]["message_id"]

    concert = concert_pagination.current()
    response = requests.get('http://127.0.0.1:80/concerts/' + str(concert.id) + '/tickets')
    response = response.json()

    if not response['ok']:
        send_message(chat_id, "Видимо на этот концерт еще нет билетов")
        return {"ok": False}

    ticket_pagination.set(response['all_tickets'])

    send_message(chat_id, ticket_pagination.current(), ticket_markup)
    return {"ok": True}


@handler.message_handler(callback=['next_concert', 'previous_concert'])
def represent_concert_by_city():
    chat_id = request.json["callback_query"]["message"]["chat"]["id"]
    message_id = request.json["callback_query"]["message"]["message_id"]
    callback = request.json["callback_query"]["data"]

    concert = None
    if callback == 'next_concert':
        concert = concert_pagination.next()
    if callback == 'previous_concert':
        concert = concert_pagination.prev()

    edit_message(chat_id, message_id, concert, concert_markup)
    return {"ok": True}


def find_concert_by_city():
    chat_id = request.json["message"]["chat"]["id"]
    city = request.json["message"]["text"]

    response = requests.get('http://127.0.0.1:80/concerts/' + city)
    response = response.json()

    if not response['ok']:
        send_message(chat_id, "Я не нашел концертов в этом городе")
        return {"ok": False}

    concert_pagination.set(response['concerts'])

    send_message(chat_id, concert_pagination.current(), concert_markup)
    return {"ok": True}


@handler.message_handler(message=['Посмотреть концерты в моем городе'], next_func=find_concert_by_city)
def request_city_to_find_concert():
    chat_id = request.json["message"]["chat"]["id"]
    send_message(chat_id, "В каком городе будем искать?")
    return {"ok": True}


@handler.message_handler(message=['Ближайшие концерты'])
def process_commands2():
    chat_id = request.json["message"]["chat"]["id"]
    b1 = InlineKeyboardButton('123', callback_data='123')
    b2 = InlineKeyboardButton('456', callback_data='456')
    rm = InlineKeyboardMarkup([[b1], [b2]])
    send_message(chat_id, "на", rm)
    return {"ok": True}


if __name__ == '__main__':
    app.run(debug=True)
