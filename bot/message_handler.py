from flask import request


class Handler:
    functions = {'message': [], 'regex': [], 'command': [], 'callback': []}
    next_functions = {}
    next_function = {}
    not_handled_func = None

    def message_handler(self, message: [str] = None, regex=None, commands: [str] = None,
                        callback: [str] = None, not_handled_func: bool = False, next_func=None):
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
            if not_handled_func:
                self.not_handled_func = func

            def wrapper(*args, **kwargs):
                func(*args, **kwargs)

            return wrapper

        return decorator

    async def send_message(self, external_id, message):
        func_to_invoke = None
        if external_id in self.next_function:
            func_to_invoke = self.next_function[external_id]
            del self.next_function[external_id]
        else:
            if "message" in request.json:
                msg = request.json["message"]["text"]
                func_to_invoke = self.find_function(msg, 'command', external_id)
                if func_to_invoke is None:
                    func_to_invoke = self.find_function(msg, 'message', external_id)

            if "callback_query" in request.json:
                callback = request.json["callback_query"]["data"]
                func_to_invoke = self.find_function(callback, 'callback', external_id)

        if func_to_invoke:
            response = await func_to_invoke(external_id, message)
            return {"is_invoked": True, "response": response}
        else:
            await self.not_handled_func(external_id, message)

        return {"is_invoked": False}

    def find_function(self, route, type_of_route, external_id):
        for d in self.functions[type_of_route]:
            if route in d:
                func = d[route]
                if func in self.next_functions:
                    self.next_function[external_id] = self.next_functions[func]
                return func
        return None
