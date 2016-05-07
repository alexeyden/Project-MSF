#!/usr/bin/env python3
import aiohttp
import asyncio
import json
import sys

if __name__ == '__main__':
    method = sys.argv[1]
    js = sys.argv[2]
    id_ = sys.argv[3]

    loop = asyncio.get_event_loop()

    req = """
    {{
        "jsonrpc" : "2.0",
        "id" : "{0}",
        "method" : "{1}",
        "params" : {2}
    }}
    """.format(id_, method, js)

    quiet = '-q' in sys.argv

    if not quiet:
        print('Request:')
        print(req)

    with aiohttp.ClientSession(loop=loop) as session:
        resp = loop.run_until_complete(session.post('http://127.0.0.1:8080/api', data=req.encode('utf-8')))
        text = loop.run_until_complete(resp.text())
        if not quiet:
            print('Response:')
            print(text)
        else:
            print(json.dumps(json.loads(text)['result']))
