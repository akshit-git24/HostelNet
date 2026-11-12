import sqlite3

def get_user(username: str):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # VULNERABILITY: SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}'"

    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()
    return result
