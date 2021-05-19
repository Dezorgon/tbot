from random import randint


from db_handlers.command_handlers import *
from db_handlers.concert_handlers import *
from db_handlers.login_handlers import *
from db_handlers.ticket_handlers import *


not_handled_answers = ['У меня вообще-то команды есть', 'Что с тобой не так?',
                       'Чел ты', 'Мне кажется тебе не нужны билеты']


@app.route('/', methods=["GET", "POST"])
def main():
    app.logger.debug(request.json)

    if 'callback_query' in request.json:
        external_id = request.json["callback_query"]["from"]["id"]
        message = request.json["callback_query"]["message"]
    else:
        external_id = request.json["message"]["from"]["id"]
        message = request.json["message"]

    is_handled = updater.update(external_id, message)

    if not is_handled:
        app.logger.debug('not_handled')
        text = not_handled_answers[randint(0, len(not_handled_answers)-1)]
        send_message(external_id, text, get_start_markup(True))

    return {'ok': True}
