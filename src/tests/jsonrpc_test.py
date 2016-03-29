#!/usr/bin/env python3
import unittest
import asyncio
import json

from server.util import jsonrpc


class TestJsonRPC(unittest.TestCase):
    def test_methods_params_list(self):
        disp = jsonrpc.Dispatcher(self)
        loop = asyncio.get_event_loop()

        req = self._make_request('_test_1', [1, 'test'])
        js = json.loads(loop.run_until_complete(disp.handle(req)))

        self.assertEqual(js.get("result"), "OK")

        req = self._make_request('_test_2', [[1, 2, 3], dict(a=100)])
        js = json.loads(loop.run_until_complete(disp.handle(req)))

        self.assertEqual(js.get("result"), 100)

    def test_methods_params_dict(self):
        disp = jsonrpc.Dispatcher(self)
        loop = asyncio.get_event_loop()

        req = self._make_request('_test_1', dict(a=1, b='test'))
        js = json.loads(loop.run_until_complete(disp.handle(req)))

        self.assertEqual(js.get("result"), "OK")

        req = self._make_request('_test_2', dict(a=[1, 2, 3], b=dict(a=100)))
        js = json.loads(loop.run_until_complete(disp.handle(req)))

        self.assertEqual(js.get("result"), 100)

    def test_methods_params_error(self):
        disp = jsonrpc.Dispatcher(self, self._auth)
        loop = asyncio.get_event_loop()

        # parameters errors
        req = self._make_request('_test_1', dict(a='string', b=[1,2,3]))
        js = json.loads(loop.run_until_complete(disp.handle(req)))

        self.assertEqual(js.get("error").get("code"), -32602)

    def test_json_parse_error(self):
        disp = jsonrpc.Dispatcher(self, self._auth)
        loop = asyncio.get_event_loop()

        # json parse error
        req_wrong_json = '{"jsonrpc" : "2.0", "}'
        js = json.loads(loop.run_until_complete(disp.handle(req_wrong_json)))

        self.assertEqual(js.get("error").get("code"), -32700)

    def test_invalid_request_error(self):
        disp = jsonrpc.Dispatcher(self, self._auth)
        loop = asyncio.get_event_loop()

        # invalid request error
        req_proto = json.loads(self._make_request('_test_1', [1, 'tt']))
        for k in req_proto.keys():
            req_wrong = req_proto.copy()
            req_wrong.pop(k)
            resp = json.loads(loop.run_until_complete(disp.handle(json.dumps(req_wrong))))

            code = -32602 if k == 'params' else -32600
            self.assertEqual(resp.get("error").get("code"), code)

    def test_no_such_method_error(self):
        disp = jsonrpc.Dispatcher(self, self._auth)
        loop = asyncio.get_event_loop()

        # no such method error
        req = self._make_request('_non_exsiting_method', dict(a='string', b=[1,2,3]))
        js = json.loads(loop.run_until_complete(disp.handle(req)))

        self.assertEqual(js.get("error").get("code"), -32601)

    def test_invalid_auth_error(self):
        disp = jsonrpc.Dispatcher(self, self._auth)
        loop = asyncio.get_event_loop()

        # invalid credentials error
        req = self._make_request('_test_1', dict(a=1, b='ss'), id_="wrong id")
        js = json.loads(loop.run_until_complete(disp.handle(req)))

        self.assertEqual(js.get("error").get("code"), 1)

    def test_custom_error(self):
        disp = jsonrpc.Dispatcher(self, self._auth)
        loop = asyncio.get_event_loop()

        # custom errors
        req = self._make_request('_test_3', dict(param=1))
        js = json.loads(loop.run_until_complete(disp.handle(req)))

        self.assertEqual(js.get("error").get("code"), 0xDEAD)
        self.assertEqual(js.get("error").get("message"), "dead")
        self.assertEqual(js.get("error").get("data"), "123")

    def _make_request(self, method, params, id_="1"):
        return """
        {{
         "jsonrpc" : "2.0",
         "id" : "{2}",
         "method" : "{0}",
         "params" : {1}
        }}
        """.format(method, json.dumps(params), id_)

    async def _auth(self, id_):
        return id_ == "1"

    @jsonrpc.Dispatcher.remote_method(int, str)
    async def _test_1(self, a, b):
        return 'OK'

    @jsonrpc.Dispatcher.remote_method(list, dict)
    async def _test_2(self, a, b):
        return 100

    @jsonrpc.Dispatcher.remote_method(int)
    async def _test_3(self, param):
        raise jsonrpc.Error(code=0xDEAD, message="dead", data="123")

if __name__ == '__main__':
    unittest.main()