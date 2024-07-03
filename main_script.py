import hashlib
from databaseconnections_and_tables import create_connection, close_connection, create_database_and_tables

from funtions import authenticate_user, log_expense, register_user, view_expenses

def login_menu():
    print("Expense Tracker - Login")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    return username, password

def registration_menu():
    print("Expense Tracker - Registration")
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    return username, password

def main_menu():
    print("\nExpense Tracker Menu:")
    print("1. Log Expense")
    print("2. View Expenses")
    print("3. Register")
    print("4. Exit")
    choice = input("Enter your choice (1, 2, 3, or 4): ")
    return choice

def login():
    while True:
        username, password = login_menu()
        authenticated, user_id = authenticate_user(username, password)
        if authenticated:
            print(f"Login successful. Welcome, {username}!")
            return user_id
        else:
            print("Invalid credentials. Please try again.")

def register():
    username, password = registration_menu()
    register_user(username, password)
    print("Registration successful. You can now log in.")

def log_expenses(user_id):
    amount = float(input("Enter the expense amount: "))
    category = input("Enter the expense category: ")
    description = input("Enter a description (optional): ")
    
    # Automatically add the current date
   
    log_expense(user_id, amount, category, description, None)
    print("Expense added successfully!")

def view_expense(user_id):
    category = input("Enter a category to filter (leave blank for all): ")
    start_date = input("Enter the start date for filtering (leave blank for no start date): ")
    end_date = input("Enter the end date for filtering (leave blank for no end date): ")

    view_expenses(user_id, category, start_date, end_date)

def main():
    create_database_and_tables()

    while True:
        choice = main_menu()

        if choice == "1":
            user_id = login()
            if user_id:
                log_expenses(user_id)

        elif choice == "2":
            user_id = login()
            if user_id:
                view_expense(user_id)

        elif choice == "3":
            register()

        elif choice == "4":
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
