#!/usr/bin/env python3
import unittest
import shutil
import os

from server.storage.storage import *
from server.storage.exceptions import *


class TestStorage(unittest.TestCase):
    STORAGE = 'storage/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._clean_storage()
        self.storage = Storage(storage_path=self.STORAGE)

        os.mkdir(os.path.join(self.STORAGE, 'user1/A'))
        os.mkdir(os.path.join(self.STORAGE, 'user1/A/B'))
        os.mkdir(os.path.join(self.STORAGE, 'user1/B'))
        shutil.copy('data/algorithm.json', os.path.join(self.STORAGE, 'user1/A/Alg1'))

    def test_init(self):
        self.assertEqual(os.path.exists(os.path.join(self.STORAGE, 'user1')), True)
        self.assertEqual(os.path.exists(os.path.join(self.STORAGE, 'user2')), True)
        self.assertEqual(os.path.exists(os.path.join(self.STORAGE, 'user3')), True)

    def test_valid(self):
        self.assertEqual(self.storage.valid('invalid/'), False)
        self.assertEqual(self.storage.valid('/invalid/\\'), False)
        self.assertEqual(self.storage.valid('/юникод!123(3)[]    !'), True)
        self.assertEqual(self.storage.valid('/invalid/????'), False)
        self.assertEqual(self.storage.valid('/'), True)

    def test_owner(self):
        with self.assertRaises(InvalidPathError):
            self.storage.owner('\/invalid\/')
        with self.assertRaises(NoSuchPathError):
            self.storage.owner('/user1/C')
        with self.assertRaises(NoSuchPathError):
            self.storage.owner('/user4/')
        with self.assertRaises(NoSuchPathError):
            self.storage.owner('/user')

        self.assertEqual(self.storage.owner('/user1').login, 'user1')
        self.assertEqual(self.storage.owner('/user2/').login, 'user2')
        self.assertEqual(self.storage.owner('/user3/').login, 'user3')

    def test_list(self):
        with self.assertRaises(InvalidPathError):
            self.storage.list('%%invalid', context=None)
        with self.assertRaises(NoSuchPathError):
            self.storage.list('/user4/', context=None)

        items = sorted([item.path for item in self.storage.list('/', context=None)])

        self.assertEqual(len(items), 3)
        self.assertEqual(items[0], '/user1')
        self.assertEqual(items[1], '/user2')
        self.assertEqual(items[2], '/user3')

        context = Storage.StorageContext('user1')
        items = sorted([item.path for item in self.storage.list('/', context)])

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0], '/user1')
        self.assertEqual(items[1], '/user2')

    def test_exists(self):
        self.assertEqual(self.storage.exists('/'), True)
        self.assertEqual(self.storage.exists('/user1'), True)
        self.assertEqual(self.storage.exists('/user1/'), True)
        self.assertEqual(self.storage.exists('/user2'), True)
        self.assertEqual(self.storage.exists('/user3'), True)

    def _clean_storage(self):
        for p in os.listdir(self.STORAGE):
            if os.path.isdir(os.path.join(self.STORAGE, p)):
                shutil.rmtree(os.path.join(self.STORAGE, p))

if __name__ == '__main__':
    unittest.main()