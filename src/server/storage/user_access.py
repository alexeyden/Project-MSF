import os
import json

from .user import User
from .exceptions import ConfigError


class UserAccess:
    def __init__(self, storage, config_path):
        self.config_path = config_path
        self.storage = storage
        self.users = dict()
        self.reload()

    def reload(self):
        self.users = dict()

        if not os.path.exists(self.config_path):
            raise ConfigError(
                'Config file not found: {0}'.format(self.config_path),
                self.config_path)

        with open(self.config_path, 'r') as file:
            try:
                config = json.load(file)
            except json.JSONDecodeError as error:
                raise ConfigError('Invalid JSON', self.config_path) from error

        # TODO: check if config is valid

        for login, info in config.items():
            user = User(login=login, password=info.get('password'))

            # TODO: read & validate tokens

            self.users[login] = user

    def by_login(self, login):
        return self.users.get(login, None)

    def create(self, user):
        raise NotImplementedError()

    def change_password(self, user, new_password):
        raise NotImplementedError()

    def remove(self, user):
        raise NotImplementedError()