import sqlite3
from datetime import datetime

DATABASE = "memory.db"


# ==========================
# Create Database
# ==========================


def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        username TEXT,
        role TEXT,
        message TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()


# ==========================
# Save Message
# ==========================


def save_message(user_id, role, message, username="unknown"):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO messages (user_id, username, role, message, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (str(user_id), username, role, message, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


# ==========================
# Get AI Memory
# ==========================


def get_history(user_id, limit=10):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT role, message
        FROM messages
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT ?
        """,
        (str(user_id), limit),
    )
    data = cursor.fetchall()
    conn.close()
    data.reverse()
    return data


# ==========================
# Search History
# ==========================


def search_history(keyword):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT username, role, message, created_at
        FROM messages
        WHERE message LIKE ?
        ORDER BY id DESC
        """,
        (f"%{keyword}%",),
    )
    data = cursor.fetchall()
    conn.close()
    return data


# ==========================
# Export All History
# ==========================


def export_history():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM messages
        ORDER BY id ASC
        """
    )
    data = cursor.fetchall()
    conn.close()
    return data