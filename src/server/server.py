#!/usr/bin/env python3
from aiohttp import web
import json

class Server:    
    def __init__(self):
        self._app = web.Application()
        self._app.router.add_route('POST', '/api', self._handler)
        
    async def _handler(self, request):
        print('>> from client: ')
        print('thingy from {0}'.format(request.match_info.get('name', 'unknown')))
        obj = await request.json()
        for k,v in obj.items():
            print('"{0}" = {1}'.format(k, v))
        
        return web.Response(body=json.dumps('thanks').encode('utf-8'))
    
    def run(self):
        web.run_app(self._app)
        
if __name__ == "__main__":
    Server().run()
