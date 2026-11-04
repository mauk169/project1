import sqlite3
from models.operation import Operation

def get_connection():
    return sqlite3.connect('finance.db')

def create_operation(operation_type: str, amount: float, description: str, user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO operations (operation_type, amount, description, user_id)
        VALUES (?, ?, ?, ?)
    """, (operation_type, amount, description, user_id))
    conn.commit()
    conn.close()

def get_all_operations() -> list[Operation]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT operations.operation_id, operations.operation_type, operations.amount, operations.description, operations.user_id, users.login
        FROM operations
        JOIN users ON operations.user_id = users.user_id
    """)
    rows = cur.fetchall()
    conn.close()
    return [
        Operation(
            operation_id=r[0],
            operation_type=r[1],
            amount=r[2],
            description=r[3],
            user_id=r[4],
            user_login=r[5]
        ) for r in rows
    ]

def get_balance() -> float:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT operation_type, amount FROM operations")
    rows = cur.fetchall()
    conn.close()
    
    balance = 0.0
    for op_type, amount in rows:
        if "расход" in op_type.lower():
            balance -= amount
        else:
            balance += amount
    return balance
