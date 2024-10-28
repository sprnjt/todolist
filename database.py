import sqlite3
from sqlite3 import Connection

# CONNECTING THE DATABASE   
def get_db_connection() -> Connection:
    conn = sqlite3.connect('todos.db')
    conn.row_factory = sqlite3.Row
    return conn

# CREATING THE TABLE    
def init_db():
    with get_db_connection() as conn:
        # CREATING THE TABLE WITH ID AS PRIMARY KEY
        conn.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN NOT NULL DEFAULT 0    
            )
        ''')
        conn.commit()

