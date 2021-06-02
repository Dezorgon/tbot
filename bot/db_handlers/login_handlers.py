import requests_async as requests
from datetime import datetime

from bot import dialog
from bot.markup import get_start_markup
from bot.server_models.user import User
from bot.tg_massage_methods import send_message
from bot import app, handler, updater


@handler.message_handler(callback=['accept_register_data'])
async def input_registration_data(external_id, massage):
    text = massage["text"].split()

    first_name = text[0]
    last_name = text[1]
    date = text[2]
    # try:
    #     date = datetime.strptime('%d.%m.%Y', text[2]).strftime('%d.%m.%Y')
    # except:
    #     send_message(external_id, "Напиши дату нормально")
    #     return

    permission = 'user'

    response = await requests.post(app.config['USERS_DB_URL'] + 'signup',
                                   json={'first_name': first_name, 'last_name': last_name,
                                         'external_id': external_id, 'date': date,
                                         'permission': permission})
    response = response.json()

    if not response['ok']:
        send_message(external_id, "Что-то пошло не так")

        await register()
    else:
        if (await login(external_id))['ok']:
            send_message(external_id, "Ок", get_start_markup(True))


async def login(external_id):
    response = await requests.post(app.config['USERS_DB_URL'] + 'login', json={'external_id': external_id})
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
async def represent_profile(external_id, massage):
    await login(external_id)

    response = await requests.get(app.config['TICKETS_DB_URL'] + 'sold_tickets/' + str(external_id))
    response = response.json()

    user_db_response = await login(external_id)
    if user_db_response['ok']:
        user = user_db_response['user']

        text = f'{user.last_name} {user.first_name}\n\nБилеты:\n'
        if response['ok']:
            sold_tickets = response['sold_tickets']
            for ticket in sold_tickets:
                text += f'{ticket["concert"]}\t{ticket["type"]} {ticket["count"]}шт\n'
        send_message(external_id, text)

        return {"ok": True}

    send_message(external_id, "Зарегистрируйтесь", get_start_markup(False))
    return {"ok": False}


@handler.message_handler(message=['Регистрация'], callback=['re_register'])
async def register(external_id, massage):
    response = await login(external_id)
    if not response['ok']:
        app.logger.debug('register')
        updater.intercept_routing(external_id, process_register_dialog)
        process_register_dialog(external_id, massage)
    else:
        send_message(external_id, "Братик, да ты уже зарегистрирован", get_start_markup(True))
    return {"ok": True}


def process_register_dialog(external_id, massage):
    text = massage["text"]
    ret = dialog.handle_message(external_id, text)
    return ret
