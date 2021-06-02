from flask import request
import requests_async as requests

from bot import concert_pagination
from bot.markup import concert_markup
from bot.server_models.concert import Concert
from bot.tg_massage_methods import send_message, edit_message, delete_message
from bot import app, handler


@handler.message_handler(callback=['next_concert', 'previous_concert'])
async def represent_concerts(external_id, massage):
    message_id = massage["message_id"]
    callback = request.json["callback_query"]["data"]

    concert = None
    if callback == 'next_concert':
        concert = concert_pagination.next(external_id)
    if callback == 'previous_concert':
        concert = concert_pagination.prev(external_id)

    edit_message(external_id, message_id, concert, concert_markup)
    return {"ok": True}


async def find_concert_by_city(external_id, massage):
    city = massage["text"]

    response = await requests.get(app.config['TICKETS_DB_URL'] + 'concerts/' + city)
    response = response.json()

    if not response['ok']:
        send_concerts_representation_message(external_id, "Я не нашел концертов в этом городе", [])
        return {"ok": False}

    send_concerts_representation_message(external_id, str(Concert(response['concerts'][0])),
                                         response['concerts'], concert_markup)
    return {"ok": True}


def send_concerts_representation_message(chat_id, text, concerts, markup=None):
    if chat_id in concert_pagination.massage_id:
        delete_message(chat_id, concert_pagination.massage_id[chat_id])

    resp = send_message(chat_id, text, markup)
    resp = resp.json()

    concert_pagination.set(concerts, chat_id, resp['result']['message_id'])


@handler.message_handler(message=['Посмотреть концерты в моем городе'], next_func=find_concert_by_city)
async def request_city_to_find_concert(external_id, massage):
    send_message(external_id, "В каком городе будем искать?")
    return {"ok": True}


@handler.message_handler(callback=['see_details'])
async def see_details(external_id, massage):
    send_message(external_id, concert_pagination.current(external_id), concert_markup)


@handler.message_handler(message=['Ближайшие концерты'])
async def get_top_concerts(external_id, massage):
    response = await requests.get(app.config['TICKETS_DB_URL'] + 'concerts/top/' + str(10))
    response = response.json()

    app.logger.debug(response)

    if not response['ok']:
        send_concerts_representation_message(external_id, "Хм, нет концертов?", [])
        return {"ok": False}

    send_concerts_representation_message(external_id, str(Concert(response['concerts'][0])),
                                         response['concerts'], concert_markup)
    return {"ok": True}
