import asyncio

from bot.db_handlers.command_handlers import *
from bot.db_handlers.concert_handlers import *
from bot.db_handlers.login_handlers import *
from bot.db_handlers.ticket_handlers import *
from bot.db_handlers.admin_handlers import *

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def handlers_loop(_request):
    app.logger.debug(_request.json)

    if 'callback_query' in _request.json:
        external_id = _request.json["callback_query"]["from"]["id"]
        message = _request.json["callback_query"]["message"]
    elif 'message' in _request.json:
        external_id = _request.json["message"]["from"]["id"]
        if 'text' in _request.json['message']:
            message = _request.json["message"]
        elif 'photo' in _request.json["message"]:
            external_id = _request.json["message"]["from"]["id"]
            send_message(external_id, 'Давай без каринок', get_start_markup(True))
            return {'ok': True}
        else:
            send_message(external_id, 'Это еще что такое?', get_start_markup(True))
            return {'ok': True}
    else:
        return {'ok': True}

    is_handled = await updater.update(external_id, message)


@app.route('/', methods=["GET", "POST"])
def main():
    loop.run_until_complete(handlers_loop(request))
    return {'ok': True}


@app.route('/test', methods=["GET", "POST"])
def test():
    send_message(435535768, 'test')

    return {'ok': True}
