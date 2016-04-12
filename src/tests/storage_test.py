#!/usr/bin/env python3
import unittest
import shutil
import os

from server.storage.storage import *
from server.storage.exceptions import *
from server.algorithm.type_spec import *
from server.algorithm.algorithm import *


class TestStorage(unittest.TestCase):
    STORAGE = 'storage/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._clean_storage()
        self.storage = Storage(storage_path=self.STORAGE)

        os.mkdir(os.path.join(self.STORAGE, 'user1/A'))
        os.mkdir(os.path.join(self.STORAGE, 'user1/A/B'))
        os.mkdir(os.path.join(self.STORAGE, 'user1/B'))
        os.mkdir(os.path.join(self.STORAGE, 'user2/A'))
        shutil.copy('data/algorithm.json', os.path.join(self.STORAGE, 'user2/A/Alg1'))

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
        self.assertListEqual(items, [
            '/user1',
            '/user2',
            '/user3'
        ])

        context = Storage.StorageContext('user1')

        items = sorted([item.path for item in self.storage.list('/', context)])
        self.assertListEqual(items, [
            '/user1',
            '/user2'
        ])

        items = sorted([item.path for item in self.storage.list('/user1/', context)])
        self.assertListEqual(items, [
            '/user1/A',
            '/user1/B'
        ])

        items = sorted([item.path for item in self.storage.list('/user1/A/', context)])
        self.assertListEqual(items, [
            '/user1/A/B'
        ])

        items = sorted([item.path for item in self.storage.list('/user2/A/', context)])
        self.assertListEqual(items, [
            '/user2/A/Alg1'
        ])

    def test_move(self):
        context = Storage.StorageContext('user1')

        loop = asyncio.get_event_loop()

        with self.assertRaises(InvalidPathError):
            loop.run_until_complete(self.storage.move('% invalid path %', '/user1/C', context))
        with self.assertRaises(InvalidPathError):
            loop.run_until_complete(self.storage.move('/user1/A', '% udsds %', context))

        with self.assertRaises(NoSuchPathError):
            loop.run_until_complete(self.storage.move('/user1/C/', '/user1/D', context))
        with self.assertRaises(InvalidPathError):
            loop.run_until_complete(self.storage.move('/user1/A/', '/user1/B', context))
        with self.assertRaises(InvalidPathError):
            loop.run_until_complete(self.storage.move('/user1/A/', '/', context))
        with self.assertRaises(InvalidPathError):
            loop.run_until_complete(self.storage.move('/user1/A/', '/user2/C/', context))
        with self.assertRaises(InvalidPathError):
            loop.run_until_complete(self.storage.move('/user2/A/', '/user1/C/', context))
        with self.assertRaises(InvalidPathError):
            loop.run_until_complete(self.storage.move('/', '/user2/C/', context))

        loop.run_until_complete(self.storage.move('/user1/A/', '/user1/B/C', context))
        self.assertEqual(self.storage.exists('/user1/A', context), False)
        self.assertEqual(self.storage.exists('/user1/B/C/', context), True)

        loop.run_until_complete(self.storage.move('/user1/B/C', '/user1/A', context))
        self.assertEqual(self.storage.exists('/user1/A', context), True)
        self.assertEqual(self.storage.exists('/user1/B/C/', context), False)

    def test_remove(self):
        context = Storage.StorageContext('user1')

        loop = asyncio.get_event_loop()

        with self.assertRaises(InvalidPathError):
            loop.run_until_complete(self.storage.remove('% invalid path %', context))
        with self.assertRaises(NoSuchPathError):
            loop.run_until_complete(self.storage.remove('/user1/C', context))
        with self.assertRaises(InvalidPathError):
            loop.run_until_complete(self.storage.remove('/user2/A', context))
        with self.assertRaises(InvalidPathError):
            loop.run_until_complete(self.storage.remove('/user2', context))

        os.mkdir(os.path.join(self.STORAGE, 'user1/C'))
        loop.run_until_complete(self.storage.remove('/user1/C', context))
        self.assertEqual(os.path.exists(os.path.join(self.STORAGE, 'user1/C')), False)

    def test_file_read(self):
        context = Storage.StorageContext('user1')
        loop = asyncio.get_event_loop()

        with self.assertRaises(InvalidPathError):
            loop.run_until_complete(self.storage.file_read('%%invalid', context))
        with self.assertRaises(NoSuchPathError):
            loop.run_until_complete(self.storage.file_read('/user1/С', context))
        with self.assertRaises(NoSuchPathError):
            loop.run_until_complete(self.storage.file_read('/user2/A/'))

        a = loop.run_until_complete(self.storage.file_read('/user2/A/Alg1'))
        self.assertEqual(a.source, '(some (source (here)))')

    def test_create(self):
        context = Storage.StorageContext('user1')
        loop = asyncio.get_event_loop()

        loop.run_until_complete(self.storage.create('/user1/A/С', context=context))
        self.assertEqual(self.storage.exists('/user1/A/С', context=context), True)
        loop.run_until_complete(self.storage.remove('/user1/A/С', context=context))

        a = Algorithm(input_spec=[TypeSpec(type_=TypeSpec.INT)], output_spec=TypeSpec(type_=TypeSpec.INT), source='(foo)')
        loop.run_until_complete(self.storage.create('/user1/A/File', context=context, content=a))
        self.assertEqual(self.storage.exists('/user1/A/File', context=context), True)
        a = loop.run_until_complete(self.storage.file_read('/user1/A/File'))
        self.assertEqual(a.source, '(foo)')
        loop.run_until_complete(self.storage.remove('/user1/A/File', context=context))

    def test_file_write(self):
        context = Storage.StorageContext('user1')
        loop = asyncio.get_event_loop()

        with self.assertRaises(NoSuchPathError):
            loop.run_until_complete(self.storage.file_read('/user1/A', context))
        with self.assertRaises(NoSuchPathError):
            loop.run_until_complete(self.storage.file_read('/user1/D', context))

        a = Algorithm(input_spec=[TypeSpec(type_=TypeSpec.INT)], output_spec=TypeSpec(type_=TypeSpec.INT), source='(foo)')
        loop.run_until_complete(self.storage.create('/user1/A/File', context=context, content=a))

        a.source = '(bar)'
        loop.run_until_complete(self.storage.file_write('/user1/A/File', context=context, content=a))

        b = loop.run_until_complete(self.storage.file_read('/user1/A/File'))
        self.assertEqual(b.source, '(bar)')

        loop.run_until_complete(self.storage.remove('/user1/A/File', context=context))

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