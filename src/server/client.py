#!/usr/bin/env python3
import aiohttp
import asyncio
import json
import sys

if __name__ == '__main__':
    method = sys.argv[1]
    id_ = sys.argv[2]
    js = sys.argv[3]

    loop = asyncio.get_event_loop()

    req = """
    {{
        "jsonrpc" : "2.0",
        "id" : "{0}",
        "method" : "{1}",
        "params" : {2}
    }}
    """.format(id_, method, js)

    with aiohttp.ClientSession(loop=loop) as session:
        resp = loop.run_until_complete(session.post('http://127.0.0.1:8080/api', data=req.encode('utf-8')))
        print(loop.run_until_complete(resp.text()))
