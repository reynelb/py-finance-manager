import sys
import os
from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.manager import engine, session, FinanceManager, Income, Expense, Payment, Budget, User

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace for production use

Session = sessionmaker(bind=engine)
db = Session()

# === Flask-Login Setup ===
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class AuthUser(UserMixin):
    def __init__(self, user):
        self.id = str(user.id)
        self.username = user.username

@login_manager.user_loader
def load_user(user_id):
    user = db.query(User).filter_by(id=int(user_id)).first()
    return AuthUser(user) if user else None

fm = FinanceManager()

# === ROUTES ===

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    income = db.query(Income).order_by(Income.date.desc()).all()
    expenses = db.query(Expense).order_by(Expense.date.desc()).all()
    payments = db.query(Payment).all()

    category_summary = defaultdict(float)
    for e in expenses:
        category_summary[e.category] += e.amount

    def format_month(dt): return dt.strftime('%Y-%m')
    monthly_income = defaultdict(float)
    monthly_expenses = defaultdict(float)
    for i in income:
        monthly_income[format_month(i.date)] += i.amount
    for e in expenses:
        monthly_expenses[format_month(e.date)] += e.amount

    all_months = sorted(set(monthly_income) | set(monthly_expenses))
    income_data = [monthly_income[m] for m in all_months]
    expense_data = [monthly_expenses[m] for m in all_months]

    budgets = db.query(Budget).all()
    actual = defaultdict(float)
    for e in expenses:
        actual[(e.category, format_month(e.date))] += e.amount
    budget_warnings = [
        (b.category, b.month, actual.get((b.category, b.month), 0), b.limit)
        for b in budgets if actual.get((b.category, b.month), 0) > b.limit
    ]

    return render_template(
        'index.html',
        income=income,
        expenses=expenses,
        payments=payments,
        category_summary=category_summary,
        months=all_months,
        income_by_month=income_data,
        expense_by_month=expense_data,
        budget_warnings=budget_warnings
    )

@app.route('/add', methods=['POST'])
@login_required
def add():
    t = request.form['type']
    amt = float(request.form['amount'])
    cat = request.form['category']
    fm.add_income(amt, cat) if t == 'income' else fm.add_expense(amt, cat)
    return redirect(url_for('dashboard'))

@app.route('/add_payment', methods=['POST'])
@login_required
def add_payment():
    db.add(Payment(description=request.form['description'], date=request.form['date']))
    db.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_budget', methods=['POST'])
@login_required
def add_budget():
    db.add(Budget(
        category=request.form['category'],
        month=request.form['month'],
        limit=float(request.form['limit'])
    ))
    db.commit()
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if db.query(User).filter_by(username=request.form['username']).first():
            flash("Username already exists.")
            return redirect(url_for('register'))
        new_user = User(username=request.form['username'])
        new_user.set_password(request.form['password'])
        db.add(new_user)
        db.commit()
        flash("Account created. Please log in.")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = db.query(User).filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(AuthUser(user))
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
