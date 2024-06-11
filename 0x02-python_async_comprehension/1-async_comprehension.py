#!/usr/bin/env python3
"""
This module has coroutine asynchronous functions
"""

from typing import List
import asyncio
import random


async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """
    Collects 10 random numbers using async comprehensing over
    async_generator, then return 10 random numbers
    """
    return [number async for number in async_generator()]
