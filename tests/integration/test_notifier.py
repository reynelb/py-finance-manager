from datetime import datetime, timedelta
import pytest
from app.manager import Base, Payment
from app.notifier import PaymentNotifier
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from io import StringIO
import sys

# === Setup in-memory test DB ===
TEST_DB = 'sqlite:///:memory:'
engine = create_engine(TEST_DB)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

# Dummy FinanceManager using the test session
class DummyFinanceManager:
    def get_upcoming_payments(self):
        return session.query(Payment).all()

def test_payment_notifier_shows_upcoming_payment(capsys):
    today = datetime.now().date()
    upcoming_date = (today + timedelta(days=2)).isoformat()
    payment = Payment(description="Credit Card", date=upcoming_date)
    session.add(payment)
    session.commit()

    manager = DummyFinanceManager()
    notifier = PaymentNotifier(manager)
    notifier.check_payments()

    captured = capsys.readouterr()
    assert "Upcoming Payments" in captured.out
    assert "Credit Card" in captured.out
    assert upcoming_date in captured.out

def test_payment_notifier_no_upcoming(capsys):
    today = datetime.now().date()
    far_date = (today + timedelta(days=10)).isoformat()
    payment = Payment(description="Rent", date=far_date)
    session.add(payment)
    session.commit()

    manager = DummyFinanceManager()
    notifier = PaymentNotifier(manager)
    notifier.check_payments()

    captured = capsys.readouterr()
    assert "No upcoming payments" in captured.out
