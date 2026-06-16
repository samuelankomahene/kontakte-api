import sqlite3

def init_db():
    # 1. Establish connection (creates kontakte.db if it doesn't exist)
    # We create it in the root folder so the main app can access it easily
    conn = sqlite3.connect('kontakte.db')
    cursor = conn.cursor()

    # 2. Execute the exact SQL schema Stephan requested
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kontakte (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            telefon TEXT,
            erstellt_am DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 3. Commit the transaction and close the secure connection
    conn.commit()
    conn.close()
    
    print("System Log: Database initialized and 'kontakte' table verified.")

# This tells Python to run the init_db() function if we execute this file directly
if __name__ == '__main__':
    init_db()