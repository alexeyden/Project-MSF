from util.jsonrpc import Error


class RpcInvalidPathError(Error):
    def __init__(self, message, data=None):
        super().__init__(code=2, message=message, data=data)


class RpcNoSuchPathError(Error):
    def __init__(self, message, data=None):
        super().__init__(code=3, message=message, data=data)

class RpcAlgorithmExecError(Error):
    def __init__(self, message, data=None):
        super().__init__(code=4, message=message, data=data)

