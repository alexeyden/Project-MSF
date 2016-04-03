class ConfigError(Exception):
    def __init__(self, msg, path):
        super().__init__(msg, path)
