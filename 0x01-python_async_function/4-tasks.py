#!/usr/bin/env python3
"""
This module shows aysnchronous and await functionalities
"""

import asyncio
from typing import List


task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    This function runs 'wait_random' n times concurrently
    The results are collected and returned in ascending order
    without explicitly sorting the list
    """
    coroutines = [task_wait_random(max_delay) for _ in range(n)]
    delays = await asyncio.gather(*coroutines)
    return sorted(delays)
