# 0x00. Python - Variable Annotations

## Project Details
- Language: Python
- Area: Back-end
- Weight: 1
- Project Duration: Jun 6, 2024, 6:00 AM - Jun 7, 2024, 6:00 AM
- Auto QA review will be launched at the deadline

## Concepts
- Advanced Python

## Resources
Read or watch:
- [Python 3 typing documentation](https://docs.python.org/3/library/typing.html)
- [MyPy cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)

## Learning Objectives
### General
By the end of this project, you should be able to explain:
- Type annotations in Python 3
- How to use type annotations to specify function signatures and variable types
- Duck typing
- How to validate your code with MyPy

## Requirements
### General
- Allowed editors: vi, vim, emacs
- All files interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
- All files end with a new line
- First line of all files should be exactly `#!/usr/bin/env python3`
- A README.md file at the root of the project folder is mandatory
- Code should use pycodestyle style (version 2.5.)
- All files must be executable
- Length of files will be tested using wc
- All modules should have documentation (`python3 -c 'print(__import__("my_module").__doc__)'`)
- All classes should have documentation (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`)
- All functions (inside and outside a class) should have documentation (`python3 -c 'print(__import__("my_module").my_function.__doc__)'` and `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`)
- Documentation should be a real sentence explaining the purpose of the module, class, or method (length will be verified)

## Tasks
### 0. Basic annotations - add
- **Mandatory**
- Write a type-annotated function `add` that takes two float arguments `a` and `b`, and returns their sum as a float.

### 1. Basic annotations - concat
- **Mandatory**
- Write a type-annotated function `concat` that takes two string arguments `str1` and `str2`, and returns their concatenated string.

### 2. Basic annotations - floor
- **Mandatory**
- Write a type-annotated function `floor` that takes a float argument `n`, and returns its floor as an integer.

### 3. Basic annotations - to string
- **Mandatory**
- Write a type-annotated function `to_str` that takes a float argument `n`, and returns its string representation.

### 4. Define variables
- **Mandatory**
- Define and annotate variables `a`, `pi`, `i_understand_annotations`, and `school` with specified values.

### 5. Complex types - list of floats
- **Mandatory**
- Write a type-annotated function `sum_list` that takes a list of floats as input and returns their sum as a float.

### 6. Complex types - mixed list
- **Mandatory**
- Write a type-annotated function `sum_mixed_list` that takes a list of integers and floats and returns their sum as a float.

### 7. Complex types - string and int/float to tuple
- **Mandatory**
- Write a type-annotated function `to_kv` that takes a string `k` and an int or float `v` and returns a tuple with `k` and the square of `v`.

### 8. Complex types - functions
- **Mandatory**
- Write a type-annotated function `make_multiplier` that takes a float `multiplier` and returns a function that multiplies a float by `multiplier`.

### 9. Let's duck type an iterable object
- **Mandatory**
- Annotate the function `element_length`'s parameters and return values with appropriate types.









