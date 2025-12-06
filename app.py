# app.py (KORRIGIERTE VERSION MIT READINESS PROBE)
from flask import Flask
import redis
import os
from flask import request
from datetime import datetime

app = Flask(__name__)

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = 6379 
r = None

def get_redis_connection():
    global r
    if r is None:
        # Erstellt die Verbindung
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    r.ping() # Ping, um die Verfügbarkeit zu prüfen
    return r

# --- NEUER ENDPUNKT FÜR KUBERNETES ---
@app.route('/health')
def health_check():
    try:
        get_redis_connection()
        return "OK", 200
    except Exception:
        # Wenn Redis nicht erreichbar ist, wird 503 zurückgegeben
        return "Service Unavailable", 503
    
@app.route('/reset')
def reset():
    try:
        redis_conn = get_redis_connection()
        redis_conn.set('visits', 0)
        return"Counter ist auf 0 zurückgesetzt.", 200
    except Exception:
        return "Zurücksetzten fehlgeschlagen.", 503    

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
    app.run(host='0.0.0.0', port=5000)

    