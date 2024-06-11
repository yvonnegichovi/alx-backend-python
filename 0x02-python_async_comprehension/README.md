## 0x02. Python - Async Comprehension
## Project Overview
This project focuses on understanding and implementing asynchronous comprehensions in Python. By the end of this project, you should be able to:

Write an asynchronous generator.
Use async comprehensions.
Type-annotate generators.
## Resources
To help you with the project, you may refer to:

PEP 530 – Asynchronous Comprehensions
What’s New in Python: Asynchronous Comprehensions / Generators
Type-hints for generators
## Learning Objectives
By completing this project, you should be able to explain:

How to write an asynchronous generator.
How to use async comprehensions.
How to type-annotate generators.
## Requirements
Editor: vi, vim, emacs
Interpreter: Python 3.7 on Ubuntu 18.04 LTS
Style: pycodestyle (version 2.5.x)
All files must end with a new line.
The first line of all files should be #!/usr/bin/env python3.
A README.md file at the root of the project is mandatory.
Documentation is required for all modules and functions.
All functions and coroutines must be type-annotated.
## Tasks
Task 0: Async Generator
Write a coroutine called async_generator that takes no arguments. The coroutine should loop 10 times, each time asynchronously waiting 1 second, then yielding a random number between 0 and 10.

Example Usage:

python
#!/usr/bin/env python3

import asyncio
from 0_async_generator import async_generator

async def print_yielded_values():
    result = []
    async for i in async_generator():
        result.append(i)
    print(result)

asyncio.run(print_yielded_values())
Expected Output:

csharp
[4.403136952967102, 6.9092712604587465, 6.293445466782645, 4.549663490048418, 4.1326571686139015, 9.99058525304903, 6.726734105473811, 9.84331704602206, 1.0067279479988345, 1.3783306401737838]
Task 1: Async Comprehensions
Import async_generator from the previous task and write a coroutine called async_comprehension that takes no arguments. The coroutine will collect 10 random numbers using an async comprehension over async_generator, then return the 10 random numbers.

Example Usage:

python
#!/usr/bin/env python3

import asyncio
from 1_async_comprehension import async_comprehension

async def main():
    print(await async_comprehension())

asyncio.run(main())
Expected Output:

csharp
[9.861842105071727, 8.572355293354995, 1.7467182056248265, 4.0724372912858575, 0.5524750922145316, 8.084266576021555, 8.387128918690468, 1.5486451376520916, 7.713335177885325, 7.673533267041574]
Task 2: Run Time for Four Parallel Comprehensions
Import async_comprehension from the previous file and write a measure_runtime coroutine that will execute async_comprehension four times in parallel using asyncio.gather. measure_runtime should measure the total runtime and return it.

Example Usage:

python
#!/usr/bin/env python3

import asyncio
from 2_measure_runtime import measure_runtime

async def main():
    return await measure_runtime()

print(asyncio.run(main()))
Expected Output:

10.021936893463135
Repository Structure
alx-backend-python
└── 0x02-python_async_comprehension
    ├── 0-async_generator.py
    ├── 1-async_comprehension.py
    ├── 2-measure_runtime.py
    ├── README.md
