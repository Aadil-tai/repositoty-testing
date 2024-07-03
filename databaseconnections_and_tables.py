import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        # Connect to the MySQL server (replace with your actual credentials)
        abc = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="expense_tracker_db"
        )
        return abc

    except Error as e:
        print(f"Error: {e}")
        return None

def close_connection(conn):
    if conn:
        conn.close()

def create_database_and_tables():
    abc = create_connection()
    if abc:
        try:
            cursor123 = abc.cursor()

            # Create a new database if it doesn't exist
            cursor123.execute("CREATE DATABASE IF NOT EXISTS expense_tracker_db")
            print("Database created successfully.")

            # Switch to the new database
            cursor123.execute("USE expense_tracker_db")

            # Check if the users table exists
            cursor123.execute("SHOW TABLES LIKE 'users'")
            users_table_exists = cursor123.fetchone()

            if not users_table_exists:
                # Create users table if it doesn't exist
                cursor123.execute('''
                    CREATE TABLE users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL
                    )
                ''')
                print("Users table created successfully.")
            else:
                print("Users table already exists.")

            # Check if the expenses table exists
            cursor123.execute("SHOW TABLES LIKE 'expenses'")
            expenses_table_exists = cursor123.fetchone()

            if not expenses_table_exists:
                # Create expenses table if it doesn't exist
                cursor123.execute('''
                    CREATE TABLE expenses (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        amount DECIMAL(10, 2) NOT NULL,
                        category VARCHAR(255) NOT NULL,
                        description TEXT,
                        date DATE NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
                print("Expenses table created successfully.")
            else:
                print("Expenses table already exists.")
            abc.commit()

        except Error as e:
            print(f"Error: {e}")

        finally:
            cursor123.close()
            close_connection(abc)

create_database_and_tables()