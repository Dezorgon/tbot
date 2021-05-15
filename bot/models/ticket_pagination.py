from bot.models.ticket import Ticket
from bot.tg_massage_methods import delete_message


class TicketPagination:
    def __init__(self):
        self.tickets = []
        self.index = 0
        self.massage_id = {}

    def set(self, concerts: [], chat_id, massage_id):
        if chat_id in self.massage_id:
            delete_message(chat_id, self.massage_id[chat_id])

        self.tickets.clear()
        for c in concerts:
            self.tickets.append(Ticket(c))
        self.index = 0
        self.massage_id[chat_id] = massage_id

    def current(self):
        return self.tickets[self.index]

    def next(self):
        self.index += 1
        self.index %= len(self.tickets)
        return self.tickets[self.index]

    def prev(self):
        self.index -= 1
        self.index %= len(self.tickets)
        return self.tickets[self.index]
