from flask import request
from random import randint

from dialog.dialog_bot import DialogBot
from dialog.registration_dialog import register_dialog
from updater import Updater
from markup import get_start_markup
from tg_massage_methods import send_message
from bot import app
from bot.db_handlers.message_handler import Handler
from server_models.concert_pagination import ConcertPagination
from server_models.ticket_pagination import TicketPagination

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








# def re_register():
#     external_id = request.json["callback_query"]["from"]["id"]
#     app.logger.debug('re_register')
#     updater.intercept_routing(external_id, process_register_dialog)
#     process_register_dialog()
#     return {"ok": True}







# if __name__ == '__main__':
#     app.run(debug=True)
