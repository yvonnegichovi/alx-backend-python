#!/usr/bin/env python3
"""This module returns a tuple where the first element is a string"""

from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Returns a tuple where the first element is a string k and the second
    element is the square of the int/float v as a float.

    Args:
        k (str): A string.
        v (Union[int, float]): An integer or float.

    Returns:
        Tuple[str, float]: A tuple containing the string k
        and the square of v as a float.
    """
    return (k, float(v ** 2))
