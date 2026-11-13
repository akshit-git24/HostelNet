from .database import get_user

def find_user(username: str):
    print(f"Searching for user: {username}")
    return get_user(username)

import sqlite3

def update_user_role(conn, username, new_role):
    cursor = conn.cursor()

    # Username was previously stored in the database
    cursor.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    if not user:
        return

    stored_username = user[0]

    # Vulnerability: stored data is later used unsafely
    query = (
        f"UPDATE users SET role = '{new_role}' "
        f"WHERE username = '{stored_username}'"
    )

    cursor.execute(query)
    conn.commit()




if __name__ == "__main__":
    username = input("Enter username: ")
    result = find_user(username)
    print(result)
