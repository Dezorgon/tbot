from bot.server_models.concert import Concert


class ConcertPagination:
    def __init__(self):
        self.concerts = []
        self.index = {}
        self.massage_id = {}

    def set(self, concerts: [], chat_id, massage_id):
        self.concerts.clear()
        for c in concerts:
            self.concerts.append(Concert(c))
        self.index[chat_id] = 0
        self.massage_id[chat_id] = massage_id

    def current(self, chat_id):
        if len(self.concerts) > 0:
            return self.concerts[self.index[chat_id]]
        return None

    def next(self, chat_id):
        if len(self.concerts) > 0:
            self.index[chat_id] += 1
            self.index[chat_id] %= len(self.concerts)
            return self.concerts[self.index[chat_id]]
        return None

    def prev(self, chat_id):
        if len(self.concerts) > 0:
            self.index[chat_id] -= 1
            self.index[chat_id] %= len(self.concerts)
            return self.concerts[self.index[chat_id]]
        return None
