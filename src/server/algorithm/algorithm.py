import json

from .exceptions import *


class Algorithm:
    def __init__(self, input_spec, output_spec, source):
        self.input_spec = input_spec
        self.output_spec = output_spec
        self.source = source

    def __eq__(self, other):
        return self.source == other.source and \
                self.input_spec == other.input_spec and \
                self.output_spec == other.output_spec

    @staticmethod
    def from_json(text):
        try:
            js = json.loads(text)

            return Algorithm.from_dict(js)
        except json.JSONDecodeError as err:
            raise AlgorithmDecodeError('Invalid JSON', text) from err

    @staticmethod
    def from_dict(js):
        if 'input_spec' not in js:
            js['input_spec'] = []
        if 'output_spec' not in js:
            js['output_spec'] = []
        if 'source' not in js:
            raise AlgorithmDecodeError('No source', js)
        if type(js['input_spec']) != list:
            raise AlgorithmDecodeError('Wrong input spec format', js)
        if type(js['output_spec']) != list:
            raise AlgorithmDecodeError('Wrong output spec format', js)

        input_spec = js['input_spec']
        output_spec = js['output_spec']
        source = js['source']

        return Algorithm(input_spec=input_spec, output_spec=output_spec, source=source)

    def to_dict(self):
        return self.__dict__
