class Concert:
    def __init__(self, d):
        self.id = d['id']
        self.name = d['name']
        self.date = d['date']
        self.city = d['city']
        self.place = d['place']
        if 'description' in d:
            self.description = d['description']
        else:
            self.description = None

    def __str__(self):
        s = f"{self.name}\n\n{self.city} {self.place}\n{self.date}\n"
        if self.description:
            s += '\n'
            s += self.description
        return s
