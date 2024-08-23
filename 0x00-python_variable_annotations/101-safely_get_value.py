#!/usr/bin/env python3
"""
This is an advanced task for basic annontation
"""

from typing import Mapping, Any, Union, TypeVar

T = TypeVar('T')


def safely_get_value(dct: Mapping[Any, T], key: Any, default: Union[T, None] = None) -> Union[T, None]:
    """
    Returns the value for the given key from the dictionary if it exists;
    otherwise, returns the default value.

    Args:
        dct (Mapping[Any, T]): A mapping (e.g., dictionary)
        with keys of any type and values of type T.
        key (Any): The key to look up in the dictionary.
        default (Union[T, None]): The value to return if the key is not found;
        defaults to None.

    Returns:
        Union[T, None]: The value associated with the key or
        the default value if the key is not found.
    """
    if key in dct:
        return dct[key]
    else:
        return default
