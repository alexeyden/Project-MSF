import os
import json

from .role import Role
from .exceptions import ConfigError


class RoleAccess:
    def __init__(self, storage, config_path):
        self.config_path = config_path
        self.storage = storage
        self.roles = dict()
        self.reload()

    def __del__(self):
        pass

    def reload(self):
        self.roles = dict()

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

        for path, users in config.items():
            # TODO: check if path and user exists

            self.roles[path] = Role(path, set(users))

    def by_owner(self, user):
        return [
            role for path, role in self.roles.items()
            if path.startswith('/{0}/'.format(user))
        ]

    def by_path(self, path):
        role = self.roles.get(path, None)

        if role is not None:
            return role

        for role_path, role in self.roles.items():
            if role_path.endswith('/'):
                if path.startswith(role_path) or role_path.startswith(path):
                    return role
            else:
                if role_path.startswith(path):
                    return role

        return None

    def create(self, role):
        raise NotImplementedError()

    def save(self, role):
        raise NotImplementedError()

    def remove(self, role):
        raise NotImplementedError()