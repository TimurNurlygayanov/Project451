from app.api.helper import hash_password


class User(object):
    def __init__(self, username, password, role):
        self.username = username
        self.pass_hash = hash_password(password)
        self.role = role

    def verify_password(self, password):
        return hash_password(password) == self.pass_hash
