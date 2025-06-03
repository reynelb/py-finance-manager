# web/app.py
from flask import Flask, render_template, request, redirect, url_for
from manager import FinanceManager

app = Flask(__name__)
fm = FinanceManager()

@app.route('/')
def index():
    income = fm.data['income']
    expenses = fm.data['expenses']
    payments = fm.get_upcoming_payments()
    return render_template('index.html', income=income, expenses=expenses, payments=payments)

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

if __name__ == '__main__':
    app.run(debug=True)
