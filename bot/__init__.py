from flask import Flask
import logging

from bot.dialog.dialog_bot import DialogBot
from bot.dialog.registration_dialog import register_dialog
from bot.message_handler import Handler
from bot.server_models.concert_pagination import ConcertPagination
from bot.server_models.ticket_pagination import TicketPagination
from bot.updater import Updater


def create_app(config):
    app = Flask(__name__)
    app.config.from_pyfile(config)
    logging.basicConfig(level=getattr(logging, app.config['LOGGING_LEVEL']),
                        format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    return app


app = create_app('config.py')
token = app.config['TOKEN']

handler = Handler()
updater = Updater([handler.send_message])
dialog = DialogBot(register_dialog)
concert_pagination = ConcertPagination()
ticket_pagination = TicketPagination()
