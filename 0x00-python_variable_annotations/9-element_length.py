#!/usr/bin/env python3
"""
This module lists tuples where tuple contains elements from the tuple iterable
"""

from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Returns a list of tuples where each tuple contains
    an element from the input iterable
    and the length of that element.

    Args:
        lst (Iterable[Sequence]): An iterable of sequences
        (e.g., strings, lists, tuples).

    Returns:
        List[Tuple[Sequence, int]]: A list of tuples,
        each containing a sequence and its length.
    """
    return [(i, len(i)) for i in lst]
