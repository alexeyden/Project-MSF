class AlgorithmDecodeError(Exception):
    def __init__(self, msg, js):
        super().__init__(msg, js)