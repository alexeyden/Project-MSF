#!/usr/bin/env python3
import unittest
import asyncio
import json

from server.storage.user import User
from server.storage.user_access import UserAccess
from server.storage.exceptions import ConfigError


class TestUserAccess(unittest.TestCase):
    def test_query(self):
        users = UserAccess(storage=None, config_path='data/users_1.json')

        loop = asyncio.get_event_loop()

        u1 = (loop.run_until_complete(users.by_login("user1")), User(login="user1", password="123"))
        u2 = (loop.run_until_complete(users.by_login("user2")), User(login="user2", password="456"))

        for uc,ut in [u1, u2]:
            self.assertEqual(uc, ut)

    def test_errors(self):
        with self.assertRaises(ConfigError):
            UserAccess(None, 'data/not_existing.json')
        with self.assertRaises(ConfigError):
            UserAccess(None, 'data/users_wrong.json')

if __name__ == '__main__':
    unittest.main()