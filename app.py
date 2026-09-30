# --- CORE MODULE IMPORTS ---
import os
import sqlite3
import csv
import io
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

# --- SYSTEM INITIALIZATION ---
app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing for frontend integration

# --- INFRASTRUCTURE HELPER ---
def get_db_connection():
    """
    Establishes a connection to the SQLite database.
    Uses absolute pathing to ensure stability when executed as a systemd daemon via Gunicorn.
    """
    # Dynamically resolve the absolute path to prevent systemd WorkingDirectory crashes
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'database', 'kontakte.db')
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# --- REST API ENDPOINTS ---

@app.route('/api/kontakte', methods=['GET'])
def get_alle_kontakte():
    """ Retrieves all contacts with optional search, sort, and pagination parameters. """
    try:
        search = request.args.get('search', '')
        sort = request.args.get('sort', 'id') 
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', 0, type=int)

        query = 'SELECT * FROM kontakte'
        params = []

        if search:
            query += ' WHERE name LIKE ?'
            params.append(f'%{search}%')

        # Defense against SQL Injection using a strict Whitelist
        erlaubte_sortierungen = ['id', 'name', 'email', 'erstellt_am']
        if sort in erlaubte_sortierungen:
            query += f' ORDER BY {sort}'
        else:
            query += ' ORDER BY id' 

        if limit is not None:
            query += ' LIMIT ? OFFSET ?'
            params.extend([limit, offset])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        kontakte_rows = cursor.fetchall()
        conn.close()

        return jsonify([dict(row) for row in kontakte_rows]), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/kontakte/export', methods=['GET'])
def export_kontakte():
    """ Exports the entire contacts database to a downloadable CSV file. """
    conn = get_db_connection()
    kontakte = conn.execute('SELECT * FROM kontakte').fetchall()
    conn.close()

    si = io.StringIO()
    cw = csv.writer(si)

    if kontakte:
        cw.writerow(kontakte[0].keys())
        for row in kontakte:
            cw.writerow(row)

    output = si.getvalue()

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=kontakte_export.csv"}
    )

@app.route('/api/kontakte/<int:id>', methods=['GET'])
def get_einzelner_kontakt(id):
    """ Retrieves a single contact payload based on the provided ID. """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM kontakte WHERE id = ?', (id,))
        kontakt_row = cursor.fetchone()
        conn.close()

        if kontakt_row is None:
            return jsonify({"error": "Kontakt nicht gefunden"}), 404

        return jsonify(dict(kontakt_row)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/kontakte', methods=['POST'])
def create_kontakt():
    """ Ingests a JSON payload and creates a new database record. """
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

@app.route('/api/kontakte/<int:id>', methods=['PUT'])
def update_kontakt(id):
    """ Updates an existing database record based on the provided ID. """
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

@app.route('/api/kontakte/<int:id>', methods=['DELETE'])
def delete_kontakt(id):
    """ Executes a database deletion command for a specific contact ID. """
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
    # SECURITY NOTICE: debug=True is strictly disabled for production environments.
    # When deployed on Hetzner, Gunicorn bypasses this block and binds to 127.0.0.1:5000 directly.
    app.run(port=3000, debug=False)