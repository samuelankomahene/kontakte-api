from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# --- INFRASTRUCTURE HELPER ---
def get_db_connection():
    # Connects to the database and formats the output as a Python dictionary
    # so Flask can easily convert it to JSON later.
    conn = sqlite3.connect('kontakte.db')
    conn.row_factory = sqlite3.Row 
    return conn

# --- REST API ENDPOINTS ---

# 1. READ ALL (GET)
@app.route('/api/kontakte', methods=['GET'])
def get_alle_kontakte():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute the SQL Command
        cursor.execute('SELECT * FROM kontakte')
        kontakte_rows = cursor.fetchall()
        conn.close()

        # Convert SQL rows into standard JSON format
        kontakte_liste = [dict(row) for row in kontakte_rows]
        
        return jsonify(kontakte_liste), 200
        
    except Exception as e:
        # System Administrator fallback: Catch errors so the server doesn't crash
        return jsonify({"error": str(e)}), 500

# --- SERVER BOOT ---
if __name__ == '__main__':
    # Running on Port 3000 to match your frontend configuration from Issue #4
    app.run(port=3000, debug=True)