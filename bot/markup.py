from bot.telegram_models.tg_models import InlineKeyboardButton
from bot.telegram_models.tg_models import InlineKeyboardMarkup
from bot.telegram_models.tg_models import KeyboardButton
from bot.telegram_models.tg_models import ReplyKeyboardMarkup

b1 = InlineKeyboardButton('<', callback_data='previous_concert')
b2 = InlineKeyboardButton('>', callback_data='next_concert')
b3 = InlineKeyboardButton('Купить билет', callback_data='buy')
concert_markup = InlineKeyboardMarkup([[b1, b2], [b3]])

b1 = InlineKeyboardButton('<', callback_data='previous_ticket')
b2 = InlineKeyboardButton('>', callback_data='next_ticket')
b3 = InlineKeyboardButton('Купить', callback_data='buy_ticket')
ticket_markup = InlineKeyboardMarkup([[b1, b2], [b3]])


def get_start_markup(is_authenticated=False):
    b1 = KeyboardButton('Посмотреть концерты в моем городе')
    b2 = KeyboardButton('Ближайшие концерты')
    btns = [[b1], [b2]]
    if not is_authenticated:
        b3 = KeyboardButton('Регистрация')
        btns.append([b3])
    else:
        b3 = KeyboardButton('Профиль')
        btns.append([b3])
    markup = ReplyKeyboardMarkup(btns)
    return markup
