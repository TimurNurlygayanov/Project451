class User(object):
    def __init__(self, id, username, role, token):
        self.id = id
        self.username = username
        self.role = role
        self.token = token


class LoggedUser(object):
    def __init__(self, username, role):
        self.username = username
        self.role = role
        self.logged = True
