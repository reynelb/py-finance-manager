from manager import FinanceManager

def main():
    fm = FinanceManager()
    print("=== Personal Finance Manager ===")

    while True:
        print("\nOptions:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Show Monthly Report")
        print("4. Show Balance")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            amount = float(input("Amount: "))
            category = input("Category: ")
            fm.add_transaction("income", amount, category)
        elif choice == "2":
            amount = float(input("Amount: "))
            category = input("Category: ")
            fm.add_transaction("expense", amount, category)
        elif choice == "3":
            fm.generate_report()
        elif choice == "4":
            fm.show_balance()
        elif choice == "5":
            fm.save_data()
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
