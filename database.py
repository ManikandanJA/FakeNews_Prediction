import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = "database.db"

def setup_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        news TEXT,
        result TEXT,
        confidence REAL,
        method TEXT,
        source_name TEXT,
        source_url TEXT,
        reason TEXT
    )
    """)

    conn.commit()
    conn.close()

# ── CREATE USER ────────────────────────
def create_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    hashed = generate_password_hash(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

# ── VERIFY USER ────────────────────────
def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user["password"], password):
        return dict(user)

    return None

# ── SAVE PREDICTION ───────────────────
def save_prediction(user_id, news, result, confidence, method, source_name, source_url, reason):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions 
    (user_id, news, result, confidence, method, source_name, source_url, reason)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, news, result, confidence, method, source_name, source_url, reason))

    conn.commit()
    conn.close()

# ── GET HISTORY (FIXED) ───────────────
def get_user_predictions(user_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]

# ── CLEAR HISTORY ─────────────────────
def clear_user_predictions(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM predictions WHERE user_id=?", (user_id,))

    conn.commit()
    conn.close()