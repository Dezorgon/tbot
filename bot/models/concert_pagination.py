from bot.models.concert import Concert


class ConcertPagination:
    def __init__(self):
        self.concerts = []
        self.index = 0

    def set(self, concerts: []):
        for c in concerts:
            self.concerts.append(Concert(c))
        self.index = 0

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
