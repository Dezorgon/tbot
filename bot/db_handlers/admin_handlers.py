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

    massages = []
    for i in indices:
        ret = send_message(i, text)
        massages.append(ret)

    return {"ok": True, "massages": massages}


@handler.message_handler(commands=['/notify'], next_func=input_notification)
async def notify(external_id, massage):
    response = await login(external_id)
    if response['ok'] and response['user'].permission == 'admin':
        massage = send_message(external_id, "Что отправим этим плебеям?")
    else:
        massage = send_message(external_id, "Эта команда для вас недоступна")

    return {"ok": True, "massage": massage}
