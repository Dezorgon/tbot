from flask_login import UserMixin


class User:
    def __init__(self):
        self.first_name = ''
        self.last_name = ''
        self.date = ''
        self.is_authenticated = False

    def set(self, first_name, last_name, date):
        self.first_name = first_name
        self.last_name = last_name
        self.date = date
        self.is_authenticated = True

    def __str__(self):
        s = f"{self.first_name} {self.last_name} {self.date}"
        return s
