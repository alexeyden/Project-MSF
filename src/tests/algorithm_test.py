#!/usr/bin/env python3
import unittest
import json

from algorithm.exceptions import *
from algorithm.algorithm import *


class TestAlgorithm(unittest.TestCase):
    def test_parse_algorithm(self):
        alg = Algorithm(["a","b"], ["x","y"], '(some (source (here)))')

        with open('data/algorithm.json', 'r') as f:
            self.assertEqual(alg, Algorithm.from_json(f.read()))

    def test_parse_errors(self):
        with open('data/algorithm_wrong.json', 'r') as f:
            with self.assertRaises(AlgorithmDecodeError):
                Algorithm.from_json(f.read())

if __name__ == '__main__':
    unittest.main()