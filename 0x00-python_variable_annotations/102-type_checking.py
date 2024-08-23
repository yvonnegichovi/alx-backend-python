#!/usr/bin/env python3
"""
This script demonstrates type checking for a zoom array function.
"""

from typing import List


def zoom_array(lst: List[int], factor: int = 2) -> List[int]:
    """
    Zooms into a list by repeating each element 'factor' times.

    Args:
        lst (List[int]): The list of integers to zoom in.
        factor (int): The number of times to repeat each element.

    Returns:
        List[int]: A new list with elements repeated 'factor' times.
    """
    if not isinstance(factor, int):
        raise TypeError("factor must be an integer")
    
    zoomed_in: List[int] = [
        item for item in lst
        for _ in range(factor)
    ]
    return zoomed_in

array = [12, 72, 91]

zoom_2x = zoom_array(array)

# This will raise a TypeError since 3.0 is not an int
try:
    zoom_3x = zoom_array(array, 3.0)
except TypeError as e:
    print(e)
