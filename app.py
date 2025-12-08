# app.py (KORRIGIERTE VERSION MIT READINESS PROBE)
from flask import Flask, request
import redis
import os
from datetime import datetime

app = Flask(__name__)

# Redis-Verbindungsdaten aus Umgebungsvariablen
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
r = None

def get_redis_connection():
    global r
    if r is None:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    r.ping()  # Prüft, ob Redis erreichbar ist
    return r

# --- Kubernetes Health-Check ---
@app.route('/health')
def health_check():
    try:
        get_redis_connection()
        return "OK", 200
    except Exception:
        return "Service Unavailable", 503

# --- Zähler zurücksetzen ---
@app.route('/reset')
def reset():
    try:
        redis_conn = get_redis_connection()
        redis_conn.set('visits', 0)
        return "Counter ist auf 0 zurückgesetzt.", 200
    except Exception:
        return "Zurücksetzen fehlgeschlagen.", 503

# --- Visits pro IP ---
@app.route('/myvisit')
def myvisit():
    try:
        redis_conn = get_redis_connection()
        ip = request.remote_addr
        key = f'visits_{ip}'
        count = redis_conn.incr(key)
        return f'Deine IP {ip} hat diese Seite {count} mal besucht.\n', 200
    except Exception:
        return "FEHLER: Der Zählerdienst ist derzeit nicht verfügbar.", 503

# --- Globaler Visit-Counter ---
@app.route('/')
def counter():
    try:
        redis_conn = get_redis_connection()
        visits = redis_conn.incr('visits')
        redis_conn.set('last_visit', datetime.utcnow().isoformat())
        return f'Der Cloud-Visit-Counter steht bei: {visits} Besuchen.\n', 200
    except Exception:
        return "FEHLER: Der Zählerdienst ist derzeit nicht verfügbar.", 503

if __name__ == '__main__':
    # WICHTIG: host='0.0.0.0', damit Kubernetes und Port-Forward funktionieren
    app.run(host='0.0.0.0', port=500)