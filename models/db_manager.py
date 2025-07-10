import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../db/database.db')


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    """Create all necessary tables if they don’t exist."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'user'
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category_id INTEGER,
                sku TEXT,
                price REAL,
                quantity_in_stock INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                change INTEGER,
                reason TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                product_name TEXT NOT NULL
            )
        """)

        conn.commit()
        print("✅ Tables created successfully.")
    finally:
        conn.close()


def insert_dummy_data():
    """Insert default users, categories, and products (if not already present)."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                       ('admin', 'admin123', 'admin'))
        cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                       ('user1', 'user123', 'user'))

        cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", ('Electronics',))
        cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", ('Groceries',))

        cursor.execute("""
            INSERT OR IGNORE INTO products (name, category_id, sku, price, quantity_in_stock) 
            VALUES (?, ?, ?, ?, ?)""",
                       ('Laptop', 1, 'SKU123', 1000.0, 10))
        cursor.execute("""
            INSERT OR IGNORE INTO products (name, category_id, sku, price, quantity_in_stock) 
            VALUES (?, ?, ?, ?, ?)""",
                       ('Apples', 2, 'SKU456', 2.5, 100))

        conn.commit()
        print("✅ Dummy data inserted.")
    finally:
        conn.close()


def log_action(username, action, product_name):
    """Record an action in the logs table."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO logs (username, action, product_name) 
            VALUES (?, ?, ?)
        """, (username, action, product_name))
        conn.commit()
        print(f"🪵 Log saved: {username} - {action} - {product_name}")
    except Exception as e:
        print(f"⚠️ Failed to log action: {e}")
    finally:
        if conn:
            conn.close()


# 👤 User management helpers

def get_all_users():
    """Fetch all users (id, username, role)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


def add_user(username, password, role):
    """Add a new user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, password, role)
    )
    conn.commit()
    conn.close()


def update_user(user_id, password=None, role=None):
    """Update a user's password and/or role."""
    conn = get_connection()
    cursor = conn.cursor()
    if password and role:
        cursor.execute(
            "UPDATE users SET password=?, role=? WHERE id=?",
            (password, role, user_id)
        )
    elif password:
        cursor.execute(
            "UPDATE users SET password=? WHERE id=?",
            (password, user_id)
        )
    elif role:
        cursor.execute(
            "UPDATE users SET role=? WHERE id=?",
            (role, user_id)
        )
    conn.commit()
    conn.close()


def delete_user(user_id):
    """Delete a user by id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    insert_dummy_data()
