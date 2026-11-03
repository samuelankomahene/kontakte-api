"""
Database initialization script for the Kontakte REST-API.
Creates the SQLite database file and the 'kontakte' table if they do not exist.
"""
import os
import sqlite3

def init_db():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'kontakte.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kontakte (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT DEFAULT '',
            telefon TEXT DEFAULT '',
            erstellt_am TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print(f"[OK] SQLite database initialized at: {db_path}")

if __name__ == '__main__':
    init_db()
