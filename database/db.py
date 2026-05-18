import os
import sqlite3
from datetime import date, timedelta
from werkzeug.security import generate_password_hash

# Detect if we are running on Railway (Postgres) or locally (SQLite)
DATABASE_URL = os.environ.get('DATABASE_URL', '')
IS_POSTGRES = DATABASE_URL.startswith('postgres')

if IS_POSTGRES:
    import psycopg2
    from psycopg2.extras import RealDictCursor

DB_PATH = DATABASE_URL if IS_POSTGRES else os.environ.get(
    'DATABASE_URL',
    os.path.join(os.path.dirname(__file__), '..', 'spendly.db')
)


def get_db():
    if IS_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')
        return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    if IS_POSTGRES:
        # Postgres compatible schema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id            SERIAL PRIMARY KEY,
                name          TEXT    NOT NULL,
                email         TEXT    UNIQUE NOT NULL,
                password_hash TEXT    NOT NULL,
                created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id          SERIAL PRIMARY KEY,
                user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                amount      REAL    NOT NULL,
                category    TEXT    NOT NULL,
                date        DATE    NOT NULL,
                description TEXT,
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
    else:
        # SQLite compatible schema
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT    NOT NULL,
                email         TEXT    UNIQUE NOT NULL,
                password_hash TEXT    NOT NULL,
                created_at    TEXT    DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL REFERENCES users(id),
                amount      REAL    NOT NULL,
                category    TEXT    NOT NULL,
                date        TEXT    NOT NULL,
                description TEXT,
                created_at  TEXT    DEFAULT (datetime('now'))
            );
        ''')
        
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) AS c FROM users')
    count = cursor.fetchone()['c']
    
    if count > 0:
        conn.close()
        return

    if IS_POSTGRES:
        cursor.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s) RETURNING id',
            ('Demo User', 'demo@spendly.com', generate_password_hash('demo123'))
        )
        user_id = cursor.fetchone()['id']
    else:
        cursor.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            ('Demo User', 'demo@spendly.com', generate_password_hash('demo123'))
        )
        user_id = cursor.lastrowid

    expenses = [
        (user_id, 12.50,  'Food',          '2026-05-01', 'Breakfast at cafe'),
        (user_id, 45.00,  'Transport',     '2026-05-03', 'Monthly bus pass top-up'),
        (user_id, 120.00, 'Bills',         '2026-05-05', 'Electricity bill'),
        (user_id, 30.00,  'Health',        '2026-05-07', 'Pharmacy'),
        (user_id, 25.00,  'Entertainment', '2026-05-09', 'Cinema tickets'),
        (user_id, 89.99,  'Shopping',      '2026-05-11', 'New shoes'),
        (user_id, 18.75,  'Food',          '2026-05-13', 'Lunch with colleague'),
        (user_id, 15.00,  'Other',         '2026-05-15', 'Miscellaneous'),
    ]
    
    if IS_POSTGRES:
        cursor.executemany(
            'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (%s, %s, %s, %s, %s)',
            expenses
        )
    else:
        cursor.executemany(
            'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
            expenses
        )
        
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_db()
    cursor = conn.cursor()
    query = 'SELECT * FROM users WHERE email = ?'
    if IS_POSTGRES: query = query.replace('?', '%s')
    
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    conn.close()
    return user


def create_user(name, email, password_hash):
    conn = get_db()
    cursor = conn.cursor()
    
    if IS_POSTGRES:
        cursor.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s) RETURNING id',
            (name, email, password_hash)
        )
        user_id = cursor.fetchone()['id']
    else:
        cursor.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            (name, email, password_hash)
        )
        user_id = cursor.lastrowid
        
    conn.commit()
    conn.close()
    return user_id


def get_expenses_by_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    query = 'SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC'
    if IS_POSTGRES: query = query.replace('?', '%s')
    
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_expense_summary(user_id):
    conn = get_db()
    cursor = conn.cursor()
    
    query_total = 'SELECT COALESCE(SUM(amount), 0) AS total FROM expenses WHERE user_id = ?'
    if IS_POSTGRES: query_total = query_total.replace('?', '%s')
    cursor.execute(query_total, (user_id,))
    total = cursor.fetchone()['total']
    
    query_cat = 'SELECT category, COALESCE(SUM(amount), 0) AS total, COUNT(*) AS count FROM expenses WHERE user_id = ? GROUP BY category ORDER BY total DESC'
    if IS_POSTGRES: query_cat = query_cat.replace('?', '%s')
    cursor.execute(query_cat, (user_id,))
    by_category = cursor.fetchall()
    
    conn.close()
    return {
        'total': total,
        'by_category': [{'category': r['category'], 'total': r['total'], 'count': r['count']} for r in by_category],
    }


def add_expense(user_id, amount, category, date, description):
    conn = get_db()
    cursor = conn.cursor()
    
    if IS_POSTGRES:
        cursor.execute(
            'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (%s, %s, %s, %s, %s) RETURNING id',
            (user_id, amount, category, date, description)
        )
        new_id = cursor.fetchone()['id']
    else:
        cursor.execute(
            'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
            (user_id, amount, category, date, description)
        )
        new_id = cursor.lastrowid
        
    conn.commit()
    conn.close()
    return new_id


def delete_expense(expense_id, user_id):
    conn = get_db()
    cursor = conn.cursor()
    query = 'DELETE FROM expenses WHERE id = ? AND user_id = ?'
    if IS_POSTGRES: query = query.replace('?', '%s')
    
    cursor.execute(query, (expense_id, user_id))
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return success


def get_expense_by_id(expense_id, user_id):
    conn = get_db()
    cursor = conn.cursor()
    query = 'SELECT * FROM expenses WHERE id = ? AND user_id = ?'
    if IS_POSTGRES: query = query.replace('?', '%s')
    
    cursor.execute(query, (expense_id, user_id))
    expense = cursor.fetchone()
    conn.close()
    return expense


def update_expense(expense_id, user_id, amount, category, date, description):
    conn = get_db()
    cursor = conn.cursor()
    query = 'UPDATE expenses SET amount = ?, category = ?, date = ?, description = ? WHERE id = ? AND user_id = ?'
    if IS_POSTGRES: query = query.replace('?', '%s')
    
    cursor.execute(query, (amount, category, date, description, expense_id, user_id))
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return success


def get_category_summary_by_range(user_id, range_filter):
    today = date.today()
    if range_filter == 'yesterday':
        start = (today - timedelta(days=1)).isoformat()
        query = 'SELECT category, COALESCE(SUM(amount), 0) AS total FROM expenses WHERE user_id = ? AND date = ? GROUP BY category ORDER BY total DESC'
    else:
        if range_filter == 'weekly':
            start = (today - timedelta(days=6)).isoformat()
        elif range_filter == '1month':
            start = (today - timedelta(days=29)).isoformat()
        else:  # 6months
            year = today.year
            month = today.month - 5
            if month <= 0:
                month += 12
                year -= 1
            start = date(year, month, 1).isoformat()
        query = 'SELECT category, COALESCE(SUM(amount), 0) AS total FROM expenses WHERE user_id = ? AND date >= ? GROUP BY category ORDER BY total DESC'
    
    if IS_POSTGRES: query = query.replace('?', '%s')
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, (user_id, start))
    rows = cursor.fetchall()
    conn.close()
    
    return [{'category': r['category'], 'total': r['total']} for r in rows]


def get_period_summary_by_range(user_id, range_filter):
    today = date.today()

    if range_filter in ['yesterday', 'weekly', '1month']:
        group_expr = "TO_CHAR(date::DATE, 'YYYY-MM-DD')" if IS_POSTGRES else "strftime('%Y-%m-%d', date)"
    else:
        group_expr = "TO_CHAR(date::DATE, 'YYYY-MM')" if IS_POSTGRES else "strftime('%Y-%m', date)"

    if range_filter == 'yesterday':
        labels = [(today - timedelta(days=1)).isoformat()]
        param = (today - timedelta(days=1)).isoformat()
        date_clause = 'date = ?'
    elif range_filter == 'weekly':
        labels = [(today - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
        param = (today - timedelta(days=6)).isoformat()
        date_clause = 'date >= ?'
    elif range_filter == '1month':
        labels = [(today - timedelta(days=i)).isoformat() for i in range(29, -1, -1)]
        param = (today - timedelta(days=29)).isoformat()
        date_clause = 'date >= ?'
    else:  # 6months
        month_labels = []
        y, m = today.year, today.month
        for _ in range(6):
            month_labels.append(f'{y:04d}-{m:02d}')
            m -= 1
            if m == 0:
                m = 12
                y -= 1
        labels = list(reversed(month_labels))
        param = date(int(labels[0][:4]), int(labels[0][5:7]), 1).isoformat()
        date_clause = 'date >= ?'

    query = f'SELECT {group_expr} AS label, COALESCE(SUM(amount), 0) AS total FROM expenses WHERE user_id = ? AND {date_clause} GROUP BY label ORDER BY label ASC'
    if IS_POSTGRES: query = query.replace('?', '%s')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, (user_id, param))
    rows = cursor.fetchall()
    conn.close()

    db_map = {r['label']: r['total'] for r in rows}
    return [{'label': lbl, 'total': db_map.get(lbl, 0)} for lbl in labels]