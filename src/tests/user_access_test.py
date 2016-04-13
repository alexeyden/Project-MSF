#!/usr/bin/env python3
import unittest

from storage.user import User
from storage.user_access import UserAccess
from storage.exceptions import ConfigError


class TestUserAccess(unittest.TestCase):
    def test_auth(self):
        users = UserAccess(storage=None, config_path='data/users_1.json')
        self.assertIsNotNone(users.auth('user1', '123'))
        self.assertIsNotNone(users.auth('user2', '456'))
        self.assertIsNone(users.auth('user1', 'invalid'))
        self.assertIsNone(users.auth('user100', 'invalid'))

    def test_query(self):
        users = UserAccess(storage=None, config_path='data/users_1.json')

        u1 = (users.by_login("user1"), User(login="user1", password="202cb962ac59075b964b07152d234b70"))
        u2 = (users.by_login("user2"), User(login="user2", password="250cf8b51c773f3f8dc8b4be867a9a02"))

        for uc,ut in [u1, u2]:
            self.assertEqual(uc, ut)

    def test_errors(self):
        with self.assertRaises(ConfigError):
            UserAccess(None, 'data/not_existing.json')
        with self.assertRaises(ConfigError):
            UserAccess(None, 'data/users_wrong.json')

    def test_create_remove(self):
        users = UserAccess(storage=None, config_path='data/users_1.json')
        self.assertEqual(users.create('test', 'test'), True)
        self.assertEqual('test' in  users.users, True)
        self.assertEqual(users.change_password('test', 'test2'), True)
        self.assertEqual(users.users['test'].password, users._hash_password('test2'))
        self.assertEqual(users.remove('test'), True)
        self.assertEqual('test' in users.users, False)

if __name__ == '__main__':
    unittest.main()