import time
import sqlite3 
import functools
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(__file__)
DB_NAME = os.path.join(SCRIPT_DIR, 'users.db')
_failure_counter = 0
_MAX_FAILURES = 2 

def with_db_connection(func):
    """
    Decorator that automatically handles opening and closing a SQLite database connection.
    
    It passes the connection object as the first argument to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            result = func(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] ERROR: Database error in '{func.__name__}': {e}")
            raise
        finally:
            if conn:
                conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries the decorated function a specified number of times if it raises an exception.

    Args:
        retries (int): The maximum number of times to retry the function.
        delay (int): The delay in seconds between retries.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{timestamp}] WARNING: Attempt {attempt}/{retries} for '{func.__name__}' failed: {e}")
                    if attempt < retries:
                        time.sleep(delay)
                    else:
                        print(f"[{timestamp}] ERROR: All {retries} attempts for '{func.__name__}' failed. Re-raising last exception.")
                        raise # Re-raise the last exception after all retries are exhausted
        return wrapper
    return decorator

def setup_database(db_name=DB_NAME):
    """
    Sets up the SQLite database: creates the users table and inserts sample data.
    Ensures the database exists and has some data for testing.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        
        users_to_insert = [
            (1, 'Alice Smith', 'alice@example.com'),
            (2, 'Bob Johnson', 'bob@example.com'),
            (3, 'Charlie Brown', 'charlie@example.com')
        ]
        
        for user_data in users_to_insert:
            try:
                cursor.execute("INSERT INTO users (id, name, email) VALUES (?, ?, ?)", user_data)
            except sqlite3.IntegrityError:
                pass # User already exists, ignore
        
        conn.commit()
    except sqlite3.Error as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ERROR: Database setup error: {e}")
        raise
    finally:
        if conn:
            conn.close()

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    """
    Attempts to fetch all users from the database.
    Includes a simulated transient failure for testing the retry decorator.
    """
    global _failure_counter
    
    if _failure_counter < _MAX_FAILURES:
        _failure_counter += 1
        raise sqlite3.OperationalError(f"Simulated transient error on attempt {_failure_counter}")
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


users = fetch_users_with_retry()
print(users)