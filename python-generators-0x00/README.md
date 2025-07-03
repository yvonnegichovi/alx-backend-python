# Python Generators - Task 0

This task sets up a MySQL database and populates it with sample data using a CSV file. It demonstrates basic database connectivity, table creation, and insertion logic using Python and `mysql-connector-python`.

## Key Features
- Creates a database `ALX_prodev`
- Creates `user_data` table
- Loads sample data from `user_data.csv` using UUID as primary key
- Ensures no duplicate entries based on email

## Requirements
- MySQL running locally
- MySQL user/password with privileges
- Python 3.x
- Install required package:
  ```bash
  pip install mysql-connector-python

