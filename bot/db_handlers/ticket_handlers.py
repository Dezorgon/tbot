from flask import request
import requests

from bot import ticket_pagination, concert_pagination
from bot.db_handlers.login_handlers import login, register
from bot.markup import get_start_markup, ticket_markup
from bot.server_models.ticket import Ticket
from bot.db_handlers.tg_massage_methods import send_message, edit_message, delete_message
from bot import app, handler


@handler.message_handler(callback=['buy_ticket'])
def buy_ticket(external_id, massage):
    user_db_response = login(external_id)
    if user_db_response['ok']:
        user = user_db_response['user']
        assert user.external_id == external_id

        data = {'user_id': external_id, 'type': ticket_pagination.current(external_id).type}
        response = requests.post(app.config['TICKETS_DB_URL'] + 'concerts/' +
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


@handler.message_handler(callback=['buy'])
def find_ticket_by_concert_id(external_id, massage):
    concert = concert_pagination.current(external_id)
    response = {"ok": False}
    if concert:
        response = requests.get(app.config['TICKETS_DB_URL'] + 'concerts/' + str(concert.id) + '/tickets')
        response = response.json()

    if not response['ok']:
        send_tickets_representation_message(external_id, "Видимо на этот концерт еще нет билетов", [])
        return {"ok": False}

    send_tickets_representation_message(external_id, str(Ticket(response['tickets'][0])),
                                        response['tickets'], ticket_markup)
    return {"ok": True}
