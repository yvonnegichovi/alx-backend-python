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
        """
        Tests access_nested_map with parameterized inputs
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a")),
        ({"a": 1}, ("a", "b")),
    ])

    def test_access_nested_map_exception(self, nested_map, path):
        """
        Tests access_nested_map raises KeyError with parameterized inputs
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), str(KeyError(path[-1])))


if __name__ == "__main__":
    unittest.main()
