import sqlite3
from datetime import datetime

DB_PATH = "context.db"

def init_metrics_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT NOT NULL,
                value TEXT
            );
        ''')

def log_event(event_type: str, value: str = ""):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            INSERT INTO metrics (event_type, value)
            VALUES (?, ?)
        ''', (event_type, value))

def track_tool_usage(tool_name: str):
    log_event("Tool used", tool_name)

def track_context_hit(hit: bool):
    log_event("Context HIT" if hit else "Context MISS")

def track_tokens(prompt_tokens: int, response_tokens: int):
    log_event("Tokens - Prompt", str(prompt_tokens))
    log_event("Tokens - Response", str(response_tokens))

def track_latency(start_time: float):
    latency = round(datetime.now().timestamp() - start_time, 4)
    log_event("Latency", f"{latency}s")

def track_error():
    log_event("Error occurred")

def get_metrics(limit=100):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute('''
            SELECT timestamp, event_type, value
            FROM metrics
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()
