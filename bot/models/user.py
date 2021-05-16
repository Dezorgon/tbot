class User:
    def __init__(self):
        self.id = 0
        self.external_id = 0
        self.first_name = ''
        self.last_name = ''
        self.date = ''
        self.permission = ''
        self.is_authenticated = False

    def set(self, user_id, extern_id, first_name, last_name, date, permission):
        self.id = user_id
        self.external_id = extern_id
        self.first_name = first_name
        self.last_name = last_name
        self.date = date
        self.permission = permission
        self.is_authenticated = True

    def __str__(self):
        s = f"{self.first_name} {self.last_name} {self.date}"
        return s
