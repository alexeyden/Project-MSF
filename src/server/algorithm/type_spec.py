from .exceptions import *


class TypeSpec:
    INT = 'int'
    REAL = 'real'
    STRING = 'string'
    LIST = 'list'

    PRIMITIVE_TYPES = [INT, REAL, STRING]
    COMPOSITE_TYPES = [LIST]

    def __init__(self, type_, child):
        self.type = type_
        self.child = child

    def __eq__(self, other):
        return self.type == other.type and \
                self.child == other.child

    @staticmethod
    def from_dict(dict_):
        if 'type' not in dict_:
            raise AlgorithmDecodeError('no type in type_spec', dict_)
        if 'child' not in dict_:
            raise AlgorithmDecodeError('no child in type_spec', dict_)

        # TODO: additional checks

        type_ = dict_['type']
        child = None

        if type_ in TypeSpec.COMPOSITE_TYPES:
            if dict_.get('child') is None:
                raise AlgorithmDecodeError('no child for composite type', dict_)

            child = TypeSpec.from_dict(dict_['child'])

        return TypeSpec(type_, child)


class TypedValue:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value