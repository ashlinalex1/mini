import csv
import pandas as pd
import datetime
import matplotlib.pyplot as plt

FILENAME = 'expenses.csv'
CATEGORY_FILE = 'categories.csv'

# Initialize the category file if it doesn't exist
def initialize_categories():
    try:
        with open(CATEGORY_FILE, 'x') as file:
            writer = csv.writer(file)
            writer.writerow(['Food', 'Transport', 'Entertainment', 'Utilities'])
    except FileExistsError:
        pass

# Get the list of categories
def get_categories():
    try:
        with open(CATEGORY_FILE, 'r') as file:
            categories = list(csv.reader(file))[0]
        return categories
    except FileNotFoundError:
        return []

# Add a new category to the category file
def add_category(new_category):
    categories = get_categories()
    if new_category not in categories:
        with open(CATEGORY_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([new_category])
        print(f"Category '{new_category}' added successfully!")
    else:
        print(f"Category '{new_category}' already exists.")

# Validate the date format
def validate_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Main menu
def main_menu():
    print("\nExpense Tracker")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Edit Expense")
    print("4. Delete Expense")
    print("5. Generate Report")
    print("6. Exit")
    choice = input("Choose an option: ")
    return choice

# Add an expense
def add_expense():
    initialize_categories()
    while True:
        date = input("Enter date (YYYY-MM-DD): ")
        if not validate_date(date):
            print("Invalid date format. Please try again.")
            continue
        
        # Get available categories
        categories = get_categories()
        print("\nAvailable categories:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        print(f"{len(categories) + 1}. Add new category")
        
        category_choice = int(input("Choose a category: "))
        if category_choice == len(categories) + 1:
            new_category = input("Enter new category: ").strip()
            add_category(new_category)
            category = new_category
        else:
            category = categories[category_choice - 1]
        
        description = input("Enter description: ")
        try:
            amount = float(input("Enter amount: "))
        except ValueError:
            print("Invalid amount. Please enter a number.")
            continue

        with open(FILENAME, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, description, amount])

        print("Expense added successfully!")
        another = input("Do you want to add another expense? (yes/no): ").strip().lower()
        if another != 'yes':
            break

# View expenses
def view_expenses():
    try:
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            print("\nDate\t\tCategory\t\tDescription\t\t\tAmount")
            print("-" * 100)
            for row in reader:
                print(f"{row[0]}\t\t{row[1]}\t\t{row[2]}\t\t{row[3]}")
    except FileNotFoundError:
        print("No expenses found. Please add some first.")

# Edit an expense
def edit_expense():
    view_expenses()
    date_to_edit = input("Enter the date of the expense you want to edit (YYYY-MM-DD): ")

    try:
        with open(FILENAME, 'r') as file:
            rows = list(csv.reader(file))

        with open(FILENAME, 'w', newline='') as file:
            writer = csv.writer(file)
            edited = False
            for row in rows:
                if row[0] == date_to_edit:
                    new_category = input(f"Enter new category (current: {row[1]}): ")
                    new_description = input(f"Enter new description (current: {row[2]}): ")
                    new_amount = input(f"Enter new amount (current: {row[3]}): ")
                    writer.writerow([row[0], new_category, new_description, new_amount])
                    edited = True
                else:
                    writer.writerow(row)

            if edited:
                print("Expense updated successfully!")
            else:
                print("No expense found for the given date.")
    except FileNotFoundError:
        print("No expenses found. Please add some first.")

# Delete an expense
def delete_expense():
    view_expenses()
    date_to_delete = input("Enter the date of the expense you want to delete (YYYY-MM-DD): ")

    try:
        with open(FILENAME, 'r') as file:
            rows = list(csv.reader(file))

        with open(FILENAME, 'w', newline='') as file:
            writer = csv.writer(file)
            deleted = False
            for row in rows:
                if row[0] != date_to_delete:
                    writer.writerow(row)
                else:
                    deleted = True

            if deleted:
                print("Expense deleted successfully!")
            else:
                print("No expense found for the given date.")
    except FileNotFoundError:
        print("No expenses found. Please add some first.")

# Generate a report
def generate_report():
    try:
        df = pd.read_csv(FILENAME, names=['Date', 'Category', 'Description', 'Amount'])
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        report = df.groupby('Category')['Amount'].sum()

        print("\nGenerating report...")
        plt.figure(figsize=(8, 6))
        report.plot.pie(
            autopct='%1.1f%%', startangle=90, title='Expense Distribution', ylabel='')
        plt.show()
    except FileNotFoundError:
        print("No expenses found. Please add some first.")

# Main program
if __name__ == "__main__":
    initialize_categories()
    while True:
        choice = main_menu()
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            edit_expense()
        elif choice == '4':
            delete_expense()
        elif choice == '5':
            generate_report()
        elif choice == '6':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
