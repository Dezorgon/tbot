from bot.models.ticket import Ticket


class TicketPagination:
    def __init__(self):
        self.tickets = []
        self.index = 0
        self.massage_id = {}

    def set(self, concerts: [], chat_id, massage_id):
        self.tickets.clear()
        for c in concerts:
            self.tickets.append(Ticket(c))
        self.index = 0
        self.massage_id[chat_id] = massage_id

    def current(self):
        if len(self.tickets) > 0:
            return self.tickets[self.index]
        return None

    def next(self):
        if len(self.tickets) > 0:
            self.index += 1
            self.index %= len(self.tickets)
            return self.tickets[self.index]
        return None

    def prev(self):
        if len(self.tickets) > 0:
            self.index -= 1
            self.index %= len(self.tickets)
            return self.tickets[self.index]
        return None
