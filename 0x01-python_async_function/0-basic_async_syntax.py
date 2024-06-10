#!/usr/bin/env python3
"""
This module is for async and await execution
"""

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """
    This aynchronous coroutine takes in an integer argument with a default
    value of 10 named wait_random
    """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
