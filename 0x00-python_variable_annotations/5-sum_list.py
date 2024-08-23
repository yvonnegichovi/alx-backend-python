#!/usr/bin/env python3
""" This module returns a list of sums"""

from typing import List


def sum_list(input_list: List[float]) -> float:
    """
    Returns the sum of a list of floats.

    Args:
        input_list (List[float]): A list of floats.

    Returns:
        float: The sum of the floats in the list.
    """
    return sum(input_list)
