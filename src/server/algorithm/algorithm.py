import json

from .exceptions import *
from .type_spec import *


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

            if 'input_spec' not in js:
                raise AlgorithmDecodeError('No input_spec', text)
            if 'output_spec' not in js:
                raise AlgorithmDecodeError('No output spec', text)
            if 'source' not in js:
                raise AlgorithmDecodeError('No source', text)
            if type(js['input_spec']) != list:
                raise AlgorithmDecodeError('Wrong input spec format', text)

            input_spec = [TypeSpec.from_dict(spec) for spec in js['input_spec']]
            output_spec = TypeSpec.from_dict(js['output_spec'])
            source = js['source']

            return Algorithm(input_spec=input_spec, output_spec=output_spec, source=source)

        except json.JSONDecodeError as err:
            raise AlgorithmDecodeError('Invalid JSON', text) from err
