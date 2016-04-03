class User:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.token = None
        self.token_expire = None

    def __eq__(self, other):
        return self.login == other.login and \
            self.password == other.password and \
            self.token == other.token and \
            self.token_expire == other.token_expire