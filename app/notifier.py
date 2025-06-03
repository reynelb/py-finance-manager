# app/notifier.py
from datetime import datetime, timedelta
from app.manager import FinanceManager

class PaymentNotifier:
    def __init__(self, manager: FinanceManager):
        self.manager = manager

    def check_payments(self):
        upcoming = []
        today = datetime.now().date()
        for payment in self.manager.get_upcoming_payments():
            try:
                due_date = datetime.fromisoformat(payment.date).date()
                if 0 <= (due_date - today).days <= 3:
                    upcoming.append(payment)
            except Exception:
                continue
        if upcoming:
            print("\n--- Upcoming Payments ---")
            for pay in upcoming:
                print(f"{pay.description} due on {pay.date}")
        else:
            print("No upcoming payments in the next 3 days.")