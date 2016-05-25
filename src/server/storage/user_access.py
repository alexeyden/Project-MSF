import os
import json
import hashlib
import time
import random

from .user import User
from .exceptions import ConfigError


class UserAccess:
    def __init__(self, storage, config_path):
        self.config_path = config_path
        self.storage = storage
        self.users = dict()
        self._token_map = dict()
        self.reload()

    def reload(self):
        self.users = dict()

        if not os.path.exists(self.config_path):
            raise ConfigError(
                'Config file not found: {0}'.format(self.config_path),
                self.config_path)

        with open(self.config_path, 'r', encoding='utf-8') as file:
            try:
                config = json.load(file)
            except json.JSONDecodeError as error:
                raise ConfigError('Invalid JSON', self.config_path) from error

        # TODO: check if config is valid

        for login, info in config.items():
            user = User(login=login, password=info.get('password'))

            # TODO: read & validate tokens

            self.users[login] = user

    def all(self):
        return self.users.values()

    def auth(self, login, password):
        if login not in self.users:
            return None

        hash_ = self._hash_password(password)

        user = self.users.get(login)

        if user.password != hash_:
            return None

        # TODO: proper token generation

        token = login + str(time.time()) + str(random.uniform(0, 1))
        token_hash = hashlib.md5(token.encode('utf-8')).hexdigest()

        user.token = token_hash
        user.token_expire = time.time() + 6 * 60 * 60

        self._update_token_map()

        return token_hash

    def by_login(self, login):
        return self.users.get(login, None)

    def by_token(self, token):
        return self._token_map.get(token, None)

    def create(self, login, password):
        if login in self.users:
            return False

        self.users[login] = User(login=login, password=password)
        self._save_config()

        return True

    def change_password(self, login, new_password):
        if login not in self.users:
            return False

        self.users[login].password = self._hash_password(new_password)
        self._save_config()

        return True

    def remove(self, login):
        if login not in self.users:
            return False

        self.users.pop(login)
        self._update_token_map()
        self._save_config()

        return True

    def _update_token_map(self):
        self._token_map.clear()

        for user in self.users.values():
            if user.token:
                self._token_map[user.token] = user

    def _hash_password(self, password):
        return hashlib.md5(password.encode('utf-8')).hexdigest()

    def _save_config(self):
        with open(self.config_path, 'w') as f:
            text = json.dumps({login: user.to_dict() for login,user in self.users.items()}, indent=True)
            f.write(text)
