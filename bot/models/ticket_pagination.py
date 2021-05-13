from bot.models.ticket import Ticket


class TicketPagination:
    def __init__(self):
        self.tickets = []
        self.index = 0

    def set(self, concerts: []):
        for c in concerts:
            self.tickets.append(Ticket(c))
        self.index = 0

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
