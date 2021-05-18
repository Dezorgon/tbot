import collections
import requests

from bot import updater
from bot.telegram_models.tg_models import Message

token = '1801411028:AAE0FzT5Ntxm0o2jMNACLcKXMlaOkz0r5nU'
url = f"https://api.telegram.org/bot{token}/"


class DialogBot(object):
    def __init__(self, generator, updater: updater):
        self.handlers = collections.defaultdict(generator)
        self.updater = updater
        self.input_data = collections.defaultdict(list)

    def handle_message(self, chat_id, input_text, restart=False):
        if restart:
            self.handlers.pop(chat_id, None)
        if chat_id in self.handlers:
            try:
                answer = self.handlers[chat_id].send(input_text)
            except StopIteration as e:
                del self.handlers[chat_id]
                self.updater.free_routing(chat_id)
                if e.value:
                    send_message(chat_id=chat_id, text=e.value[0], reply_markup=e.value[1])
                return
        else:
            answer = next(self.handlers[chat_id])

        reply_markup = None
        text = answer
        if not isinstance(answer, str):
            text = answer[0]
            reply_markup = answer[1]
            if len(answer) > 2 and answer[2]:
                self.input_data[chat_id].append(input_text)

        send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


def send_message(chat_id, text, reply_markup=None):
    method = "sendMessage"
    m = Message(chat_id, text, reply_markup=reply_markup)
    data = m.to_json()
    requests.post(url + method, data=data)
