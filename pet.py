# ==============================
#     PERSONAL EXPENSE TRACKER
# ==============================
import os
import csv


file_name = "expenses.tsv"

# ==============================
# 1. DISPLAY MENU
# ==============================

def display_menu():
    
    print("\n===== PERSONAL EXPENSE TRACKER =====")
    print("1. Add Transaction")
    print("2. View All Transactions")
    print("3. View Summary")
    print("4. Edit Expense")
    print("5. Delete Transaction")
    print("6. Export Transaction To CSV")
    print("7. Exit")

# ==============================
# 2. ENSURE THE FILE EXISTS
# ==============================
def ensure_file():
    if not os.path.exists(file_name):
        with open(file_name, "w", encoding="utf-8"):
            pass


# ==============================
# 3. LOAD ALL EXPENSES FROM THE FILE
# ==============================
def load_expenses():

    ensure_file() 

    expenses = []

    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:

            #Skip Empty Lines
            if not line.strip():
                continue

            #Separate The five Fields
            fields = line.rstrip("\n").split("\t")
            
            if len(fields) != 5:
                print(f"Invalid expense record: {line!r}")
                continue
            
            expense_id, date, category, amount, note = fields

            # Store each expense as dictionary
            expense = {
                "id" : int(expense_id),
                "date" : date,
                "category" : category,
                "amount" : float(amount),
                "note" : note
            }
            expenses.append(expense)
    return expenses

# ==============================
# 4. CONVERT & VALIDATE THE AMOUNT
# ==============================

def convert_amount(amount_text) :
    try: 
        amount = float(amount_text)

        # Expense must be grater than 0
        if amount <= 0:
            return None
        
        return amount
    
    except ValueError:
        return None

# ==================================
# 5. GENERATE THE NEXT EXPENSE ID
# ==================================

def generate_nxt_id(expenses):
    highest_id = max (
        (expense["id"] for expense in expenses),
        default=0
    )
    return highest_id + 1

# ==============================
# 6. CLEAR THE USER INPUT
# ==============================

def clean_filed(text):
    #Prevent tabs and newlines from breaking the file format
    return text.replace("\t", " ").replace("\n", " ").replace("\r", " ")

# ==============================
# 7. SAVE ALL EXPENSES TO THE FILE
# ==============================


def save_expenses(expenses):
    with open(file_name, "w", encoding="utf-8") as file:
        for expense in expenses:
            line = (
                f"{expense['id']}\t"
                f"{expense['date']}\t"
                f"{expense['category']}\t"
                f"{expense['amount']:.2f}\t"
                f"{expense['note']}\n"
            )
            file.write(line)
# ==============================
# 8. DISPLAY A SINGLE EXPENSE
# ==============================


def display_expense(expense):
    print("-" * 50)
    print(f"ID       : {expense['id']}")
    print(f"Date     : {expense['date']}")
    print(f"Category : {expense['category']}")
    print(f"Amount   : ₹{expense['amount']:.2f}")
    print(f"Note     : {expense['note']}")
    print("-" * 50)

# ==============================
# 9. ADD A NEW EXPENSE
# ==============================


def add_expense():
    expenses = load_expenses()

    date = clean_filed(input("Enter data (YYYY-MM-DD): ").strip())

    category = clean_filed(
        input("Enter category: ").strip()
    )
    if not category:
        category = "Uncategorized"

    amount_text = input("Enter amount in rupees:").strip()

    amount = convert_amount(amount_text)

    if amount is None:
        print("Invalid Amount ! Enter a number greater that 0")
        return
    
    note = clean_filed(input("Enter note:").strip())

    #Created new expense dictionary
    expense = {
        "id": generate_nxt_id(expenses),
        "date": date,
        "category": category,
        "amount": amount,
        "note": note,
    }

    # Add the expense to the list
    expenses.append(expense)

    #Save all expenses
    save_expenses(expenses)

    print("\nExpense saved successfully!")
    display_expense(expense)

# ==============================
# 10. VIEW ALL EXPENSES
# ==============================


def view_all_expenses():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses found.")
        return
    
    print("\n===== ALL EXPENSES =====")

    for expense in expenses:
        display_expense(expense)

# ==============================
# 11. DISPLAY EXPENSE SUMMARY
# ==============================

def view_summary():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses available for summary.")
        return

    total_amount = 0
    category_totals = {}

    for expense in expenses:
        amount = expense["amount"]
        category = expense["category"]

        total_amount += amount

        # Add the amount to its category total
        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    print("\n========= EXPENSE SUMMARY ========")
    print(f"Total Transactions : {len(expenses)}")
    print(f"Total Expenses     : ₹{total_amount:.2f}")  

    print("\nExpenses by Category:")

    for category, amount in category_totals.items():
        print(f"{category}: ₹{amount:.2f}") 

# ==============================
# 12. EDIT EXPENSES
# ==============================

def edit_expenses():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses available to edit")
        return

    try:
        expense_id = int(input("Enter ID to edit: ").strip())
    except ValueError:
        print("Invalid ID.")
        return

    target = 0
    for expense in expenses:
        if expense['id'] == expense_id:
            target = expense
            break

    if not target:
        print(f"No expense with id {expense_id}.")
        return

    print("\nPress enter to keep existing value.")

    edit_date     = input(f"date [{target['date']}]:").strip()
    edit_category = input(f"category [{target['category']}]:").strip()
    edit_amount   = input(f"amount [{target['amount']}]:").strip()
    edit_note     = input(f"note [{target['note']}]:").strip()

    if edit_date:
        target['date'] = clean_filed(edit_date)

    if edit_category:
        target['category'] = clean_filed(edit_category)

    if edit_amount:
        target['amount'] = convert_amount(edit_amount)

    if edit_note:
        target['note'] = clean_filed(edit_note)

    save_expenses(expenses)
    print("\nUpdated expense")
    display_expense(target)


# ==============================
# 13. DELETE EXPENSES
# ==============================

def delete_expenses():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses available to delete")
        return

    try:
        expense_id = int(input("Enter ID to Delete:").strip())
    except ValueError:
        print("Invalid ID")
        return

    new_expenses = [expense for expense in expenses if expense['id'] != expense_id]
    
    if len(new_expenses) == len(expenses):
        print(f"No expense with ID {expense_id}.")
        return

    save_expenses(new_expenses)
    print(f"Deleted expense {expense_id}.")

    

# ==============================
# 14. EXPORT EXPENSES TO CSV
# ============================== 

def export_to_csv():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses available to export.")
        return
    
    csv_file_name = "expenses.csv"

    with open(csv_file_name, "w", newline="", encoding="utf-8") as file:
        field_names = [
            "id",
            "date", 
            "category", 
            "amount", 
            "note"
        ]
        writer = csv.DictWriter(
            file,
            fieldnames=field_names
        )
        writer.writeheader()
        writer.writerows(expenses)

    print("\nExpenses exported successfully to",file_name)

# ==============================
# 15. MAIN PROGRAM
# ==============================         

def main():

    while True:
        display_menu()
        choice = input("Choose an option above from: ").strip()

        match choice:
            case "1": add_expense()
            case "2": view_all_expenses()
            case "3": view_summary()
            case "4": edit_expenses()
            case "5": delete_expenses()
            case "6": export_to_csv()
            case "7": print("Goodbye !"); break
            case _: print("Invalid Choice. Try Again.")

#Start the application
if __name__ == "__main__":
    main()