from bot.db_handlers.login_handlers import login, register
from bot.markup import get_start_markup
from bot.tg_massage_methods import send_message
from bot import handler


@handler.message_handler(commands=['/start'])
def process_start_command(external_id, massage):
    if not login(external_id)['ok']:
        register(external_id, massage)
    else:
        process_help_command(external_id, massage)
    return {"ok": True}


@handler.message_handler(commands=['/help'])
def process_help_command(external_id, massage):
    send_message(external_id, "Здесь ты можешь купить билеты", get_start_markup(login(external_id)['ok']))
    return {"ok": True}
