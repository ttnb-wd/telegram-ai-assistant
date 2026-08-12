import sqlite3
from datetime import datetime


DATABASE = "memory.db"



def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id TEXT,

        role TEXT,

        message TEXT,

        created_at TEXT

    )
    """)


    conn.commit()

    conn.close()





def save_message(user_id, role, message):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO messages
        (user_id, role, message, created_at)

        VALUES (?, ?, ?, ?)
        """,
        (
            str(user_id),
            role,
            message,
            datetime.now().isoformat()
        )
    )


    conn.commit()

    conn.close()





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
        (
            str(user_id),
            limit
        )
    )


    data = cursor.fetchall()


    conn.close()


    data.reverse()


    return data