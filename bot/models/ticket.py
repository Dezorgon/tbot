class Ticket:
    def __init__(self, d):
        self.id = d['id']
        self.concert_id = d['concert_id']
        self.count = d['count']
        self.price = d['price']
        self.type = d['type']

    def __str__(self):
        s = f"{self.id} {self.id} {self.concert_id}\n{self.price}р {self.count}шт"
        return s
