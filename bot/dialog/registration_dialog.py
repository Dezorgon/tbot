from datetime import datetime

from bot.markup import get_start_markup
from bot.telegram_models.tg_models import KeyboardButton, ReplyKeyboardMarkup,\
    InlineKeyboardButton, InlineKeyboardMarkup


def register_dialog():
    if_register = yield from ask_yes_or_no("Привет! Смотрю ты новенький\nXочешь оставаить мне свои данные?")

    if if_register:
        first_name = yield "Начнем с имени", None, True
        last_name = yield "Фамилия?", None, True
        date = yield "Ну и укажи мне дату своего рождения в формате: день.месяц.год (1.01.2000)", None, True
        is_valid_date = False
        while not is_valid_date:
            try:
                datetime.strptime(date, "%d.%m.%Y")
                is_valid_date = True
            except ValueError:
                is_valid_date = False
                b1 = KeyboardButton('Перехотелось')
                markup = ReplyKeyboardMarkup([[b1]])
                answer = yield "Введи дату нормально", markup
                if answer == "Перехотелось":
                    return "Ну и ладно(", get_start_markup(False)
                else:
                    date = answer

        b2 = InlineKeyboardButton('Норм', callback_data='accept_register_data')
        b1 = InlineKeyboardButton('Давай по новой Миша', callback_data='re_register')
        markup = InlineKeyboardMarkup([[b1], [b2]])
        text = f'{first_name} {last_name} {date}'
        return text, markup

    return "Что тогда делаем?", get_start_markup(False)


def ask_yes_or_no(question):
    b1 = KeyboardButton('Да')
    b2 = KeyboardButton('Нет')
    markup = ReplyKeyboardMarkup([[b1, b2]])
    answer = yield question, markup
    while not ("да" in answer.lower() or "нет" in answer.lower()):
        answer = yield "a?"
    return "да" in answer.lower()


# def input_registration_data():
#     first_name = yield "Начнем с имени", None, True
#     last_name = yield "Фамилия?", None, True
#     date = yield "Ну и укажи мне дату своего рождения в формате: день.месяц.год (1.01.2000)", None, True
#
#     b2 = InlineKeyboardButton('Норм', callback_data='accept_register_data')
#     b1 = InlineKeyboardButton('Давай по новой', callback_data='next_ticket')
#     markup = InlineKeyboardMarkup([[b1], [b2]])
#     text = f'{first_name} {last_name} {date}'
#     return text, markup
    # redirect(url_for('main'))
    # permission = 'user'
    # external_id = current_user.external_id

    # response = requests.post('http://127.0.0.1:81/signup',
    #                          json={'first_name': first_name, 'last_name': last_name,
    #                                'external_id': external_id, 'date': date,
    #                                'permission': permission})
    # response = response.json()
    #
    # if not response['ok']:
    #     send_message(external_id, "Что-то пошло не так")
    #     register(external_id)
    # else:
    #     login(external_id)

#
# def f():
#     a = yield 1
#     return 1, 2
#
#
# try:
#     g = f()
#     next(g)
#     print(g.send(1))
# except StopIteration as e:
#     print(e.value[0], e.value[1])
