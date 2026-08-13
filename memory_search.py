import sqlite3

DATABASE = "memory.db"


def search_keyword(keyword):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username, role, message, created_at
        FROM messages
        WHERE message LIKE ?
        ORDER BY id DESC
        """,
        (f"%{keyword}%",)
    )

    results = cursor.fetchall()

    conn.close()

    return results


def search_user(username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username, role, message, created_at
        FROM messages
        WHERE username LIKE ?
        ORDER BY id DESC
        """,
        (f"%{username}%",)
    )

    results = cursor.fetchall()

    conn.close()

    return results


def search_date(date):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username, role, message, created_at
        FROM messages
        WHERE created_at LIKE ?
        ORDER BY id ASC
        """,
        (f"{date}%",)
    )

    results = cursor.fetchall()

    conn.close()

    return results


if __name__ == "__main__":

    print("Memory Search Tool")
    print("==================")

    keyword = input("Search keyword: ")

    results = search_keyword(keyword)

    print()

    if not results:
        print("No messages found.")

    else:

        for username, role, message, created_at in results:

            print(
                f"[{created_at}] "
                f"{username} | "
                f"{role}: "
                f"{message}"
            )