# app/main.py
from app.manager import FinanceManager
from app.notifier import PaymentNotifier
import time

if __name__ == '__main__':
    fm = FinanceManager()
    notifier = PaymentNotifier(fm)

    while True:
        print("\n=== Personal Finance Manager ===")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Show Report")
        print("4. Upcoming Payments")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            amount = float(input("Enter income amount: "))
            category = input("Enter category: ")
            fm.add_income(amount, category)
        elif choice == '2':
            amount = float(input("Enter expense amount: "))
            category = input("Enter category: ")
            fm.add_expense(amount, category)
        elif choice == '3':
            fm.show_report()
        elif choice == '4':
            notifier.check_payments()
        elif choice == '5':
            break
        else:
            print("Invalid choice")

        time.sleep(1)
