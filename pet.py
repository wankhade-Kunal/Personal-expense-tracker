# ==============================
#     PERSONAL EXPENSE TRACKER
# ==============================
import os
import csv


fileName = "expenses.tsv"

# ==============================
# 1. DISPLAY MENU
# ==============================

def displayMenu():
    
    print("\n===== PERSONAL EXPENSE TRACKER =====")
    print("1. Add Transaction")
    print("2. View All Transactions")
    print("3. View Summary")
    print("4. Delete Transaction")
    print("5. Export Transaction To CSV")
    print("6. Exit")

# ==============================
# 2. ENSURE THE FILE EXISTS
# ==============================
def ensureFile():
    if not os.path.exists(fileName):
        with open(fileName, "w", encoding="utf-8"):
            pass


# ==============================
# 3. LOAD ALL EXPENSES FROM THE FILE
# ==============================
def loadExpenses():

    ensureFile() 

    expenses = []

    with open(fileName, "r", encoding="utf-8") as file:
        for line in file:

            #Skip Empty Lines
            if not line.strip():
                continue

            #Separate The five Fields
            fields = line.rstrip("\n").split("\t")
            
            if len(fields) != 5:
                print(f"Invalid expense record: {line!r}")
                continue
            
            expenseId, date, category, amount, note = fields

            # Store each expense as dictionary
            expense = {
                "id" : int(expenseId),
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

def convertAmount(amountText) :
    try: 
        amount = float(amountText)

        # Expense must be grater than 0
        if amount <= 0:
            return None
        
        return amount
    
    except ValueError:
        return None

# ==================================
# 5. GENERATE THE NEXT EXPENSE ID
# ==================================

def generateNxtId(expenses):
    highestId = max (
        (expense["id"] for expense in expenses),
        default=0
    )
    return highestId + 1

# ==============================
# 6. CLEAR THE USER INPUT
# ==============================

def cleanField(text):
    #Prevent tabs and newlines from breaking the file format
    return text.replace("\t", " ").replace("\n", " ").replace("\r", " ")

# ==============================
# 7. SAVE ALL EXPENSES TO THE FILE
# ==============================


def saveExpenses(expenses):
    with open(fileName, "w", encoding="utf-8") as file:
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


def displayExpense(expense):
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


def addExpense():
    expenses = loadExpenses()

    date = cleanField(input("Enter data (YYYY-MM-DD): ").strip())

    category = cleanField(
        input("Enter category: ").strip()
    )
    if not category:
        category = "Uncategorized"

    amountText = input("Enter amount in rupees:").strip()

    amount = convertAmount(amountText)

    if amount is None:
        print("Invalid Amount ! Enter a number greater that 0")
        return
    
    note = cleanField(input("Enter note:").strip())

    #Created new expense dictionary
    expense = {
        "id": generateNxtId(expenses),
        "date": date,
        "category": category,
        "amount": amount,
        "note": note,
    }

    # Add the expense to the list
    expenses.append(expense)

    #Save all expenses
    saveExpenses(expenses)

    print("\nExpense saved successfully!")
    displayExpense(expense)

# ==============================
# 10. VIEW ALL EXPENSES
# ==============================


def viewAllExpenses():
    expenses = loadExpenses()

    if not expenses:
        print("\nNo expenses found.")
        return
    
    print("\n===== ALL EXPENSES =====")

    for expense in expenses:
        displayExpense(expense)

# ==============================
# 11. DISPLAY EXPENSE SUMMARY
# ==============================

def viewSummary():
    expenses = loadExpenses()

    if not expenses:
        print("\nNo expenses available for summary.")
        return

    totalAmount = 0
    categoryTotals = {}

    for expense in expenses:
        amount = expense["amount"]
        category = expense["category"]

        totalAmount += amount

        # Add the amount to its category total
        if category in categoryTotals:
            categoryTotals[category] += amount
        else:
            categoryTotals[category] = amount

    print("\n========= EXPENSE SUMMARY ========")
    print(f"Total Transactions : {len(expenses)}")
    print(f"Total Expenses     : ₹{totalAmount:.2f}")  

    print("\nExpenses by Category:")

    for category, amount in categoryTotals.items():
        print(f"{category}: ₹{amount:.2f}") 

# ==============================
# 12. EXPORT EXPENSES TO CSV
# ============================== 

def exportToCsv():
    expenses = loadExpenses()

    if not expenses:
        print("\nNo expenses available to export.")
        return
    
    csvFileName = "expenses.csv"

    with open(csvFileName, "w", newline="", encoding="utf-8") as file:
        fieldNames = [
            "id",
            "date", 
            "category", 
            "amount", 
            "note"
        ]
        writer = csv.DictWriter(
            file,
            fieldnames=fieldNames
        )
        writer.writeheader()
        writer.writerows(expenses)

    print("\nExpenses exported successfully to {csvFileName}")

# ==============================
# 13. MAIN PROGRAM
# ==============================         

def main():

    while True:
        displayMenu()
        choice = input("Choose an option above from: ").strip()

        match choice:
            case "1": addExpense()
            case "2": viewAllExpenses()
            case "3": viewSummary()
            case "4": print("Delete Transaction: Not implemented yet.")
            case "5": exportToCsv()
            case "6": print("Goodbye !"); break
            case _: print("Invalid Choice. Try Again.")

#Start the application
if __name__ == "__main__":
    main()