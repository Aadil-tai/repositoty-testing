from aifc import Error
import mysql.connector
from databaseconnections_and_tables import create_connection, close_connection
def modify_foreign_key():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()

            # Drop the existing foreign key constraint
            cursor.execute("ALTER TABLE expenses DROP FOREIGN KEY expenses_ibfk_1")

            # Add the new foreign key constraint with the SET NULL option
            cursor.execute("""
                ALTER TABLE expenses
                ADD CONSTRAINT expenses_user_id_fk
                FOREIGN KEY (user_id) REFERENCES users(id)
                ON DELETE SET NULL
            """)

            conn.commit()
            print("Foreign key constraint modified successfully.")

        except Error as e:
            print(f"Error: {e}")
            conn.rollback()

        finally:
            cursor.close()
            close_connection(conn)

if __name__ == "__main__":
    modify_foreign_key()