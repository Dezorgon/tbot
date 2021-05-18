from flask import request
import requests
from random import randint
import os

from dialog.dialog_bot import DialogBot
from dialog.registration_dialog import register_dialog
from updater import Updater
from markup import get_start_markup, ticket_markup, concert_markup
from models.concert import Concert
from models.ticket import Ticket
from models.user import User
from tg_massage_methods import send_message, edit_message, delete_message
from bot import app
from message_handler import Handler
from models.concert_pagination import ConcertPagination
from models.ticket_pagination import TicketPagination

handler = Handler()  # session
updater = Updater([handler.send_message])

dialog = DialogBot(register_dialog, updater)

concert_pagination = ConcertPagination()
ticket_pagination = TicketPagination()

not_handled_answers = ['У меня вообще-то команды есть', 'Что с тобой не так?',
                       'Чел ты', 'Мне кажется тебе не нужны билеты']


@app.route('/', methods=["GET", "POST"])
def main():
    app.logger.debug('main')

    if 'callback_query' in request.json:
        external_id = request.json["callback_query"]["from"]["id"]
        message = request.json["callback_query"]["message"]
    else:
        external_id = request.json["message"]["from"]["id"]
        message = request.json["message"]

    is_handled = updater.update(external_id, message)

    if not is_handled:
        text = not_handled_answers[randint(0, len(not_handled_answers)-1)]
        send_message(external_id, text, get_start_markup(True))

    return {'ok': True}


def process_register_dialog(external_id, massage):
    text = massage["text"]
    dialog.handle_message(external_id, text)


@handler.message_handler(commands=['/start'])
def process_start_command(external_id, massage):
    if not login(external_id)['ok']:
        register(external_id, massage)
    else:
        process_help_command(external_id, massage)
    return {"ok": True}


@handler.message_handler(commands=['/help'])
def process_help_command(external_id, massage):
    send_message(external_id, "Здесь ты можешь купить билеты", get_start_markup(login(external_id)['ok']))
    return {"ok": True}


@handler.message_handler(callback=['accept_register_data'])
def input_registration_data(external_id, massage):
    text = massage["text"].split()

    first_name = text[0]
    last_name = text[1]
    date = text[2]
    permission = 'user'

    response = requests.post(f'http://{os.environ["USERS_DB_HOST"]}:81/signup',
                             json={'first_name': first_name, 'last_name': last_name,
                                   'external_id': external_id, 'date': date,
                                   'permission': permission})
    response = response.json()

    if not response['ok']:
        send_message(external_id, "Что-то пошло не так")
        register()
    else:
        if login(external_id)['ok']:
            send_message(external_id, "Ок", get_start_markup(True))


def login(external_id):
    response = requests.post(f'http://{os.environ["USERS_DB_HOST"]}:81/login', json={'external_id': external_id})
    response = response.json()
    app.logger.debug(response)

    if response['ok']:
        user = response['user']
        user = User(user['id'], external_id, user['first_name'],
                    user['last_name'], user['date'], user['permission'])
        return {'ok': True, 'user': user}
    else:
        return {'ok': False}


@handler.message_handler(message=['Профиль'])
def represent_profile(external_id, massage):
    login(external_id)

    response = requests.get(f'http://{os.environ["TICKETS_DB_HOST"]}:80/sold_tickets/' + str(external_id))
    response = response.json()

    user_db_response = login(external_id)
    if user_db_response['ok']:
        user = user_db_response['user']

        text = f'{user.last_name} {user.first_name}\n\nБилеты:\n'
        if response['ok']:
            sold_tickets = response['sold_tickets']
            for ticket in sold_tickets:
                text += f'{ticket["concert"]} {ticket["type"]} {ticket["count"]}шт\n'
        send_message(external_id, text)

        return {"ok": True}

    send_message(external_id, "Зарегистрируйтесь", get_start_markup(False))
    return {"ok": False}


@handler.message_handler(message=['Регистрация'], callback=['re_register'])
def register(external_id, massage):
    app.logger.debug('register')
    updater.intercept_routing(external_id, process_register_dialog)
    process_register_dialog(external_id, massage)
    return {"ok": True}


# def re_register():
#     external_id = request.json["callback_query"]["from"]["id"]
#     app.logger.debug('re_register')
#     updater.intercept_routing(external_id, process_register_dialog)
#     process_register_dialog()
#     return {"ok": True}


@handler.message_handler(callback=['buy_ticket'])
def buy_ticket(external_id, massage):
    user_db_response = login(external_id)
    if user_db_response['ok']:
        user = user_db_response['user']
        assert user.external_id == external_id

        data = {'user_id': external_id, 'type': ticket_pagination.current(external_id).type}
        response = requests.post(f'http://{os.environ["TICKETS_DB_HOST"]}:80/concerts/' +
                                 str(concert_pagination.current(external_id).id) + "/buy", json=data)
        response = response.json()
        app.logger.debug(response)

        if response['ok']:
            send_message(external_id, 'Ну купил ты билет, а дальше то что?',
                         get_start_markup(True))
    else:
        register(external_id, massage)

    return {"ok": True}


@handler.message_handler(callback=['next_ticket', 'previous_ticket'])
def represent_ticket_by_concert_id(external_id, massage):
    message_id = massage["message_id"]
    callback = request.json["callback_query"]["data"]

    ticket = None
    if callback == 'next_ticket':
        ticket = ticket_pagination.next(external_id)
    if callback == 'previous_ticket':
        ticket = ticket_pagination.prev(external_id)

    edit_message(external_id, message_id, ticket, ticket_markup)
    return {"ok": True}


def send_tickets_representation_message(chat_id, text, tickets, markup=None):
    if chat_id in ticket_pagination.massage_id:
        delete_message(chat_id, ticket_pagination.massage_id[chat_id])

    resp = send_message(chat_id, text, markup)
    resp = resp.json()

    ticket_pagination.set(tickets, chat_id, resp['result']['message_id'])


def send_concerts_representation_message(chat_id, text, concerts, markup=None):
    if chat_id in concert_pagination.massage_id:
        delete_message(chat_id, concert_pagination.massage_id[chat_id])

    resp = send_message(chat_id, text, markup)
    resp = resp.json()

    concert_pagination.set(concerts, chat_id, resp['result']['message_id'])


@handler.message_handler(callback=['buy'])
def find_ticket_by_concert_id(external_id, massage):
    concert = concert_pagination.current(external_id)
    response = {"ok": False}
    if concert:
        response = requests.get(f'http://{os.environ["TICKETS_DB_HOST"]}:80/concerts/' + str(concert.id) + '/tickets')
        response = response.json()

    if not response['ok']:
        send_tickets_representation_message(external_id, "Видимо на этот концерт еще нет билетов", [])
        return {"ok": False}

    send_tickets_representation_message(external_id, str(Ticket(response['tickets'][0])),
                                        response['tickets'], ticket_markup)
    return {"ok": True}


@handler.message_handler(callback=['next_concert', 'previous_concert'])
def represent_concerts(external_id, massage):
    message_id = massage["message_id"]
    callback = request.json["callback_query"]["data"]

    concert = None
    if callback == 'next_concert':
        concert = concert_pagination.next(external_id)
    if callback == 'previous_concert':
        concert = concert_pagination.prev(external_id)

    edit_message(external_id, message_id, concert, concert_markup)
    return {"ok": True}


def find_concert_by_city(external_id, massage):
    city = massage["text"]

    response = requests.get(f'http://{os.environ["TICKETS_DB_HOST"]}:80/concerts/' + city)
    response = response.json()

    if not response['ok']:
        send_concerts_representation_message(external_id, "Я не нашел концертов в этом городе", [])
        return {"ok": False}

    send_concerts_representation_message(external_id, str(Concert(response['concerts'][0])),
                                         response['concerts'], concert_markup)
    return {"ok": True}


@handler.message_handler(message=['Посмотреть концерты в моем городе'], next_func=find_concert_by_city)
def request_city_to_find_concert(external_id, massage):
    send_message(external_id, "В каком городе будем искать?")
    return {"ok": True}


@handler.message_handler(callback=['see_details'])
def see_details(external_id, massage):
    send_message(external_id, concert_pagination.current(external_id), concert_markup)


@handler.message_handler(message=['Ближайшие концерты'])
def get_top_concerts(external_id, massage):
    response = requests.get(f'http://{os.environ["TICKETS_DB_HOST"]}:80/concerts/top/' + str(10))
    response = response.json()
    app.logger.debug(response)

    if not response['ok']:
        send_concerts_representation_message(external_id, "Хм, нет концертов?", [])
        return {"ok": False}

    send_concerts_representation_message(external_id, str(Concert(response['concerts'][0])),
                                         response['concerts'], concert_markup)
    return {"ok": True}


# if __name__ == '__main__':
#     app.run(debug=True)
