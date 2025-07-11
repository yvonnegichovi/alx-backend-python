import sqlite3 
import functools
import os
from datetime import datetime

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

def transactional(func):
    """
    Decorator that manages database transactions.
    
    It ensures that the decorated function's database operations are wrapped in a transaction.
    If the functions raises an error, the transaction is rolled back; otherwise, it's commited.
    Assumes teh first argument passed to the decorated function is a database connection object.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            conn.execute("BEGIN TRANSACTION")
            result = func(conn, *args, **kwargs)
            conn.commit()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO: Transaction committed successful")
            return result
        except Exception as e:
            if conn:
                conn.rollback()
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: Transaction rolled back successfully")
            raise
    return wrapper

def setup_database(db_name=DB_NAME):
    """
    Sets up the SQLite database: creates the users table and inserts sample data.
    Ensures the database exists and has some data for testing.
    """
    conn = None
    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DEBUG: Setting up DB at: {db_name}") # Optional debug print
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
                pass
        
        conn.commit()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DEBUG: Database setup complete.") # Optional debug print
    except sqlite3.Error as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ERROR: Database setup error: {e}")
        raise
    finally:
        if conn:
            conn.close()

"""your code goes here"""

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')