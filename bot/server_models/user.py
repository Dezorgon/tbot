class User:
    def __init__(self, user_id, extern_id, first_name, last_name, date, permission):
        self.id = user_id
        self.external_id = extern_id
        self.first_name = first_name
        self.last_name = last_name
        self.date = date
        self.permission = permission

    def __str__(self):
        s = f"{self.first_name} {self.last_name} {self.date}"
        return s
