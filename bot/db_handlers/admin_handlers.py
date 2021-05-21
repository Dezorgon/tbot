import requests

from bot.db_handlers.login_handlers import login, register
from bot.markup import get_start_markup
from bot.tg_massage_methods import send_message
from bot import handler, app


def input_notification(external_id, massage):
    text = massage["text"]

    response = requests.get(app.config['USERS_DB_URL'] + 'user')
    response = response.json()

    indices = []
    if response['ok']:
        for user in response['users']:
            indices.append(user['external_id'])
    else:
        return {"ok": False}

    for i in indices:
        send_message(i, text)

    return {"ok": True}


@handler.message_handler(commands=['/notify'], next_func=input_notification)
def notify(external_id, massage):
    response = login(external_id)
    if response['ok'] and response['user'].permission == 'admin':
        send_message(external_id, "Что отправим этим плебеям?")
    else:
        send_message(external_id, "Эта команда для вас недоступна")

    return {"ok": True}
