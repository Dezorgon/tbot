from bot.models.concert import Concert
from bot.tg_massage_methods import delete_message


class ConcertPagination:
    def __init__(self):
        self.concerts = []
        self.index = 0
        self.massage_id = {}

    def set(self, concerts: [], chat_id, massage_id):
        if chat_id in self.massage_id:
            delete_message(chat_id, self.massage_id[chat_id])

        self.concerts.clear()
        for c in concerts:
            self.concerts.append(Concert(c))
        self.index = 0
        self.massage_id[chat_id] = massage_id

    def current(self):
        return self.concerts[self.index]

    def next(self):
        self.index += 1
        self.index %= len(self.concerts)
        return self.concerts[self.index]

    def prev(self):
        self.index -= 1
        self.index %= len(self.concerts)
        return self.concerts[self.index]
