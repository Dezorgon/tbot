from flask import request, session
import requests

from bot.dialog.dialog_bot import DialogBot
from bot.dialog.registration_dialog import register_dialog
from bot.Updater import Updater
from bot.markup import get_start_markup, ticket_markup, concert_markup
from bot.models.user import User
from bot.tg_models import *
from bot import app
from bot.message_handler import Handler
from bot.models.concert_pagination import ConcertPagination
from bot.models.ticket_pagination import TicketPagination

token = "1783536914:AAGKrclSrCaPUZCsZt-8I3qiPmjIf24cCu0"
url = f"https://api.telegram.org/bot{token}/"

handler = Handler()  # сессии
updater = Updater([handler.send_message])

dialog = DialogBot(register_dialog, updater)

concert_pagination = ConcertPagination()
ticket_pagination = TicketPagination()

current_user = User()


# session


@app.route('/', methods=["GET", "POST"])
def main():
    app.logger.debug('main')

    if 'callback_query' in request.json:
        external_id = request.json["callback_query"]["from"]["id"]
    else:
        external_id = request.json["message"]["from"]["id"]

    updater.update(external_id)
    return {'ok': True}
    # return handler.send_message()


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


def process_dialog():
    chat_id = request.json["message"]["chat"]["id"]
    external_id = request.json["message"]["from"]["id"]
    text = request.json["message"]["text"]
    register_dialog.handle_message(chat_id, text)


@handler.message_handler(commands=['/start', '/help'])
def process_commands():
    chat_id = request.json["message"]["chat"]["id"]
    external_id = request.json["message"]["from"]["id"]

    current_user.external_id = external_id

    if not login(external_id):
        register(external_id)
    else:
        send_message(chat_id, "Здесь ты можешь купить билеты", get_start_markup(current_user.is_authenticated))
    return {"ok": True}


@handler.message_handler(callback=['accept_register_data'])
def input_registration_data():
    external_id = request.json["callback_query"]["from"]["id"]
    text = request.json["callback_query"]["message"]["text"].split()
    app.logger.debug(register_dialog.input_data[external_id])
    first_name = text[0]
    last_name = text[1]
    date = text[2]
    permission = 'user'

    response = requests.post('http://127.0.0.1:81/signup',
                             json={'first_name': first_name, 'last_name': last_name,
                                   'external_id': external_id, 'date': date,
                                   'permission': permission})
    response = response.json()

    if not response['ok']:
        send_message(external_id, "Что-то пошло не так")
        register(external_id)
    else:
        login(external_id)


def login(external_id):
    response = requests.post('http://127.0.0.1:81/login', json={'external_id': external_id})
    response = response.json()
    app.logger.debug(response)

    if response['ok']:
        user = response['user']
        current_user.set(user['id'], external_id, user['first_name'],
                         user['last_name'], user['date'], user['permission'])

        send_message(external_id, "Я помню тебя)", get_start_markup())
        return True
    else:
        return False


def register(external_id):
    app.logger.debug('register')
    updater.intercept_routing(external_id, process_dialog)
    process_dialog()
    # send_message(chat_id, "Давай-ка ты оставишь нам свои данные)")
    # send_message(chat_id, "Фамилия Имя Дата рождения\nИванов Иван 16.03.1998")
    return {"ok": True}


@handler.message_handler(callback=['buy_ticket'])
def buy_ticket():
    if not current_user.is_authenticated:
        if not login(current_user.external_id):
            register(current_user.external_id)
    data = {'user_id': current_user.id, 'type': ticket_pagination.current().type}
    response = requests.post("http://127.0.0.1:80/concerts/" + str(concert_pagination.current().id) + "/buy", data=data)

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
