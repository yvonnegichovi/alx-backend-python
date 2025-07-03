import mysql.connector
from mysql.connector import Error
from seed import connect_to_prodev, close_connection
import sys
from decimal import Decimal # Import Decimal to handle age comparison correctly

def stream_users_in_batches(batch_size):
    """
    Generator function to fetch rows from the user_data table in specified batch sizes.
    It connects to the ALX_prodev database and yields lists of rows (batches).
    This function uses one loop.
    """
    connection = None
    cursor = None
    try:
        connection = connect_to_prodev()
        if connection is None:
            print("Error: Could not connect to the ALX_prodev database.", file=sys.stderr)
            return

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except Error as e:
        print(f"Database error during batch streaming: {e}", file=sys.stderr)
    finally:
        if cursor:
            try:
                cursor.fetchall()
            except Error as e:
                print(f"Warning: Error consuming remaining results before closing cursor: {e}", file=sys.stderr)
            finally:
                cursor.close()
        if connection:
            close_connection(connection)

def batch_processing(batch_size):
    """
    Generator function that processes users in batches.
    It fetches batches using stream_users_in_batches and then filters
    users whose age is greater than 25.
    This function uses two loops (one for batches, one for users within a batch).
    """
    processed_count = 0
    filtered_count = 0
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            processed_count += 1
            if isinstance(user['age'], Decimal):
                if user['age'] > Decimal('25'):
                    print(user) # Print the user directly as per the expected output
                    filtered_count += 1
            elif isinstance(user['age'], (int, float)):
                if user['age'] > 25:
                    print(user) # Handle cases where age might be int/float if not Decimal
                    filtered_count += 1
            # else:
            #     print(f"DEBUG: User {user['user_id']} has unexpected age type: {type(user['age'])}", file=sys.stderr)

    print(f"DEBUG: Finished batch processing. Total users processed: {processed_count}, Filtered users (age > 25): {filtered_count}", file=sys.stderr)

