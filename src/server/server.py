#!/usr/bin/env python3

import argparse
import sys

from aiohttp import web
from util import jsonrpc

from storage.storage import Storage
from storage.exceptions import *

jsonrpc_method = jsonrpc.Dispatcher.remote_method


class Server:    
    def __init__(self, data_path, debug=False):
        self._app = web.Application()
        self._app.router.add_route('POST', '/api', self._handler)

        self._dispatcher = jsonrpc.Dispatcher(self)
        self._debug = debug
        self.storage = Storage(storage_path=data_path)

    @jsonrpc_method(str, str)
    async def user_authorize(self, login, password):
        return "user_authorize"

    @jsonrpc_method(str)
    async def path_list(self, path):
        return "user_authorize"

    @jsonrpc_method(str)
    async def path_fetch(self, path):
        return "path_fetch"

    @jsonrpc_method(str, list)
    async def path_exec(self, path, args):
        return "path_exec"

    @jsonrpc_method(str)
    async def path_create(self, path):
        return "path_create"

    @jsonrpc_method(str, str)
    async def path_move(self, source, dest):
        return "path_move"

    @jsonrpc_method(str, dict)
    async def path_edit(self, path, alg):
        return "path_edit"

    @jsonrpc_method(str)
    async def path_remove(self, path):
        return "path_remove"

    async def _handler(self, request):
        text = await request.text()
        resp = await self._dispatcher.handle(text)

        return web.Response(body=resp.encode('utf-8'))
    
    def run(self, host, port):
        web.run_app(self._app, host=host, port=port)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', help='data storage path', default='data', metavar='DATA_PATH')
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
        server = Server(data_path=args.data, debug=args.verbose)
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
