class Updater:
    def __init__(self, handlers: []):
        self.handlers = handlers
        self.interceptors = {}

    def intercept_routing(self, user_id, interceptor):
        self.interceptors[user_id] = interceptor

    def free_routing(self, user_id):
        del self.interceptors[user_id]

    async def update(self, user_id, *args, **kwargs) -> bool:
        is_invoked = False

        if user_id in self.interceptors:
            to_free_routing = self.interceptors[user_id](user_id, *args, **kwargs)
            if to_free_routing:
                self.free_routing(user_id)
            is_invoked = True
        else:
            for h in self.handlers:
                response = await h(user_id, *args, **kwargs)
                if not is_invoked and response['is_invoked']:
                    is_invoked = True

        return is_invoked
