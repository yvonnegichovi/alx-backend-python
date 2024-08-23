#!/usr/bin/env python3
"""
This module is an example of basic annontation
"""

import math


def floor(n: float) -> int:
    """
    Returns the floor of the given float.

    Args:
        n (float): The float number to floor.

    Returns:
        int: The largest integer less than or equal to n.
    """
    return math.floor(n)
