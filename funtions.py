import mysql.connector
from datetime import datetime
import hashlib
from databaseconnections_and_tables import create_connection, close_connection, create_database_and_tables
from mysql.connector import Error
from mysql.connector import errorcode


def register_user(username, password):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()

            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()

        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            close_connection(conn)

def authenticate_user(username, password):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()

            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, hashed_password))
            user = cursor.fetchone()
            return user is not None, user[0] if user else None

        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            close_connection(conn)
def create_category(user_id, category_name):
  conn = create_connection()
  if conn:
    try:
      cursor = conn.cursor()
      cursor.execute("INSERT INTO categories (user_id, name) VALUES (%s, %s)", (user_id, category_name))
      conn.commit()
      print(f"Category '{category_name}' created successfully!")
    except mysql.connector.Error as err:
      print(f"Error: {err}")
    finally:
      close_connection(conn)

def log_expense(user_id, amount, category, description, date):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if date is None:
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute('''
                INSERT INTO expenses (user_id, amount, category, description, date)
                VALUES (%s, %s, %s, %s, %s)
            ''', (user_id, amount, category, description, date))
            
            conn.commit()

        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            close_connection(conn)

def view_expenses(user_id, category=None, start_date=None, end_date=None):
    conn = create_connection()
    if conn:
        try:
                        # Start a transaction
            conn.start_transaction()

            cursor = conn.cursor()

            query = "SELECT * FROM expenses WHERE user_id = %s"
            params = [user_id]
#The params list is used to store the values that will be substituted for the placeholders in the query.
#The query is constructed based on the provided parameters. If a category is provided, it is added to the query. If start_date and end_date are provided, they are also added to the query.

            if category:
                query += " AND category = %s"
                params.append(category)

            if start_date:
                query += " AND date >= %s"
                params.append(start_date)

            if end_date:
                query += " AND date <= %s"
                params.append(end_date)

            cursor.execute(query, params)
            expenses = cursor.fetchall()

            for expense in expenses:
                print(expense)
                        # Commit the transaction
            conn.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(f"Error: {err}")
            # Rollback the transaction in case of an error
            conn.rollback()

        finally:
            cursor.close()
            close_connection(conn)
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Continue with the example usage

# Call the create_database_and_tables function to create the database and tables
#create_database_and_tables()

# Example usage
#register_user("user1", "password1")
#authenticated, user_id = authenticate_user("user1", "password1")
#if authenticated:
    # Log an expense
 #    log_expense(user_id, 50.0, "Groceries", "Weekly grocery shopping", datetime.now().strftime("%Y-%m-%d"))
  #   log_expense(user_id, 80.0, "Fuel", "Fuel Filling", datetime.now().strftime("%Y-%m-%d"))
   #  log_expense(user_id, 80.0, "Fueel", "Fuel Filling", datetime.now().strftime("%Y-%m-%d"))
    # log_expense(user_id, 1000.0, "Fueel", "Fuel Filling", datetime.now().strftime("%Y-%m-%d"))

    # View expenses
     #view_expenses(user_id, category="Fueel", start_date="2023-11-01", end_date="2023-11-15")
