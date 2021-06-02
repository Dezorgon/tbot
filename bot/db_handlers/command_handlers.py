from random import randint

from bot.db_handlers.login_handlers import login, register
from bot.markup import get_start_markup
from bot.tg_massage_methods import send_message
from bot import handler


not_handled_answers = ['У меня вообще-то команды есть', 'Что с тобой не так?',
                       'Чел ты', 'Мне кажется тебе не нужны билеты']


@handler.message_handler(commands=['/start'])
async def process_start_command(external_id, massage):
    if not (await login(external_id))['ok']:
        await register(external_id, massage)
    else:
        await process_help_command(external_id, massage)
    return {"ok": True}


@handler.message_handler(commands=['/help'])
async def process_help_command(external_id, massage):
    send_message(external_id, "Привет")
    send_message(external_id, "Здесь ты можешь купить билеты",
                 get_start_markup((await login(external_id))['ok']))
    return {"ok": True}


@handler.message_handler(not_handled_func=True)
async def not_handled(external_id, massage):
    text = not_handled_answers[randint(0, len(not_handled_answers) - 1)]
    send_message(external_id, text, get_start_markup(True))
