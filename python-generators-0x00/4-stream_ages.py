import mysql.connector
from mysql.connector import Error
import sys
from decimal import Decimal # To handle Decimal types from the database
from seed import connect_to_prodev, close_connection # Import database connection utilities

def stream_user_ages():
    """
    Generator function that yields user ages one by one from the user_data table.
    This function establishes a database connection and streams ages efficiently.
    It uses one loop for fetching data.
    """
    connection = None
    cursor = None
    try:
        connection = connect_to_prodev()
        if connection is None:
            print("Error: Could not connect to the ALX_prodev database to stream ages.", file=sys.stderr)
            return # Exit the generator if connection fails

        cursor = connection.cursor(dictionary=True) # Fetch rows as dictionaries
        cursor.execute("SELECT age FROM user_data") # Select only the age column

        # Loop 1: Fetches and yields ages one by one
        while True:
            row = cursor.fetchone()
            if row is None:
                break # No more rows to fetch

            age = row['age']
            # Ensure age is a numeric type (int or float) for calculation
            # It might come as Decimal from the database, convert if necessary
            if isinstance(age, Decimal):
                yield float(age) # Convert Decimal to float for consistent calculations
            else:
                yield float(age) # Ensure it's float if it's already int/float

    except Error as e:
        print(f"Database error during age streaming: {e}", file=sys.stderr)
    finally:
        if cursor:
            try:
                # Consume any remaining unread results to prevent "Unread result found" error
                cursor.fetchall()
            except Error as e:
                print(f"Warning: Error consuming remaining results before closing cursor in stream_user_ages: {e}", file=sys.stderr)
            finally:
                cursor.close()
        if connection:
            close_connection(connection)


def calculate_average_age():
    """
    Calculates the average age of users by consuming the stream_user_ages() generator.
    This function processes ages without loading the entire dataset into memory.
    It uses one loop.
    """
    total_age = 0.0
    user_count = 0

    # Loop 2: Iterates over ages yielded by the stream_user_ages generator
    for age in stream_user_ages():
        total_age += age
        user_count += 1

    if user_count > 0:
        average_age = total_age / user_count
        print(f"Average age of users: {average_age:.2f}") # Format to 2 decimal places
    else:
        print("No user data found to calculate average age.")


if __name__ == "__main__":
    # This block ensures calculate_average_age() is called when the script is executed directly.
    # It will not run when the module is imported by a checker.
    calculate_average_age()
