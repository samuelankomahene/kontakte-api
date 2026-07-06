# --- CORE MODULE IMPORTS ---
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- SYSTEM INITIALIZATION ---
# 1. Boot the Flask server engine
app = Flask(__name__)

# 2. Attach the Cross-Origin Resource Sharing (CORS) security middleware
CORS(app)
# --- INFRASTRUCTURE HELPER ---
def get_db_connection():
    # Connects to the SQLite database and formats the output as a Python dictionary
    conn = sqlite3.connect('kontakte.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- REST API ENDPOINTS ---

# 1. READ ALL (GET) - Bonus Aufgabe 9 (Search, Sort, Pagination)
@app.route('/api/kontakte', methods=['GET'])
def get_alle_kontakte():
    try:
        # 1. Extract Query Parameters from the URL
        search = request.args.get('search', '')
        sort = request.args.get('sort', 'id')  # Defaults to sorting by ID
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', 0, type=int) # Defaults to 0

        # 2. Start building the Base SQL Query
        query = 'SELECT * FROM kontakte'
        params = []

        # 3. Apply Search Filter (WHERE)
        if search:
            # The % symbols are SQL wildcards. '%Max%' means "contains Max anywhere"
            query += ' WHERE name LIKE ?'
            params.append(f'%{search}%')

        # 4. Apply Sorting (ORDER BY)
        # WHITELIST: Only allow sorting by specific columns to prevent SQL Injection!
        erlaubte_sortierungen = ['id', 'name', 'email', 'erstellt_am']
        if sort in erlaubte_sortierungen:
            query += f' ORDER BY {sort}'
        else:
            query += ' ORDER BY id' # Fallback if hacker tries to inject code

        # 5. Apply Pagination (LIMIT & OFFSET)
        if limit is not None:
            query += ' LIMIT ? OFFSET ?'
            params.extend([limit, offset])

        # 6. Execute the final Dynamic Query
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
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

        if kontakt_row is None:
            return jsonify({"error": "Kontakt nicht gefunden"}), 404

        return jsonify(dict(kontakt_row)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. CREATE (POST) - Aufgabe 5
@app.route('/api/kontakte', methods=['POST'])
def create_kontakt():
    try:
        neuer_kontakt = request.get_json()
        
        if not neuer_kontakt or 'name' not in neuer_kontakt:
            return jsonify({"error": "Bad Request: Feld 'name' ist ein Pflichtfeld"}), 400

        name = neuer_kontakt['name']
        email = neuer_kontakt.get('email', '')
        telefon = neuer_kontakt.get('telefon', '')

        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO kontakte (name, email, telefon)
            VALUES (?, ?, ?)
        ''', (name, email, telefon))
        
        conn.commit()
        
        neue_id = cursor.lastrowid
        conn.close()

        return jsonify({"id": neue_id, "message": "Kontakt erfolgreich erstellt"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4. UPDATE (PUT) - Aufgabe 6
@app.route('/api/kontakte/<int:id>', methods=['PUT'])
def update_kontakt(id):
    try:
        update_daten = request.get_json()
        
        if not update_daten or 'name' not in update_daten:
            return jsonify({"error": "Bad Request: Feld 'name' ist ein Pflichtfeld"}), 400

        name = update_daten['name']
        email = update_daten.get('email', '')
        telefon = update_daten.get('telefon', '')

        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE kontakte 
            SET name = ?, email = ?, telefon = ? 
            WHERE id = ?
        ''', (name, email, telefon, id))
        
        conn.commit()

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Kontakt nicht gefunden"}), 404

        conn.close()
        return jsonify({"message": f"Kontakt {id} erfolgreich aktualisiert"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 5. DELETE - Aufgabe 7
@app.route('/api/kontakte/<int:id>', methods=['DELETE'])
def delete_kontakt(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM kontakte WHERE id = ?', (id,))
        conn.commit()

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Kontakt nicht gefunden"}), 404

        conn.close()
        return '', 204 

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- SERVER BOOT ---
if __name__ == '__main__':
    app.run(port=3000, debug=True)