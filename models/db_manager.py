import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../db/database.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )""")

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
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        change INTEGER,
        reason TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(id)
    )""")

    conn.commit()
    conn.close()
    print("✅ Tables created successfully.")

def insert_dummy_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                   ('admin', 'admin123', 'admin'))
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                   ('user1', 'user123', 'user'))

    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", ('Electronics',))
    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", ('Groceries',))

    cursor.execute("INSERT OR IGNORE INTO products (name, category_id, sku, price, quantity_in_stock) VALUES (?, ?, ?, ?, ?)",
                   ('Laptop', 1, 'SKU123', 1000.0, 10))
    cursor.execute("INSERT OR IGNORE INTO products (name, category_id, sku, price, quantity_in_stock) VALUES (?, ?, ?, ?, ?)",
                   ('Apples', 2, 'SKU456', 2.5, 100))

    conn.commit()
    conn.close()
    print("✅ Dummy data inserted.")

if __name__ == "__main__":
    create_tables()
    insert_dummy_data()
