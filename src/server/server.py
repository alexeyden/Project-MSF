#!/usr/bin/env python3

import argparse
import sys
import os
import time
import mimetypes

from aiohttp import web
from util import jsonrpc

from storage.storage import Storage
from storage.exceptions import *
from algorithm.algorithm import *
from algorithm.executor import Executor
from algorithm.exceptions import *
from exceptions import *

jsonrpc_method = jsonrpc.Dispatcher.remote_method
jsonrpc_noauth = jsonrpc.Dispatcher.remote_noauth


class Authenticator:
    def __init__(self, storage):
        self.storage = storage
        self.token = None

    async def __call__(self, token):
        self.token = None

        for user in self.storage.users.all():
            # TODO: token expire

            if user.token == token:
                self.token = token
                return True

        return False


class Server:    
    def __init__(self, data_path, client_path='../client', debug=False):
        self._app = web.Application()
        self._app.router.add_route('POST', '/api', self._api_handler)
        self._app.router.add_route('GET', '/{path:.*}', self._web_handler)

        #self._app.router.add_static('/', '../client')
        self.client_data = client_path
        self.storage = Storage(storage_path=data_path)
        self.executor = Executor()

        self._debug = debug
        self._auth = Authenticator(self.storage)
        self._dispatcher = jsonrpc.Dispatcher(self, self._auth)

    @jsonrpc_method(str, str)
    @jsonrpc_noauth
    async def user_authorize(self, login, password):
        self._log('user_authorize({0}, {1})'.format(login, password))

        auth_token = self.storage.users.auth(login, password)

        if not auth_token:
            self._log('  auth failed: invalid login or password')
            raise jsonrpc.AuthError("Неверная пара логин\\пароль!")

        self._log('return: auth token: {0}'.format(auth_token))
        return auth_token

    @jsonrpc_method(str, bool)
    async def path_list(self, path, recursive):
        self._log('path_list({0})'.format(path))

        context = self._context()

        try:
            contents = self.storage.list(path, context, recursive=recursive)
            result = [item.to_dict() for item in contents]
            self._log("return: items: {0}".format(", ".join([item.name for item in contents])))

            return result
        except InvalidPathError as err:
            raise RpcInvalidPathError("Неверный путь", path) from err
        except NoSuchPathError as err:
            raise RpcNoSuchPathError("Нет такого каталога", path) from err

    @jsonrpc_method(str)
    async def algorithm_fetch(self, path):
        self._log('algorithm_fetch({0})'.format(path))

        context = self._context()

        try:
            contents = await self.storage.file_read(path, context)
            result = contents.to_dict()
            result['name'] = path.split('/')[-1]

            self._log("return: algorithm {0}".format(result.get("name")))

            return result
        except InvalidPathError as err:
            raise RpcInvalidPathError("Неверный путь", path) from err
        except NoSuchPathError as err:
            raise RpcNoSuchPathError("Нет такого файла", path) from err

    @jsonrpc_method(dict, dict)
    async def algorithm_exec(self, alg, args):
        self._log('algorithm_exec({0}, {1})'.format("alg", args))

        context = self._context()

        try:
            self._log("  executing algorithm")
            result = await self.executor.run(Algorithm.from_dict(alg), args)

            self._log("return: result: {0}".format(result))
            return result
        except AlgorithmError as err:
            raise RpcAlgorithmExecError(err.msg)

    @jsonrpc_method(str, dict)
    async def algorithm_create(self, path, alg_dict):
        self._log('algorithm_create({0}, alg)'.format(path))

        context = self._context()

        alg = Algorithm.from_dict(alg_dict)

        try:
            await self.storage.create(path, content=alg, context=context)

            self._log("return: OK")

            return 'OK'
        except InvalidPathError as err:
            raise RpcInvalidPathError("Неверный путь", path) from err

    @jsonrpc_method(str)
    async def path_create(self, path):
        self._log('path_create({0})'.format(path))

        context = self._context()

        try:
            await self.storage.create(path, context=context)

            self._log("return: OK")

            return 'OK'
        except InvalidPathError as err:
            raise RpcInvalidPathError("Неверный путь", path) from err

    @jsonrpc_method(str, str)
    async def path_move(self, source, dest):
        self._log('path_move({0},{1})'.format(source, dest))

        context = self._context()

        try:
            await self.storage.move(source, dest, context)

            self._log("return: OK")

            return 'OK'
        except InvalidPathError as err:
            raise RpcInvalidPathError("Неверный путь", err.args[1]) from err
        except NoSuchPathError as err:
            raise RpcNoSuchPathError("Нет такого файла или каталога", err.args[1]) from err

    @jsonrpc_method(str, dict)
    async def algorithm_update(self, path, alg_dict):
        self._log('algorithm_update({0}, alg)'.format(path))

        context = self._context()
        alg = Algorithm.from_dict(alg_dict)

        try:
            await self.storage.file_write(path, alg, context)

            self._log("return: OK")

            return 'OK'
        except InvalidPathError as err:
            raise RpcInvalidPathError("Неверный путь", err.args[1]) from err
        except NoSuchPathError as err:
            raise RpcNoSuchPathError("Нет такого файла", err.args[1]) from err

    @jsonrpc_method(str)
    async def path_remove(self, path):
        self._log('algorithm_update({0}, alg)'.format(path))

        context = self._context()

        try:
            await self.storage.remove(path, context)

            self._log("return: OK")

            return 'OK'
        except InvalidPathError as err:
            raise RpcInvalidPathError("Неверный путь", err.args[1]) from err
        except NoSuchPathError as err:
            raise RpcNoSuchPathError("Нет такого файла или каталога", err.args[1]) from err

    async def _web_handler(self, request):
        path = request.path
        if path == '/':
            path = '/index.html'

        content_root = self.client_data
        if self._debug:
            print('GET static file: ' + content_root + path)

        if os.path.exists(content_root + path) and not os.path.isdir(content_root + path):
            with open(content_root + path, 'rb') as f:
                resp = f.read()
        else:
            raise web.HTTPNotFound()
	
        mimetype,_ = mimetypes.guess_type(content_root + path)

        return web.Response(body=resp, content_type = mimetype if mimetype else 'application/octet-stream')

    async def _api_handler(self, request):
        text = await request.text()
        resp = await self._dispatcher.handle(text)

        return web.Response(body=resp.encode('utf-8'))

    def run(self, host, port):
        web.run_app(self._app, host=host, port=port)

    def _context(self):
        user = self.storage.users.by_token(self._auth.token)
        return Storage.StorageContext(user_login=user.login)

    def _log(self, msg):
        if self._debug:
            print(msg)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', help='data storage path', default='data', metavar='DATA_PATH')
    parser.add_argument('-e', '--client-data', help='web client path', default='../client', metavar='CLIENT_PATH')
    parser.add_argument('-v', '--verbose', help='print debug messages', action='store_true')
    parser.add_argument('-l', '--listen', help='listening host', default='', metavar='HOST')
    parser.add_argument('-p', '--port', help='listening port', default=8080, type=int)

    parser.add_argument('-a', '--add-user', help='create new user and exit', nargs=2,
                        metavar=('LOGIN', 'PASSWORD'))
    parser.add_argument('-c', '--change-password', help='change password and exit', nargs=2,
                        metavar=('LOGIN', 'NEW_PASSWORD'))
    parser.add_argument('-r', '--remove-user', help='delete user and exit', metavar='LOGIN')

    args = parser.parse_args()

    try:
        server = Server(data_path=args.data, debug=args.verbose, client_path=args.client_data)
    except ConfigError as error:
        print('Config Error ({1}):\n\t{0}'.format(*error.args), file=sys.stderr)

        sys.exit(1)

    if args.add_user:
        if not server.storage.users.create(*args.add_user):
            print('User already exists')
            sys.exit(1)
        sys.exit(0)

    if args.change_password:
        if not server.storage.users.change_password(*args.change_password):
            print('No such user')
            sys.exit(1)
        sys.exit(0)

    if args.remove_user:
        if not server.storage.users.remove(*args.remove_user):
            print('No such user')
            sys.exit(1)
        sys.exit(0)

    if args.verbose:
        print('Server is listening on {0}:{1}'.format(args.listen, args.port))

    server.run(host=args.listen, port=args.port)

if __name__ == "__main__":
    main()
