import sqlite3
from models.user import User

def get_connection():
    return sqlite3.connect('finance.db')

def get_by_login(login: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.user_id, u.login, u.password, u.user_role, r.role_name
        FROM users u
        JOIN user_roles r ON u.user_role = r.role_id
        WHERE u.login = ?
    """, (login,))
    row = cur.fetchone()
    conn.close()
    if row:
        return User(user_id=row[0], login=row[1], password=row[2], user_role=row[3], role_name=row[4])
    return None

def create_user(login: str, password: str, user_role: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (login, password, user_role)
        VALUES (?, ?, ?)
    """, (login, password, user_role))
    conn.commit()
    conn.close()

def update_user_password(user_id: int, new_password: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET password = ? WHERE user_id = ?", (new_password, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, login, user_role FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows