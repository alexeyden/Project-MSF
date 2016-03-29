#!/usr/bin/env python3
from aiohttp import web
from util import jsonrpc

jsonrpc_method = jsonrpc.Dispatcher.remote_method


class Server:    
    def __init__(self):
        self._app = web.Application()
        self._app.router.add_route('POST', '/api', self._handler)

        self._dispatcher = jsonrpc.Dispatcher(self)

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
    
    def run(self):
        web.run_app(self._app)
        
if __name__ == "__main__":
    Server().run()
