import time
import sqlite3 
import functools
import os
from datetime import datetime


query_cache = {}

SCRIPT_DIR = os.path.dirname(__file__)
DB_NAME = os.path.join(SCRIPT_DIR, 'users.db')

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

def cache_query(func):
    """
    Decorator that caches the results of a database query based on the SQL query string.

    Assumes the decorated function's first argument (after 'conn') is the SQL query string,
    and that this query string uniquely identifies the result to be cached.
    """
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        cache_key = (query, tuple(args), tuple(sorted(kwargs.items())))
        
        if cache_key in query_cache:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] INFO: CACHE HIT for query: '{query[:50]}...'")
            return query_cache[cache_key]
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] INFO: CACHE MISS for query: '{query[:50]}...'. Fetching from database.")
            
            result = func(conn, query, *args, **kwargs)
            
            query_cache[cache_key] = result
            return result
    return wrapper

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
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    time.sleep(0.1)
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")