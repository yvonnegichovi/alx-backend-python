import mysql.connector
from mysql.connector import Error
import csv
import uuid

DB_NAME = "ALX_prodev"

def connect_db():
    """Connect to MYSQL server"""
    try:
        return mysql.connector.connect(
                host="localhost",
                user="root",
                password="new_password"
        )
    except Error as e:
        print(f"Connection error: {e}")
        return None

def create_database(connection):
    """Create database ALX_prodev if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database {DB_NAME} created or already exists.")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")

def connect_to_prodev():
    """Connect to ALX_prodev database"""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="new_password",
            database=DB_NAME
        )
    except Error as e:
        print(f"Connection error: {e}")
        return None

def create_table(connection):
    """Create the user_data table"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(5, 2) NOT NULL # Changed DECIMAL to DECIMAL(5,2) for better precision control
            )
        """)
        connection.commit()
        print("Table user_data created successfully or already exists.")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")

def insert_data(connection, csv_file):
    """Insert data from CSV file into user_data table if it doesn't already exist."""
    try:
        cursor = connection.cursor()
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            inserted_count = 0
            for row in reader:
                # Check if a record with the same email already exists
                cursor.execute("SELECT user_id FROM user_data WHERE email = %s", (row['email'],))
                if cursor.fetchone() is None:
                    user_id = str(uuid.uuid4()) # Generate a new UUID for each new entry
                    name = row['name']
                    email = row['email']
                    age = float(row['age']) # Convert age to float for DECIMAL type
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, name, email, age))
                    inserted_count += 1
            connection.commit()
            print(f"Successfully inserted {inserted_count} new records from {csv_file}.")
        cursor.close()
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
    except Error as e:
        print(f"Error inserting data: {e}")

def stream_user_data(connection):
    """
    Generator function to stream user data from the database one row at a time.
    Yields each row as a dictionary.
    """
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        while True:
            row = cursor.fetchone()
            if row is None:
                break # No more rows to fetch
            yield row
    except Error as e:
        print(f"Error streaming data: {e}")
    finally:
        if cursor:
            cursor.close()

def close_connection(connection):
    """
    Closes the database connection if it's open.
    """
    if connection and connection.is_connected():
        connection.close()
        print("Database connection closed.")
