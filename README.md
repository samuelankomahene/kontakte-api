# Kontakte REST-API

## Architecture Overview
This repository contains a backend REST API for a contacts management system. It is engineered for a production environment hosted on a Hetzner Linux VPS, demonstrating full-stack system integration, daemonization, and strict traffic routing.

### Technology Stack
- **Host OS:** Ubuntu Linux 24.04
- **Web Server:** Nginx (Reverse Proxy)
- **WSGI Server:** Gunicorn (Managed via `systemd`)
- **Framework:** Python 3 / Flask
- **Database:** SQLite3

## Infrastructure Traffic Flow
The deployment architecture ensures strict separation of concerns and security:
1. **UFW Firewall:** Only permits external traffic on OpenSSH (22), HTTP (80), and HTTPS (443).
2. **Nginx Reverse Proxy:** Intercepts public HTTP traffic on Port 80 and securely forwards it internally.
3. **Gunicorn WSGI:** Listens internally on Port 5000, managing the Python Flask application workers.
4. **Flask Application:** Processes the REST constraints and executes CRUD operations against the `.db` file.

## Deployment Instructions (Ubuntu Server)

### 1. Environment Setup
Clone the repository and isolate the dependencies:
```bash
git clone [https://github.com/samuelankomahene/kontakte-api.git](https://github.com/samuelankomahene/kontakte-api.git)
cd kontakte-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt