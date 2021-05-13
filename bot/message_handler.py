from typing import Callable
from flask import request

from bot import app


class Handler:
    functions = {'message': [], 'regex': [], 'command': [], "callback": []}
    next_functions = {}
    next_function = None

    def message_handler(self, message: [str] = None, regex=None, commands: [str] = None,
                        callback: [str] = None, next_func=None):
        def decorator(func):

            if next_func:
                self.next_functions[func] = next_func
            if message:
                for m in message:
                    self.functions['message'].append({m: func})
            if regex:
                self.functions['message'].append({regex: func})
            if commands:
                for c in commands:
                    self.functions['command'].append({c: func})
            if callback:
                for c in callback:
                    self.functions['callback'].append({c: func})

            def wrapper(*args, **kwargs):
                func(*args, **kwargs)

            return wrapper

        return decorator

    def send_message(self):
        app.logger.debug(request.json)
        func_to_invoke = None
        if self.next_function:
            func_to_invoke = self.next_function
            self.next_function = None
        else:
            if "message" in request.json:
                msg = request.json["message"]["text"]
                func_to_invoke = self.find_function(msg, 'command')
                if func_to_invoke is None:
                    func_to_invoke = self.find_function(msg, 'message')

            if "callback_query" in request.json:
                callback = request.json["callback_query"]["data"]
                func_to_invoke = self.find_function(callback, 'callback')

        if func_to_invoke:
            func_to_invoke()

        return {"ok": True}

    def find_function(self, route, type_of_route):
        for d in self.functions[type_of_route]:
            if route in d:
                func = d[route]
                if func in self.next_functions:
                    self.next_function = self.next_functions[func]
                return func
        return None
