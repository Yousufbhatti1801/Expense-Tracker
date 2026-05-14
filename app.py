import functools
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import init_db, seed_db, get_user_by_email, create_user, get_expenses_by_user, get_expense_summary, add_expense

app = Flask(__name__)
app.secret_key = 'dev-secret-key'  # TODO: load from env var in production


@app.template_filter('currency')
def currency_filter(value):
    return f'Rs {value:,.2f}'


def login_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper


@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not all([name, email, password, confirm_password]):
            flash('All fields are required.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        if get_user_by_email(email):
            flash('An account with that email already exists.', 'error')
            return render_template('register.html')

        create_user(name, email, generate_password_hash(password))
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        user = get_user_by_email(email)
        # Generic message for both unknown email and wrong password — prevents user enumeration
        if not user or not check_password_hash(user['password_hash'], password):
            flash('Invalid email or password.', 'error')
            return render_template('login.html')

        session['user_id'] = user['id']
        session['user_name'] = user['name']
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    expenses = get_expenses_by_user(user_id)
    summary = get_expense_summary(user_id)
    return render_template('dashboard.html', expenses=expenses, summary=summary)


EXPENSE_CATEGORIES = ['Food', 'Transport', 'Shopping', 'Entertainment', 'Health', 'Bills', 'Other']


@app.route('/expenses/add', methods=['GET', 'POST'])
@login_required
def add_expense_view():
    errors = {}

    if request.method == 'POST':
        raw_amount = request.form.get('amount', '').strip()
        category = request.form.get('category', '').strip()
        date_str = request.form.get('date', '').strip()
        description = request.form.get('description', '').strip() or None

        amount = None
        if not raw_amount:
            errors['amount'] = 'Amount is required.'
        else:
            try:
                amount = float(raw_amount)
                if amount <= 0:
                    errors['amount'] = 'Amount must be greater than zero.'
            except ValueError:
                errors['amount'] = 'Amount must be a valid number.'

        if category not in EXPENSE_CATEGORIES:
            errors['category'] = 'Please select a valid category.'

        if not date_str:
            errors['date'] = 'Date is required.'
        else:
            try:
                parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                if parsed_date > datetime.today().date():
                    errors['date'] = 'Date cannot be in the future.'
            except ValueError:
                errors['date'] = 'Date must be in YYYY-MM-DD format.'

        if not errors:
            add_expense(session['user_id'], amount, category, date_str, description)
            flash('Expense added.', 'success')
            return redirect(url_for('dashboard'))

        return render_template('add_expense.html', categories=EXPENSE_CATEGORIES, errors=errors, form=request.form)

    return render_template('add_expense.html', categories=EXPENSE_CATEGORIES, errors={}, form={})


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))


if __name__ == '__main__':
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
