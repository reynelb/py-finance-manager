import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

# === Database Setup ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, '..', 'finance.db')
engine = create_engine(f'sqlite:///{os.path.abspath(db_path)}', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# === Models ===
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Income(Base):
    __tablename__ = 'income'
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now)

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now)

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    date = Column(String, nullable=False)  # ISO date string

class Budget(Base):
    __tablename__ = 'budgets'
    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    month = Column(String, nullable=False)  # YYYY-MM
    limit = Column(Float, nullable=False)

# === Create Tables ===
Base.metadata.create_all(engine)

# === Finance Manager ===
class FinanceManager:
    def add_income(self, amount, category):
        entry = Income(amount=amount, category=category)
        session.add(entry)
        session.commit()

    def add_expense(self, amount, category):
        entry = Expense(amount=amount, category=category)
        session.add(entry)
        session.commit()

    def show_report(self):
        income_total = sum(entry.amount for entry in session.query(Income).all())
        expense_total = sum(entry.amount for entry in session.query(Expense).all())
        print("\n--- Financial Report ---")
        print(f"Total Income: {income_total:.2f}")
        print(f"Total Expenses: {expense_total:.2f}")
        print(f"Net Balance: {income_total - expense_total:.2f}")

    def get_upcoming_payments(self):
        return session.query(Payment).all()
