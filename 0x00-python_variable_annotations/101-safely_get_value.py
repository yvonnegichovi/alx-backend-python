#!/usr/bin/env python3

"""Type-annotated function safely_get_value that takes a dictionary d,
    a key k and an optional default value
"""

from typing import Mapping, Any, TypeVar, Union, Optional

# Define a TypeVar for the default value
T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Optional[Union[T, None]] = None
                     ) -> Union[Any, T]:
    """Return the value linked to a key in a dictionary.
    """
    if key in dct:
        return dct[key]
    else:
        return default
