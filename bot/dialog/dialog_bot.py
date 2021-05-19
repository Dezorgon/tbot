import collections

from bot.tg_massage_methods import send_message


class DialogBot(object):
    def __init__(self, generator):
        self.handlers = collections.defaultdict(generator)

    def handle_message(self, chat_id, input_text, restart=False):
        if restart:
            self.handlers.pop(chat_id, None)
        if chat_id in self.handlers:
            try:
                answer = self.handlers[chat_id].send(input_text)
            except StopIteration as e:
                del self.handlers[chat_id]
                if e.value:
                    send_message(chat_id=chat_id, text=e.value[0], reply_markup=e.value[1])
                return True
        else:
            answer = next(self.handlers[chat_id])

        reply_markup = None
        text = answer
        if not isinstance(answer, str):
            text = answer[0]
            reply_markup = answer[1]

        send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        return False
