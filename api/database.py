import sqlite3


DATABASE = "finpay.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL,
            currency TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT UNIQUE NOT NULL,
                from_user TEXT NOT NULL,
                to_user TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT NOT NULL,
                status TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def seed_database():
    connection = get_db_connection()

    cursor = connection.cursor()

    users = [
        ("Alice", "Alice", 1000, "USD", "Customer"),
        ("Bob", "Bob", 500, "USD", "Customer"),
        ("Admin", "Admin", None, "USD", "Administrator")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO users
        (username, name, balance, currency, role)
        VALUES (?, ?, ?, ?, ?)
    """, users)

    connection.commit()
    connection.close()