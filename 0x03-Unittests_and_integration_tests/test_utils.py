#!/usr/bin/env python3
"""
This module has tests
"""

from parameterized import parameterized
import unittest


def access_nested_map(nested_map, path):
    """
    This method tests parameterization
    """
    current = nested_map
    for key in path:
        current = current[key]
    return current


class TestAccessNestedMap(unittest.TestCase):
    """
    This class parameterize a unit test
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])

    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == "__main__":
    unittest.main()
