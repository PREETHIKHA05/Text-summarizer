import sqlite3
import json

DB_FILE = "poc.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS poc (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT,
            output_json TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_text(input_text, output_json):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO poc (input_text, output_json) VALUES (?, ?)",
        (input_text, json.dumps(output_json))
    )
    conn.commit()
    conn.close()

def last_five_runs(limit=5):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT input_text, output_json FROM poc ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [{"input": r[0], "output": json.loads(r[1])} for r in rows]
