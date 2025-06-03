# manager.py
import json
import os
from datetime import datetime

class FinanceManager:
    def __init__(self, data_file='data.json'):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(self.data_file):
            return {"income": [], "expenses": [], "payments": []}
        with open(self.data_file, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        # Ensure all expected keys are present
        for key in ["income", "expenses", "payments"]:
            if key not in data:
                data[key] = []
        return data

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_income(self, amount, category):
        self.data['income'].append({
            "amount": amount,
            "category": category,
            "date": datetime.now().isoformat()
        })
        self.save_data()
        print("Income added.")

    def add_expense(self, amount, category):
        self.data['expenses'].append({
            "amount": amount,
            "category": category,
            "date": datetime.now().isoformat()
        })
        self.save_data()
        print("Expense added.")

    def show_report(self):
        income_total = sum(item['amount'] for item in self.data['income'])
        expense_total = sum(item['amount'] for item in self.data['expenses'])
        print("\n--- Financial Report ---")
        print(f"Total Income: {income_total:.2f}")
        print(f"Total Expenses: {expense_total:.2f}")
        print(f"Net Balance: {income_total - expense_total:.2f}")

    def get_upcoming_payments(self):
        return self.data.get('payments', [])
