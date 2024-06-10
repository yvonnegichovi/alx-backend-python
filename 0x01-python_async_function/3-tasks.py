#!/usr/bin/env python3
"""
This module focuses on asyncio and await
"""

import asyncio


wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Creates an asyncio.Task that runs wait_random with the specified max_delay.

    Args:
        max_delay (int): The maximum delay for wait_random.

    Returns:
        asyncio.Task: An asyncio task object.
    """
    return asyncio.create_task(wait_random(max_delay))
