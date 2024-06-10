#!/usr/bin/env python3
"""
This module shows aysnchronous and await functionalities
"""

import asyncio
from typing import List
from heapq import nsmallest
from 0-basic_async_syntax import wait_random


async def wait_n(n: int, max_delay: int) -> list[float]:
    """
    This function runs 'wait_random' n times concurrently
    The results are collected and returned in ascending order
    without explicitly sorting the list
    """
    coroutines = [wait_random(max_delay) for _ in range(n)]
    delays = await asyncio.gather(*coroutines)
    return delays
