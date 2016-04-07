#!/usr/bin/env python3
import unittest

from server.storage.role_access import RoleAccess
from server.storage.role import Role
from server.storage.exceptions import ConfigError


class TestRoleAccess(unittest.TestCase):
    roles = [
        Role(path='/user1/A/B/', users={'user2'}),
        Role(path='/user1/B/', users={'user2', 'user3'}),
        Role(path='/user2/A/B', users={'user1'}),
        Role(path='/user2/A/B', users={'user1'})
    ]

    def test_query(self):
        roles = RoleAccess(storage=None, config_path='data/roles_1.json')

        user1_own = roles.by_owner("user1")
        user2_own = roles.by_owner("user2")
        user3_own = roles.by_owner("user3")

        self.assertSetEqual(set(user1_own), set(self.roles[:2]))
        self.assertSetEqual(set(user2_own), set(self.roles[2:]))
        self.assertSetEqual(set(user3_own), set())

    def test_errors(self):
        with self.assertRaises(ConfigError):
            RoleAccess(None, 'data/not_existing.json')
        with self.assertRaises(ConfigError):
            RoleAccess(None, 'data/roles_wrong.json')

    def test_prefixes(self):
        roles = RoleAccess(storage=None, config_path='data/roles_1.json')
        role1 = roles.by_path("/user1/A/B/")
        role1_1 = roles.by_path("/user1/A/B/C/D")

        self.assertEqual(role1, self.roles[0])
        self.assertEqual(role1_1, self.roles[0])

        role2 = roles.by_path('/user2/A/B')
        self.assertEqual(role2, self.roles[2])
        role2_1 = roles.by_path('/user2/A/')
        self.assertEqual(role2_1, self.roles[3])

if __name__ == '__main__':
    unittest.main()