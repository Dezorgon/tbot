from flask import request

from bot import app


functions = {'message': [], 'regex': [], 'commands': [], "callback": []}


def message_handler(message: [str] = None, regex=None, commands: [str] = None, callback: [str] = None):
    def decorator(func):

        if message:
            for m in message:
                functions['message'].append({m: func})
        if regex:
            functions['message'].append({regex: func})
        if commands:
            for c in commands:
                functions['commands'].append({c: func})
        if callback:
            for c in callback:
                functions['callback'].append({c: func})

        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return decorator


@app.route('/', methods=["GET", "POST"])
def send_message():
    app.logger.debug(request.json)
    if "message" in request.json:
        msg = request.json["message"]["text"]
        for d in functions['commands']:
            if msg in d:
                d[msg]()
        for d in functions['message']:
            if msg in d:
                d[msg]()
    if "callback_query" in request.json:
        data = request.json["message"]["data"]
        for d in functions['message']:
            if data in d:
                d[data]()
    return {"ok": True}
