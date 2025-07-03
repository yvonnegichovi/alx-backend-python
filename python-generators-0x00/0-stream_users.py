import mysql.connector
from mysql.connector import Error
from seed import connect_to_prodev, close_connection

def stream_users():
    """
    Generator function to fetch rows one by one from the user_data table.
    It connects to the ALX_prodev database and yields each row as a dictionary.
    This function uses a single loop for fetching data.
    """
    connection = None
    cursor = None
    try:
        connection = connect_to_prodev()
        if connection is None:
            print("Error: Could not connect to the ALX_prodev database.")
            return

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row

    except Error as e:
        print(f"Database error during streaming: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_connection(connection)
