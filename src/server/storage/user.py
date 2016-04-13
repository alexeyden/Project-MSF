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

    def __str__(self):
        return 'User (login={0}, password={1}, token={2}, token_expire={3})' \
            .format(self.login, self.password, self.token, self.token_expire)

    def to_dict(self):
        return {
            'password': self.password
        }