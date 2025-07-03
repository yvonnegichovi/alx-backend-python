import mysql.connector
from mysql.connector import Error
import sys
from seed import connect_to_prodev, close_connection

def paginate_users(page_size, offset):
    """
    Fetches a single page of user data from the database.
    This function connects to the database, executes a LIMIT/OFFSET query,
    fetches the results, and then closes the connection.
    It returns a list of user dictionaries for the specified page.
    """
    connection = None
    cursor = None
    rows = []
    try:
        connection = connect_to_prodev()
        if connection is None:
            print("Error: Could not connect to the database for pagination.", file=sys.stderr)
            return []

        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT user_id, name, email, age FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"Database error during paginate_users: {e}", file=sys.stderr)
        return []
    finally:
        if cursor:
            try:
                cursor.fetchall()
            except Error as e:
                print(f"Warning: Error consuming remaining results before closing cursor in paginate_users: {e}", file=sys.stderr)
            finally:
                cursor.close()
        if connection:
            close_connection(connection)


def lazy_pagination(page_size):
    """
    Generator function to lazily load paginated data from the users database.
    It uses the paginate_users function to fetch each page only when needed.
    This function adheres to the requirement of using only one loop.

    Args:
        page_size (int): The number of users to fetch per page.

    Yields:
        list: A list of user dictionaries representing a page of data.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)

        if not page:
            break # Exit the generator

        yield page # Yield the entire page (a list of user dictionaries)

        offset += page_size
