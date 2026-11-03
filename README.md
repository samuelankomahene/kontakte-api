# Kontakte REST-API

> **DE:** Entkoppeltes Python/Flask-REST-API-Backend mit relationaler SQLite-Datenbank. Entwickelt für den produktiven Betrieb auf einem Ubuntu 24.04 LTS Linux-VPS (Hetzner Cloud) hinter einem Nginx Reverse Proxy.
>
> **EN:** Decoupled Python/Flask REST API backend with relational SQLite database integration, engineered for production deployment on an Ubuntu 24.04 LTS Linux VPS behind an Nginx reverse proxy.

---

## 1. System Architecture & Traffic Flow

The deployment architecture enforces strict network isolation, **TLS termination** (decrypting incoming HTTPS traffic at the reverse proxy layer before forwarding over the private loopback interface), and process daemonization:

1. **UFW Firewall:** Restricts external ingress strictly to OpenSSH (`22`), HTTP (`80`), and HTTPS (`443`).
2. **Nginx Reverse Proxy:** Terminates public SSL/TLS (HTTPS via Let's Encrypt) and forwards requests internally over the private loopback interface (`127.0.0.1:5000`).
3. **Gunicorn WSGI Server:** Managed as a background `systemd` service daemon listening exclusively on `127.0.0.1:5000`.
4. **Flask Application (`app.py`):** Processes synchronous REST requests and executes parameterized CRUD operations against SQLite (`database/kontakte.db`).

### Technology Stack
* **Operating System:** Ubuntu Linux 24.04 LTS (Hetzner Cloud VPS)
* **Reverse Proxy & TLS:** Nginx with Let's Encrypt SSL/TLS certificates
* **WSGI Server:** Gunicorn (`26.2.0`) managed via `systemd`
* **Framework:** Python 3, Flask (`3.1.3`), Flask-CORS (`6.0.5`)
* **Database:** SQLite3 (Parameterized SQL queries & strict `ORDER BY` whitelisting)

---

## 2. Relational Database Schema (`SQLite3`)

Initialized via `database/db.py`:

```sql
CREATE TABLE IF NOT EXISTS kontakte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT DEFAULT "",
    telefon TEXT DEFAULT "",
    erstellt_am TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 3. REST API Endpoints

| HTTP Method | Endpoint | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| **`GET`** | `/api/kontakte` | Retrieve all contacts (supports `?search=`, `?sort=id\|name\|email\|erstellt_am`, `?limit=`, `?offset=`) | `200 OK`, `500` |
| **`GET`** | `/api/kontakte/<int:id>` | Retrieve a single contact by ID | `200 OK`, `404` |
| **`POST`** | `/api/kontakte` | Create a new contact (`{"name": "...", "email": "...", "telefon": "..."}`) | `201 Created`, `400` |
| **`PUT`** | `/api/kontakte/<int:id>` | Update an existing contact by ID | `200 OK`, `400`, `404` |
| **`DELETE`** | `/api/kontakte/<int:id>` | Delete a contact by ID | `204 No Content`, `404` |
| **`GET`** | `/api/kontakte/export` | Export all contacts as a downloadable CSV file (`kontakte_export.csv`) | `200 OK` |

---

## 4. Deployment & Local Setup Instructions

```bash
git clone https://github.com/samuelankomahene/kontakte-api.git
cd kontakte-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 database/db.py
python3 app.py
```
