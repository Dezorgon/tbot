class Ticket:
    def __init__(self, d):
        self.id = d['id']
        self.concert_id = d['concert_id']
        self.count = d['count']
        self.price = d['price']
        self.type = d['type']
        self.left = d['left']

    def __str__(self):
        s = f"{self.type}\n{self.price}р {self.left}шт"
        return s
