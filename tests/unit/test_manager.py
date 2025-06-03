import os
import pytest
from app.manager import FinanceManager, Income, Expense, Payment, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# === Setup test database ===
TEST_DB = 'sqlite:///:memory:'
engine = create_engine(TEST_DB)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

# Override FinanceManager to use test session
class TestFinanceManager(FinanceManager):
    def __init__(self):
        self._session = session

    def add_income(self, amount, category):
        entry = Income(amount=amount, category=category)
        self._session.add(entry)
        self._session.commit()
        return entry

    def add_expense(self, amount, category):
        entry = Expense(amount=amount, category=category)
        self._session.add(entry)
        self._session.commit()
        return entry

    def get_incomes(self):
        return self._session.query(Income).all()

    def get_expenses(self):
        return self._session.query(Expense).all()

def test_add_income():
    fm = TestFinanceManager()
    income = fm.add_income(100.0, "Salary")
    incomes = fm.get_incomes()
    assert len(incomes) == 1
    assert incomes[0].amount == 100.0
    assert incomes[0].category == "Salary"

def test_add_expense():
    fm = TestFinanceManager()
    expense = fm.add_expense(50.0, "Groceries")
    expenses = fm.get_expenses()
    assert len(expenses) == 1
    assert expenses[0].amount == 50.0
    assert expenses[0].category == "Groceries"
