import sqlite3 
import functools
import os
from datetime import datetime

SCRIPT_DIR =os.path.dirname(__file__)
DB_NAME = os.path.join(SCRIPT_DIR, 'users.db')

def with_db_connection(func):
    """Decorator that automatically handles opening and closing a SQLite database connection.
    
    It passes teh connection object as a first argument to the decorated fucntion.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            result = func(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M-%S")
            print(f"[{timestamp}] ERROR: Database error in '{func.__name__}': {e}")
            return None
        finally:
            if conn:
                conn.close()
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DEBUG: Database connection closed.")
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
                pass # User already exists
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: Database setup error: {e}")
    finally:
        if conn:
            conn.close()


@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 


user = get_user_by_id(user_id=1)
print(user)
