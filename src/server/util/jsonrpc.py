import json
import asyncio
import inspect


class Error(Exception):
    def __init__(self, code, message, data):
        super().__init__(code, message, data)
        self.code = code
        self.data = data
        self.message = message


class InvalidParamsError(Error):
    def __init__(self, message, data=None):
        super().__init__(code=-32602, message=message, data=data)


class AuthError(Error):
    def __init__(self, message, data=None):
        super().__init__(code=1, message=message, data=data)


class Dispatcher:
    def __init__(self, handler, authenticator=None):
        self._handlers = dict()
        self._authenticator = authenticator
        self._handler_obj = handler

        handler_attrs = type(handler).__dict__
        for key, value in handler_attrs.items():
            if hasattr(value, "_json_rpc_dispatch_method"):
                noauth = hasattr(value, "_json_rpc_dispatch_noauth")
                self._register_method(key, value, value._json_rpc_dispatch_method, noauth)

    @staticmethod
    def remote_method(*param_types):
        def wrapper(f):
            params = list(inspect.signature(f).parameters.keys())[1:]

            param_list = [
                (param, param_types[i])
                for i, param in enumerate(params)
            ]

            f._json_rpc_dispatch_method = param_list
            return f
        return wrapper

    @staticmethod
    def remote_noauth(f):
        f._json_rpc_dispatch_noauth = True
        return f

    def _register_method(self, name, coro, params, noauth=False):
        self._handlers[name] = (coro, params, noauth)

    async def handle(self, json_):
        try:
            obj = json.loads(json_)

            id_ = None

            if not self._validate_request(obj):
                return self._error_json(code=-32600, message="Invalid request")

            id_ = obj['id']

            if obj['method'] not in self._handlers:
                return self._error_json(code=-32601, message="No such method")

            handler, args_spec, no_auth = self._handlers.get(obj.get('method'))

            if self._authenticator and not no_auth:
                auth_ok = await self._authenticator(id_)

                if not auth_ok:
                    raise AuthError(message='Invalid credentials')

            if not self._validate_params(args_spec, obj.get('params')):
                raise InvalidParamsError('Wrong arguments')

            if type(obj['params']) is list:
                result = await handler(self._handler_obj, *obj['params'])
            else:
                result = await handler(self._handler_obj, **obj['params'])

            return self._result_json(result, id_)

        except json.JSONDecodeError as error:
            return self._error_json(code=-32700,
                                    message="Json parse error",
                                    data=dict(
                                        message=error.msg,
                                        column=error.colno,
                                        line=error.lineno))
        except Error as error:
            return self._error_json(code=error.code, message=error.message, data=error.data, id_=id_)

    @staticmethod
    def _validate_params(args_spec, args):
        if args is None and len(args_spec) > 0:
            return False

        if len(args_spec) != len(args):
            return False

        if type(args) == list:
            for i, arg in enumerate(args):
                if type(arg) != args_spec[i][1]:
                    return False
        else:
            for k, v in args.items():
                if (k, type(v)) not in args_spec:
                    return False

        return True

    @staticmethod
    def _validate_request(obj):
        if type(obj) != dict:
            return False

        validators = dict(
            id=lambda x: type(x) == str,
            jsonrpc=lambda x: x == '2.0',
            method=lambda x: type(x) == str
        )

        for key, is_valid in validators.items():
            if key not in obj:
                return False

            if not is_valid(obj[key]):
                return False

        if 'params' in obj and type(obj['params']) not in (list, dict):
            return False

        return True

    @staticmethod
    def _result_json(result, id_):
        result = dict(
            jsonrpc="2.0",
            id=id_,
            result=result
        )
        return json.dumps(result)

    @staticmethod
    def _error_json(code, message, data=None, id_=None):
        error = dict(
            jsonrpc="2.0",
            error=dict(
                code=code,
                message=message,
                data=data
            )
        )

        if id_ is not None:
            error['id'] = id_

        return json.dumps(error)