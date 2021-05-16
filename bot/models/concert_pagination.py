from bot.models.concert import Concert


class ConcertPagination:
    def __init__(self):
        self.concerts = []
        self.index = 0
        self.massage_id = {}

    def set(self, concerts: [], chat_id, massage_id):
        self.concerts.clear()
        for c in concerts:
            self.concerts.append(Concert(c))
        self.index = 0
        self.massage_id[chat_id] = massage_id

    def current(self):
        if len(self.concerts) > 0:
            return self.concerts[self.index]
        return None

    def next(self):
        if len(self.concerts) > 0:
            self.index += 1
            self.index %= len(self.concerts)
            return self.concerts[self.index]
        return None

    def prev(self):
        if len(self.concerts) > 0:
            self.index -= 1
            self.index %= len(self.concerts)
            return self.concerts[self.index]
        return None
