from flask import Flask

from bot.dialog.dialog_bot import DialogBot
from bot.dialog.registration_dialog import register_dialog
from bot.message_handler import Handler
from bot.server_models.concert_pagination import ConcertPagination
from bot.server_models.ticket_pagination import TicketPagination
from bot.updater import Updater

app = Flask(__name__)
app.config.from_pyfile('config.py')

handler = Handler()
updater = Updater([handler.send_message])
dialog = DialogBot(register_dialog)
concert_pagination = ConcertPagination()
ticket_pagination = TicketPagination()

not_handled_answers = ['У меня вообще-то команды есть', 'Что с тобой не так?',
                       'Чел ты', 'Мне кажется тебе не нужны билеты']