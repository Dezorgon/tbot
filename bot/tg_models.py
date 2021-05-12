import json


class Markup:
    def to_json(self):
        pass


class Message:
    def __init__(self, chat_id, text, parse_mode=None, disable_notification=None,
                 reply_to_message_id=None, reply_markup: Markup = None):
        self.chat_id = chat_id
        self.text = text
        self.parse_mode = parse_mode
        self.disable_notification = disable_notification
        self.reply_to_message_id = reply_to_message_id
        self.reply_markup: Markup = reply_markup

    def to_json(self):
        d = {k: v for k, v in self.__dict__.items() if v is not None}
        if 'reply_markup' in d:
            d['reply_markup'] = json.dumps(d['reply_markup'].to_json())
        return d


class KeyboardButton:
    def __init__(self, text: str, request_contact: bool = None):
        self.text = text
        self.request_contact = request_contact

    def to_json(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}


class ReplyKeyboardMarkup(Markup):
    def __init__(self, keyboard: [[KeyboardButton]], resize_keyboard: bool = True, one_time_keyboard: bool = True):
        self.keyboard: [[KeyboardButton]] = keyboard
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard

    def to_json(self):
        d = {k: v for k, v in self.__dict__.items() if v is not None}
        for row in d['keyboard']:
            for i in range(len(row)):
                row[i] = row[i].to_json()
        return d


# b1 = KeyboardButton('1')
# b2 = KeyboardButton('2')
# rkm = ReplyKeyboardMarkup([[b1], [b2]])
# m = Message(1, 'fds', reply_markup=rkm)
# print(m.to_json())
