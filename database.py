import sqlite3

DB_NAME = "users.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        full_name TEXT,
        username TEXT,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        question TEXT,
        answer TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def add_user(telegram_id, full_name, username):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO users
    (telegram_id, full_name, username)
    VALUES (?, ?, ?)
    """, (telegram_id, full_name, username))

    conn.commit()
    conn.close()


def save_history(telegram_id, question, answer):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO history
    (telegram_id, question, answer)
    VALUES (?, ?, ?)
    """, (telegram_id, question, answer))

    conn.commit()
    conn.close()


def get_users_count():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    conn.close()

    return count


create_tables()
