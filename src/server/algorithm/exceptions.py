class AlgorithmError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AlgorithmParseError(AlgorithmError):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class BlockSyntaxError(AlgorithmError):
    def __init__(self, msg, block, pos):
        super().__init__(msg, block, pos)
        self.msg = msg
        self.block = block
        self.pos = pos


class BlockEvalError(AlgorithmError):
    def __init__(self, msg, block):
        super().__init__(msg, block)
        self.msg = msg
        self.block = block


class BlockSymbolError(AlgorithmError):
    def __init__(self, msg, block, sym, pos):
        super().__init__(msg, block, sym, pos)
        self.msg = msg
        self.block = block
        self.sym = sym
        self.pos = pos


class GraphConnectivityError(AlgorithmError):
    def __init__(self, msg, block):
        super().__init__(msg, block)
        self.msg = msg
        self.block = block


class GraphTimeoutError(AlgorithmError):
    def __init__(self, msg, time):
        super().__init__(msg, time)
        self.msg = msg
        self.time = time