import sys
import os
from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# === Setup for Module Imports ===
# Append parent directory to system path to import local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.manager import engine, session, FinanceManager, Income, Expense, Payment, Budget, User
from app.notifier import PaymentNotifier

# === Load Environment Variables ===
load_dotenv()

# === Initialize Flask App ===
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # IMPORTANT: Use a secure key in production!

# === Database Setup ===
Session = sessionmaker(bind=engine)
db = Session()

# === Flask-Login Configuration ===
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect unauthorized users to login page

# === Authentication Helper Class ===
class AuthUser(UserMixin):
    def __init__(self, user):
        self.id = str(user.id)
        self.username = user.username

# === User Loader for Flask-Login ===
@login_manager.user_loader
def load_user(user_id):
    user = db.query(User).filter_by(id=int(user_id)).first()
    return AuthUser(user) if user else None

# === Initialize Finance Manager ===
fm = FinanceManager()

# === Routes ===

@app.route('/')
def home():
    return redirect(url_for('login'))

# === Telegram Chat ID Setup ===
@app.route('/set_chat_id', methods=['GET', 'POST'])
@login_required
def set_chat_id():
    user = db.query(User).filter_by(id=int(current_user.id)).first()
    if request.method == 'POST':
        user.telegram_chat_id = request.form['chat_id']
        db.commit()
        flash("Telegram Chat ID saved!")
        return redirect(url_for('dashboard'))
    return render_template('set_chat_id.html', current_chat_id=user.telegram_chat_id or "")

# === Dashboard View ===
@app.route('/dashboard')
@login_required
def dashboard():
    income = db.query(Income).order_by(Income.date.desc()).all()
    expenses = db.query(Expense).order_by(Expense.date.desc()).all()
    payments = db.query(Payment).filter_by(user_id=current_user.id).all()

    # Summarize expenses by category
    category_summary = defaultdict(float)
    for e in expenses:
        category_summary[e.category] += e.amount

    # Aggregate income and expenses by month
    def format_month(dt): return dt.strftime('%Y-%m')
    monthly_income = defaultdict(float)
    monthly_expenses = defaultdict(float)
    for i in income:
        monthly_income[format_month(i.date)] += i.amount
    for e in expenses:
        monthly_expenses[format_month(e.date)] += e.amount

    # Prepare data for chart rendering
    all_months = sorted(set(monthly_income) | set(monthly_expenses))
    income_data = [monthly_income[m] for m in all_months]
    expense_data = [monthly_expenses[m] for m in all_months]

    # Budget warnings
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

# === Add Income or Expense ===
@app.route('/add', methods=['POST'])
@login_required
def add():
    t = request.form['type']
    amt = float(request.form['amount'])
    cat = request.form['category']
    if t == 'income':
        fm.add_income(amt, cat)
    else:
        fm.add_expense(amt, cat)
    return redirect(url_for('dashboard'))

# === Add Payment and Notify if Chat ID Exists ===
@app.route('/add_payment', methods=['POST'])
@login_required
def add_payment():
    user = db.query(User).filter_by(id=int(current_user.id)).first()
    description = request.form['description']
    date = request.form['date']

    db.add(Payment(description=description, date=date, user_id=user.id))
    db.commit()

    if user.telegram_chat_id:
        notifier = PaymentNotifier(fm)
        notifier.send_reminder(f"🔔 New payment '{description}' scheduled for {date}", user.telegram_chat_id)

    return redirect(url_for('dashboard'))

# === Add Budget Limit ===
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

# === User Registration ===
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

# === User Login ===
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

# === User Logout ===
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# === Run Application ===
if __name__ == '__main__':
    app.run(debug=True)
