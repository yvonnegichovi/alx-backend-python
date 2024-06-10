# Python Async Project

This project demonstrates the basics of asynchronous programming in Python using `asyncio`. The main focus is on understanding the `async` and `await` syntax, running concurrent coroutines, creating asyncio tasks, and measuring their execution time.

## Learning Objectives

- Understand `async` and `await` syntax
- Execute an async program with `asyncio`
- Run concurrent coroutines
- Create `asyncio` tasks
- Use the `random` module

## Requirements

- Python 3.7 on Ubuntu 18.04 LTS
- All code should be type-annotated and follow `pycodestyle` guidelines
- All modules and functions must have proper documentation

## Project Tasks

1. **The basics of async:** Create an asynchronous coroutine that waits for a random delay and returns it.
2. **Execute multiple coroutines:** Run multiple coroutines concurrently and return their results in ascending order.
3. **Measure the runtime:** Measure the execution time for running multiple coroutines.
4. **Tasks:** Create an asyncio Task from a coroutine.
5. **Tasks with concurrency:** Modify a function to use asyncio tasks for concurrent execution.
Task 0: The basics of async
File: 0-basic_async_syntax.py
python
Copy code
#!/usr/bin/env python3
import asyncio
import random

async def wait_random(max_delay: int = 10) -> float:
    """
    Wait for a random delay between 0 and max_delay seconds and return it.
    """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
File: 0-main.py
python
Copy code
#!/usr/bin/env python3
import asyncio
from 0-basic_async_syntax import wait_random

print(asyncio.run(wait_random()))
print(asyncio.run(wait_random(5)))
print(asyncio.run(wait_random(15)))
Task 1: Execute multiple coroutines
File: 1-concurrent_coroutines.py
python
Copy code
#!/usr/bin/env python3
import asyncio
from typing import List
from 0-basic_async_syntax import wait_random

async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Spawn wait_random n times with the specified max_delay.
    Return the list of delays in ascending order.
    """
    tasks = [asyncio.create_task(wait_random(max_delay)) for _ in range(n)]
    delays = await asyncio.gather(*tasks)
    return sorted(delays)
File: 1-main.py
python
Copy code
#!/usr/bin/env python3
import asyncio
from 1-concurrent_coroutines import wait_n

print(asyncio.run(wait_n(5, 5)))
print(asyncio.run(wait_n(10, 7)))
print(asyncio.run(wait_n(10, 0)))
Task 2: Measure the runtime
File: 2-measure_runtime.py
python
Copy code
#!/usr/bin/env python3
import time
import asyncio
from 1-concurrent_coroutines import wait_n

def measure_time(n: int, max_delay: int) -> float:
    """
    Measure the total execution time for wait_n(n, max_delay), and return total_time / n.
    """
    start_time = time.time()
    asyncio.run(wait_n(n, max_delay))
    end_time = time.time()
    total_time = end_time - start_time
    return total_time / n
File: 2-main.py
python
Copy code
#!/usr/bin/env python3
from 2-measure_runtime import measure_time

n = 5
max_delay = 9

print(measure_time(n, max_delay))
Task 3: Tasks
File: 3-tasks.py
python
Copy code
#!/usr/bin/env python3
import asyncio
from 0-basic_async_syntax import wait_random

def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Create an asyncio Task from the wait_random coroutine.
    """
    return asyncio.create_task(wait_random(max_delay))
File: 3-main.py
python
Copy code
#!/usr/bin/env python3
import asyncio
from 3-tasks import task_wait_random

async def test(max_delay: int) -> float:
    task = task_wait_random(max_delay)
    await task
    print(task.__class__)

asyncio.run(test(5))
Task 4: Tasks with concurrency
File: 4-tasks.py
python
Copy code
#!/usr/bin/env python3
import asyncio
from typing import List
from 3-tasks import task_wait_random

async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    Spawn task_wait_random n times with the specified max_delay.
    Return the list of delays in ascending order.
    """
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    delays = await asyncio.gather(*tasks)
    return sorted(delays)
File: 4-main.py
python
Copy code
#!/usr/bin/env python3
import asyncio
from 4-tasks import task_wait_n

n = 5
max_delay = 6
print(asyncio.run(task_wait_n(n, max_delay)))
This completes the initial setup and implementation for the tasks outlined in the project. Ensure that each script is executable and properly documented as required.
