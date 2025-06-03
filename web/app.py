# web/app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, redirect, url_for
from app.manager import FinanceManager
from sqlalchemy.orm import sessionmaker
from app.manager import engine, Income, Expense, Payment

app = Flask(__name__)
Session = sessionmaker(bind=engine)
session = Session()
fm = FinanceManager()

from collections import defaultdict

from app.manager import Budget

@app.route('/add_budget', methods=['POST'])
def add_budget():
    category = request.form['category']
    month = request.form['month']
    limit = float(request.form['limit'])
    new_budget = Budget(category=category, month=month, limit=limit)
    session.add(new_budget)
    session.commit()
    return redirect(url_for('index'))

@app.route('/')
def index():
    income = session.query(Income).order_by(Income.date.desc()).all()
    expenses = session.query(Expense).order_by(Expense.date.desc()).all()
    payments = session.query(Payment).all()

    # Pie chart summary (expenses by category)
    category_summary = {}
    for e in expenses:
        category_summary[e.category] = category_summary.get(e.category, 0) + e.amount

    # Bar chart summary (monthly income vs expenses)
    def format_month(dt):
        return dt.strftime('%Y-%m')

    monthly_income = defaultdict(float)
    for entry in income:
        monthly_income[format_month(entry.date)] += entry.amount

    monthly_expenses = defaultdict(float)
    for entry in expenses:
        monthly_expenses[format_month(entry.date)] += entry.amount

    # Ensure both dicts have same months (fill gaps)
    all_months = sorted(set(monthly_income.keys()) | set(monthly_expenses.keys()))
    income_data = [monthly_income[month] for month in all_months]
    expense_data = [monthly_expenses[month] for month in all_months]

    return render_template(
        'index.html',
        income=income,
        expenses=expenses,
        payments=payments,
        category_summary=category_summary,
        months=all_months,
        income_by_month=income_data,
        expense_by_month=expense_data
    )


@app.route('/add', methods=['POST'])
def add():
    entry_type = request.form['type']
    amount = float(request.form['amount'])
    category = request.form['category']
    if entry_type == 'income':
        fm.add_income(amount, category)
    elif entry_type == 'expense':
        fm.add_expense(amount, category)
    return redirect(url_for('index'))

@app.route('/add_payment', methods=['POST'])
def add_payment():
    description = request.form['description']
    date = request.form['date']  # ISO string: YYYY-MM-DD
    new_payment = Payment(description=description, date=date)
    session.add(new_payment)
    session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
