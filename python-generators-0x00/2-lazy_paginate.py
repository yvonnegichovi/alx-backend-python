import mysql.connector
from mysql.connector import Error
from seed import connect_to_prodev, close_connection

def paginate_users(page_size, offset):
    """
    Fetches a single page of user data from the database.
    """
    connection = None
    cursor = None
    rows = []
    try:
        connection = connect_to_prodev()
        if connection is None:
            return []

        sql_query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(sql_query, (page_size, offset))
        rows = cursor.fetchall()
        return rows
    except Error as e:
        return []
    finally:
        if cursor:
            try:
                cursor.fetchall()
            except Error as e:
            finally:
                cursor.close()
        if connection:
            close_connection(connection)


def lazy_paginate(page_size): # CHANGED NAME from lazy_pagination to lazy_paginate
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
            break

        yield page

        offset += page_size
