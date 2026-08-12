# Kontakte API - Backend Infrastructure

## System Architecture
This repository houses the backend REST-API for the Kontakte software ecosystem. It is engineered strictly with **Python** and **Flask**, utilizing a local **SQLite** database for persistent data storage. 

## Network Pipelines (REST Endpoints)
This server is configured to intercept and route the following HTTP network requests:
* `GET /api/kontakte` - Retrieves the full JSON payload of all contacts in the database.
* `POST /api/kontakte` - Ingests a JSON payload to create a new database entry.
* `PUT /api/kontakte/:id` - Updates an existing contact based on ID.
* `DELETE /api/kontakte/:id` - Executes a database deletion command for a specific contact.

## Infrastructure Security
* **CORS:** Cross-Origin Resource Sharing is natively configured via `flask-cors` to allow secure data transmission to the frontend client.
* **SQL Injection Protection:** All SQLite database routing utilizes Parameterized Queries to prevent malicious data execution.

## Local Server Deployment
To spin up this server environment locally:
1. Activate the virtual environment: `source venv/bin/activate` (macOS/Linux)
2. Install dependencies: `pip install -r requirements.txt`
3. Boot the server: `python app.py`