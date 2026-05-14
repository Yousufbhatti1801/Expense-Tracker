import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'spendly.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    conn = get_db()
    conn.executescript('''
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
    count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    if count > 0:
        conn.close()
        return

    conn.execute(
        'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
        ('Demo User', 'demo@spendly.com', generate_password_hash('demo123'))
    )
    user_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

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
    conn.executemany(
        'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
        expenses
    )
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    return user


def create_user(name, email, password_hash):
    conn = get_db()
    cursor = conn.execute(
        'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
        (name, email, password_hash)
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id


def get_expenses_by_user(user_id):
    conn = get_db()
    rows = conn.execute(
        'SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC',
        (user_id,)
    ).fetchall()
    conn.close()
    return rows


def get_expense_summary(user_id):
    conn = get_db()
    total = conn.execute(
        'SELECT COALESCE(SUM(amount), 0) AS total FROM expenses WHERE user_id = ?',
        (user_id,)
    ).fetchone()['total']
    by_category = conn.execute(
        'SELECT category, COALESCE(SUM(amount), 0) AS total FROM expenses WHERE user_id = ? GROUP BY category ORDER BY total DESC',
        (user_id,)
    ).fetchall()
    conn.close()
    return {'total': total, 'by_category': by_category}


def add_expense(user_id, amount, category, date, description):
    conn = get_db()
    cursor = conn.execute(
        'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
        (user_id, amount, category, date, description)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def delete_expense(expense_id, user_id):
    conn = get_db()
    cursor = conn.execute(
        'DELETE FROM expenses WHERE id = ? AND user_id = ?',
        (expense_id, user_id)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0
