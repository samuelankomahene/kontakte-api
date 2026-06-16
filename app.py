from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# --- INFRASTRUCTURE HELPER ---
def get_db_connection():
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
        cursor.execute('SELECT * FROM kontakte')
        kontakte_rows = cursor.fetchall()
        conn.close()

        return jsonify([dict(row) for row in kontakte_rows]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. READ SINGLE (GET by ID) - Aufgabe 4
@app.route('/api/kontakte/<int:id>', methods=['GET'])
def get_einzelner_kontakt(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Parameterized query using '?' to prevent SQL injection
        cursor.execute('SELECT * FROM kontakte WHERE id = ?', (id,))
        kontakt_row = cursor.fetchone()
        conn.close()

        # Error Handling: If the ID does not exist in the database
        if kontakt_row is None:
            return jsonify({"error": "Kontakt nicht gefunden"}), 404

        return jsonify(dict(kontakt_row)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. CREATE (POST) - Aufgabe 5
@app.route('/api/kontakte', methods=['POST'])
def create_kontakt():
    try:
        # Intercept the incoming HTTP Request Body
        neuer_kontakt = request.get_json()
        
        # Validation: The database rule says 'name' is NOT NULL
        if not neuer_kontakt or 'name' not in neuer_kontakt:
            return jsonify({"error": "Bad Request: Feld 'name' ist ein Pflichtfeld"}), 400

        name = neuer_kontakt['name']
        email = neuer_kontakt.get('email', '')
        telefon = neuer_kontakt.get('telefon', '')

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute the INSERT command securely using '?' placeholders
        cursor.execute('''
            INSERT INTO kontakte (name, email, telefon)
            VALUES (?, ?, ?)
        ''', (name, email, telefon))
        
        conn.commit()
        
        # Grab the auto-generated ID of the newly inserted row
        neue_id = cursor.lastrowid
        conn.close()

        return jsonify({"id": neue_id, "message": "Kontakt erfolgreich erstellt"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- SERVER BOOT ---
if __name__ == '__main__':
    app.run(port=3000, debug=True)