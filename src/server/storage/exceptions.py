class ConfigError(Exception):
    def __init__(self, msg, path):
        super().__init__(msg, path)


class InvalidPathError(Exception):
    def __init__(self, msg, path):
        super().__init__(msg, path)


class NoSuchPathError(Exception):
    def __init__(self, msg, path):
        super().__init__(msg, path)
