import sqlite3
import functools
import os
from datetime import datetime

DB_NAME = 'users.db'

def log_queries(func):
    """Log database queries executed by any function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper for the function"""
        query = "No query provided"

        if 'query' in kwargs:
            query = kwargs['query']
        elif args:
            query = args[0]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] LOG: Executing query: '{query}'")
        print(f"LOG: Executing query: '{query}'")
        result = func(*args, **kwargs)
        return result
    return wrapper

def setup_database(db_name=DB_NAME):
    """
    Sets up the SQLite database: creates the users table and inserts sample data.
    """
    conn = None
    try: 
        db_full_path = os.path.join(os.getcwd(), db_name)
        print(f"DEBUG: Attempting to connect to/create database at: {db_full_path}")
        
        conn = sqlite3.connect(db_full_path)
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
        print(f"DEBUG: Database '{db_name}' setup complete with 'users' table and sample data.")
    except sqlite3.Error as e:
        print(f"ERROR: Database setup error: {e}")
    finally:
        if conn:
            conn.close()


@log_queries
def fetch_all_users(query):
    """
    Connects to the users.db, executes the given query, and returns all results.
    
    This function is decorated by log_queries.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    setup_database()

    print("\n--- Fetching all users ---")
    users = fetch_all_users(query="SELECT * FROM users")
    print("Fetched users:")
    for user in users:
        print(user)

    print("\n--- Fetching a specific user ---")
    user_bob = fetch_all_users(query="SELECT * FROM users WHERE name = 'Bob Johnson'")
    print("Fetched specific user:")
    for user in user_bob:
        print(user)

    print("\n--- Testing with a positional argument for query ---")
    user_charlie = fetch_all_users("SELECT * FROM users WHERE name = 'Charlie Brown'")
    print("Fetched specific user (positional):")
    for user in user_charlie:
        print(user)