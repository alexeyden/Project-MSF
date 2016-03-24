#!/usr/bin/env python3
import aiohttp
import asyncio
import json
import sys

if __name__ == '__main__':
    js = json.dumps(dict(hello='world', foo=['bar', 'baz'], num=666))
    if len(sys.argv) > 1:
        js = sys.argv[1]
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        resp = loop.run_until_complete(session.post('http://127.0.0.1:8080/api', data=js.encode('utf-8')))
        print('>> from server: ')
        print(loop.run_until_complete(resp.text()))
