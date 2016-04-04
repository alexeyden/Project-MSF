#!/usr/bin/env python3
import unittest
import json

from server.algorithm.exceptions import *
from server.algorithm.type_spec import *
from server.algorithm.algorithm import *


class TestAlgorithm(unittest.TestCase):
    def test_parse_algorithm(self):
        input_spec = [
            TypeSpec(TypeSpec.LIST, TypeSpec(TypeSpec.INT, None)),
            TypeSpec(TypeSpec.INT, None)
        ]
        output_spec = TypeSpec(TypeSpec.REAL, None)
        alg = Algorithm(input_spec, output_spec, '(some (source (here)))')

        with open('data/algorithm.json', 'r') as f:
            self.assertEqual(alg, Algorithm.from_json(f.read()))

    def test_parse_type_spec(self):
        with open('data/type_spec_wrong.json', 'r') as f:
            specs = json.load(f)

        for s in specs:
            with self.assertRaises(AlgorithmDecodeError):
                TypeSpec.from_dict(s)

    def test_parse_errors(self):
        with open('data/algorithm_wrong.json', 'r') as f:
            with self.assertRaises(AlgorithmDecodeError):
                Algorithm.from_json(f.read())

if __name__ == '__main__':
    unittest.main()