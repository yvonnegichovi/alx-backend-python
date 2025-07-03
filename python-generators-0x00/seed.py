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
        print(f"Connection error {e}")
        return None

def create_database(connection):
    """Create database ALX_prodev if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXIST {DB_NAME}")
        cursor.close()
    except Error as e:
        print(f"Error creating database {e}")

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
                age DECIMAL NOT NULL
            )
        """)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")

def insert_data(connection, csv_file):
    """Insert data from CSV file"""
    try:
        cursor = connection.cursor()
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Ensure UUID is consistent format
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']
                cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, name, email, age))
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
