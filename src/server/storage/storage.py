import os
import re
import shutil
import asyncio

from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

from .user import User
from .role import Role
from .role_access import RoleAccess
from .user_access import UserAccess
from .exceptions import *

from server.algorithm.algorithm import Algorithm


class FileInfo:
    def __init__(self, name, path, owner, shared, is_directory, can_write, can_read):
        self.name = name
        self.path = path
        self.owner = owner
        self.shared = shared
        self.is_directory = is_directory
        self.can_write = can_write
        self.can_read = can_read


class Storage:
    class StorageContext:
        def __init__(self, user_login):
            self.user = user_login

    def __init__(self, storage_path='data'):
        users_config = os.path.join(storage_path, 'users.json')
        roles_config = os.path.join(storage_path, 'roles.json')

        self.storage_path = storage_path

        self.users = UserAccess(storage=self, config_path=users_config)
        self.roles = RoleAccess(storage=self, config_path=roles_config)

        self._read_pool = ThreadPoolExecutor()
        self._locked_paths = dict()

        self._init_storage()

    def __del__(self):
        pass

    def owner(self, path):
        if not self.valid(path):
            raise InvalidPathError('Invalid path', path)

        if not self.exists(path):
            raise NoSuchPathError('No such path', path)

        login, *parts = self._path_split(path)

        return self.users.by_login(login)

    def list(self, path, context):
        if not self.valid(path):
            raise InvalidPathError('Invalid path', path)

        if not self.exists(path, context):
            raise NoSuchPathError('No such path', path)

        if not os.path.isdir(os.path.join(self.storage_path, path)):
            raise InvalidPathError('Invalid path: not a directory')

        contents = os.listdir(self._path_full(path))
        result = []

        for item in contents:
            if path == '/' and self.owner(os.path.join(path, item)) is None:
                continue

            if self.exists(os.path.join(path, item), context):
                item_path = os.path.join(path, item)
                result.append(self.file_info(item_path, context))

        return result

    async def move(self, src, dst, context):
        if not self.valid(src):
            raise InvalidPathError('Invalid src path', src)
        if not self.valid(dst):
            raise InvalidPathError('Invalid dst path', dst)

        if not self.exists(src, context):
            raise NoSuchPathError('No such path', src)
        if self.exists(dst, context):
            raise InvalidPathError('Invalid dst path: already exists', dst)

        dst_user, *dst_parts = self._path_split(dst)

        if len(dst_parts) < 1:
            raise InvalidPathError('Invalid dst path: dst cannot be root')

        if dst_user != context.user.login:
            raise InvalidPathError('Invalid dst path: cannot move to '
                                   'another user\'s directory', dst)

        await self._await_path(src)

        info = self.file_info(src, context)

        if not info.can_write:
            raise InvalidPathError('Invalid path: Cannot remove shared path', src)

        shutil.move(os.path.join(self.storage_path, src), os.path.join(self.storage_path, dst))

    async def remove(self, path, context=None):
        if not self.valid(path):
            raise InvalidPathError('Invalid path', path)

        if not self.exists(path, context):
            raise NoSuchPathError('No such path', path)

        await self._await_path(path)

        info = self.file_info(path, context)

        if not info.can_write:
            raise InvalidPathError('Invalid path: Cannot remove shared path', path)

        if not len(self._path_split(path)) > 1:
            raise InvalidPathError('Invalid path: Cannot remove root path', path)

        shutil.rmtree(path)

    async def file_read(self, path, context=None):
        if not self.valid(path):
            raise InvalidPathError('Invalid path', path)

        if not self.exists(path, context):
            raise NoSuchPathError('No such path', path)

        if os.path.isdir(os.path.join(self.storage_path, path)):
            raise NoSuchPathError('Path points to directory, not a file', path)

        with open(os.path.join(self.storage_path, path), 'r') as f:
            loop = asyncio.get_event_loop()
            task = asyncio.ensure_future(loop.run_in_executor(self._read_pool, f.read))

            with self._lock_path(path, task):
                text = await task

        return Algorithm.from_json(text)

    def file_info(self, path, context=None):
        if not self.valid(path):
            raise InvalidPathError('Invalid path', path)

        if not self.exists(path, context):
            raise NoSuchPathError('No such path', path)

        owner, *parts = self._path_split(path)
        name = parts[-1] if parts != [] else '/'

        is_directory = os.path.isdir(self._path_full(path))
        is_shared = False
        can_write = True
        can_read = True

        if context is not None:
            is_shared = owner != context.user
            can_write = False

        return FileInfo(name=name,
                        path=path,
                        owner=owner,
                        shared=is_shared,
                        is_directory=is_directory,
                        can_write=can_write,
                        can_read=can_read)

    def exists(self, path, context=None):
        if not self.valid(path):
            raise InvalidPathError('Invalid path', path)

        if not os.path.exists(self._path_full(path)):
            return False

        if path == '/':
            return True

        if context is not None:
            user, *parts = self._path_split(path)
            if user != context.user:
                role = self.roles.by_path(path)

                if role and context.user in role.users:
                    return True

                return False

        return True

    def valid(self, path):
        if path is None:
            return False

        if not path.startswith('/'):
            return False

        parts = self._path_split(path)

        # allowed characters: letters space - ! ( ) [ ] .
        name_re = re.compile('[\w\-!()\[\] \.]+')

        for part in parts:
            if part == '':
                return False

            if name_re.fullmatch(part) is None:
                return False

        return True

    def _init_storage(self):
        items = os.listdir(self.storage_path)

        for user in self.users.all():
            if not user.login in items:
                os.mkdir(os.path.join(self.storage_path, user.login))

    @contextmanager
    def _lock_path(self, path, task):
        # FIXME: need to check sub paths
        if path not in self._locked_paths:
            self._locked_paths[path] = task

        yield

        if path not in self._locked_paths:
            self._locked_paths.pop(path)

    async def _await_path(self, path):
        if path in self._locked_paths:
            await self._locked_paths.get(path)

    @staticmethod
    def _path_split(path):
        return [part for part in path.split('/') if part != '']

    def _path_full(self, path, *args):
        return os.path.join(self.storage_path, path[1:], *args)