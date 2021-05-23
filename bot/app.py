from random import randint

from bot.db_handlers.command_handlers import *
from bot.db_handlers.concert_handlers import *
from bot.db_handlers.login_handlers import *
from bot.db_handlers.ticket_handlers import *
from bot.db_handlers.admin_handlers import *


not_handled_answers = ['У меня вообще-то команды есть', 'Что с тобой не так?',
                       'Чел ты', 'Мне кажется тебе не нужны билеты']


@app.route('/', methods=["GET", "POST"])
def main():
    app.logger.debug(request.json)

    if 'callback_query' in request.json:
        external_id = request.json["callback_query"]["from"]["id"]
        message = request.json["callback_query"]["message"]
    elif 'message' in request.json:
        external_id = request.json["message"]["from"]["id"]
        if 'text' in request.json['message']:
            message = request.json["message"]
        elif 'photo' in request.json["message"]:
            external_id = request.json["message"]["from"]["id"]
            send_message(external_id, 'Давай без каринок', get_start_markup(True))
            return {'ok': True}
        else:
            send_message(external_id, 'Это еще что такое?', get_start_markup(True))
            return {'ok': True}
    else:
        return {'ok': True}

    is_handled = updater.update(external_id, message)

    if not is_handled:
        app.logger.debug('not_handled')
        text = not_handled_answers[randint(0, len(not_handled_answers)-1)]
        send_message(external_id, text, get_start_markup(True))

    return {'ok': True}
