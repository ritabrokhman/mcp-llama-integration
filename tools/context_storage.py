import sqlite3
from datetime import datetime

DB_PATH = "context.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT NOT NULL,
                user_id TEXT,
                prompt TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')

def save_context(tool_name, user_id, prompt, response):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            INSERT INTO context (tool_name, user_id, prompt, response)
            VALUES (?, ?, ?, ?)
        ''', (tool_name, user_id, prompt, response))

def get_recent_context(user_id, limit=5):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute('''
            SELECT prompt, response, timestamp
            FROM context
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        return cursor.fetchall()
