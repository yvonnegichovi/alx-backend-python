import sqlite3
import functools


def log_queries(func):
    """Log database queries executed by any function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper for the function"""
        query = args[0] if args else "No query provided"
        print(f"LOG: Executing query: '{query}'")
        result = func(*args, **kwargs)
        return result
    return wrapper

conn_setup = sqlite3.connect('user.db')
cursor_setup =conn_setup.cursor()
cursor_setup.execute('''
        CREATE TABLE IF NOT EXISTS users (
