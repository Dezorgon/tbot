from bot.server_models.ticket import Ticket


class TicketPagination:
    def __init__(self):
        self.tickets = []
        self.index = {}
        self.massage_id = {}

    def set(self, concerts: [], chat_id, massage_id):
        self.tickets.clear()
        for c in concerts:
            self.tickets.append(Ticket(c))
        self.index[chat_id] = 0
        self.massage_id[chat_id] = massage_id

    def current(self, chat_id):
        if len(self.tickets) > 0:
            return self.tickets[self.index[chat_id]]
        return None

    def next(self, chat_id):
        if len(self.tickets) > 0:
            self.index[chat_id] += 1
            self.index[chat_id] %= len(self.tickets)
            return self.tickets[self.index[chat_id]]
        return None

    def prev(self, chat_id):
        if len(self.tickets) > 0:
            self.index[chat_id] -= 1
            self.index[chat_id] %= len(self.tickets)
            return self.tickets[self.index[chat_id]]
        return None
